import random, time
from datetime import date
from faker import Faker
from sqlalchemy import func, insert
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
        session = Session(engine)
        frame_size = 100000
        for i in range(0, len(employee_list), frame_size):
            frame = employee_list[i:i+frame_size]
            session.bulk_save_objects(frame)
            session.commit()
        session.close()

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
    session = Session(engine)
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
    session.close()


def automatic_filling_directory():
    fake = Faker("ru_RU")
    Faker.seed(50)
    random.seed(50)

    employees = []
    for _ in range(1000000):
        first_letter = random.choice('АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЬЪЭЮЯ')
        last_name = first_letter + fake.last_name()[1:]
        gender = random.choice(["мужской", "женский"])
        if gender == "мужской":
            first_name = fake.first_name_male()
            middle_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()
            middle_name = fake.first_name_female()
        name = f"{last_name} {first_name} {middle_name}"        
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)

        employees.append(Employee(name, date_of_birth, gender))

    for _ in range(100):
        employees.append(
            Employee(
                name = (
                    f"Ф{fake.last_name_male()}" 
                    f"{fake.first_name_male()}"
                    f"{fake.middle_name_male()}"
                ),
                date_of_birth = fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=65
                ),
                gender = 'мужской'
            )
        )
    Employee.batch_adding_records(employees)
    print("База заполнена")


def sampling_time_measurement():
    t_start = time.perf_counter()
    pass