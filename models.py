from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


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
