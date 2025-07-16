from datetime import date, datetime
from database import create_table


class App:
    def __init__(self, launch_app=False):
        self.launch_app = launch_app
    
    def start_app(self):
        self.launch_app = True
    
    def menu(self):
        print(
            "Выберите один из пунктов меню:\n"
            "1 - Создание таблицы\n"
            "2 - Добавить запись в таблицу\n"
            "3 - Посмотреть всех сотрудников в справочнике\n"
            "4 - Заполнение справочника сотрудников из списка\n"
            "5 - Получить отфильтрованные данные из таблицы\n"
            "0 - Выход из приложения"
        )
        number_menu = input("...Введите число: ")
        try:
            number_menu = int(number_menu)
            if number_menu == 0:
                print("До свидания!")
                self.launch_app = False
            elif number_menu == 1:
                create_table()
            elif number_menu == 2:
                lats_name = input("...Введите имя: ")
                first_name = input("...Введите фамилию: ")
                patronymic = input("...Введите отчество: ")
                date_string = input("...Введите дату рождения в формате ГГГГ-ММ-ДД.: ")
                try:
                    date_of_birth = datetime.strptime(date_string, "%Y-%m-%d").date()
                except ValueError:
                    print("Некорректный формат даты.")
                    date_string = input("...Введите дату рождения в формате ГГГГ-ММ-ДД.: ")
                gender = input("...Укажите ваш пол: ")
                employee = Employee(
                    lats_name,
                    first_name,
                    patronymic,
                    date_of_birth,
                    gender
                )
                employee.create_a_recording_in_the_table()
            elif number_menu == 3:
                pass
            elif number_menu == 4:
                pass
            elif number_menu == 5:
                pass
        except ValueError:
            print(
                "Ошибка! Введите число от 1 до 5 включительно."
                "Или 0 для выхода"
            )



class Employee:
    def __init__(
        self,
        last_name: str,
        first_name: str,
        patronymic: str,
        date_of_birth: date,
        gender: str
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.date_of_birth = date_of_birth
        self.gender = gender
        print("Сотрудник создан")
    
    def __str__(self):
        return (
            f"Сотрудник {self.last_name}"
            f"{self.first_name} добавлен в базу."
        )

    def create_a_recording_in_the_table(self):
        pass

    def age_calculation(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (
            self.date_of_birth.month >= today.month and 
            self.date_of_birth.day > today.day
        ):
            age -= 1
        return age


if __name__ == "__main__":
    print("Добро пожаловать в приложение по работе с базой данных!")
    app = App()
    app.start_app()
    while(app.launch_app):
        app.menu()
