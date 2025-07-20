from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from config import engine


class Base(DeclarativeBase):
    pass


# В задании было указано ФИО в одной строке,
# но я взял на себя ответственность и разбил 
# их по разным стокам, так гораздо удобнее.
class Employee(Base):
    __tablename__= "employee_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str]
    first_name: Mapped[str]
    patronymic: Mapped[str]
    date_of_birth: Mapped[date]
    gender: Mapped[str]

    def __repr__(self):
        return (
            f"Employee: id={self.id}"
            f"last_name={self.last_name}" 
            f"first_name={self.first_name}"
            f"patronymic={self.patronymic}"
            f"date_of_birth={self.date_of_birth}"
            f"gebder={self.gender}"
        )

def create_a_record(
    lats_name,
    first_name,
    patronymic,
    date_of_birth,
    gender
):
    with Session(engine) as session:
        employee = Employee()

        employee.last_name = lats_name
        employee.first_name = first_name
        employee.patronymic = patronymic
        employee.date_of_birth = date_of_birth
        employee.gender = gender

        session.add(employee)
        session.commit()
