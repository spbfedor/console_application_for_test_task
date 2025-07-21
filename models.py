import random, time
from datetime import date

from faker import Faker
from sqlalchemy import func, Index, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from config import engine


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__= "employee_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    date_of_birth: Mapped[date]
    gender: Mapped[str]

    def __init__(self, name, date_of_birth, gender):
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender

    def age_calculation(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (
            self.date_of_birth.month >= today.month and 
            self.date_of_birth.day > today.day
        ):
            age -= 1
        return age
    
    def batch_adding_records(employee_list):
        with Session(engine) as session:
            frame_size = 10000
            for i in range(0, len(employee_list), frame_size):
                frame = employee_list[i:i+frame_size]
                session.bulk_save_objects(frame)
                session.commit()
                session.expunge_all()

    def create_a_record(
        name,
        date_of_birth,
        gender
    ):
        with Session(engine) as session:
            employee = Employee(
                name,
                date_of_birth,
                gender
            )

            session.add(employee)
            session.commit()


def output_of_unique_employees():
    with Session(engine) as session:
        sub_query = (
            session.query(
                Employee.name,
                Employee.date_of_birth,
                func.min(Employee.id).label("min_id"))
            .group_by(Employee.name, Employee.date_of_birth)
            .subquery()
        )
        employees = (
             session.query(Employee)
            .join(sub_query, Employee.id == sub_query.c.min_id)
            .order_by(Employee.name)
            .all()
        )
        for employee in employees:
            age = employee.age_calculation()
            print(
                f"{employee.name}, {employee.date_of_birth}, {age}"
            )


def automatic_filling_directory():
    fake = Faker()
    Faker.seed(50)
    random.seed(50)

    employees = []
    for _ in range(1000000):
        first_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        last_name = first_letter + fake.last_name()[1:]
        gender = random.choice(["male", "female"])
        if gender == "male":
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()
        name = f"{last_name} {first_name}"        
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)

        employees.append(Employee(name, date_of_birth, gender))

    for _ in range(100):
        employees.append(
            Employee(
                name = (
                    f"F{fake.last_name_male()}" # тут нужно доработать.
                    f"{fake.first_name_male()}"
                ),
                date_of_birth = fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=65
                ),
                gender = 'male'
            )
        )
    Employee.batch_adding_records(employees)
    print("База заполнена")


def sampling_time_measurement():
    with Session(engine) as session:
        t_start = time.perf_counter()
        sample = (
            session.query(Employee)
            .filter(Employee.gender == 'male', Employee.name.like("F%"))
            .all()
        )
        lead_time = time.perf_counter() - t_start
        print(f"Время выборки {len(sample)} строк {lead_time:.6F} секунд")
        return lead_time


def query_optimization():
    with Session(engine) as session:
        session.execute(text("DROP INDEX IF EXISTS index_gender_name_lower"))
        session.commit()
    
    print("...До оптимизации...")
    before_time = sampling_time_measurement()

    with Session(engine) as session:
        session.execute(text(
            "CREATE INDEX index_gender_name_lower ON employee_list "
            "(gender, lower(name) varchar_pattern_ops)"
        ))
        session.commit()

        session.execute(text("ANALYZE employee_list"))
        session.commit()
    
    time.sleep(1)

    print("...После оптимизации...")
    after_time = sampling_time_measurement()

    result = before_time - after_time
    print(f"Запрос быстрее на {result:.6F} секунд.")

