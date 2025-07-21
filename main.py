from datetime import datetime

from database import create_table, delete_table
from models import automatic_filling_directory, Employee
from models import output_of_unique_employees, sampling_time_measurement


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
                delete_table()
                print("До свидания!")
                self.launch_app = False
            elif number_menu == 1:
                create_table()
            elif number_menu == 2:
                name = input("...Введите ФИО: ")
                date_string = input(
                    "...Введите дату рождения в формате ГГГГ-ММ-ДД.: "
                )

                try:
                    date_of_birth = datetime.strptime(
                        date_string,
                        "%Y-%m-%d"
                    ).date()
                except ValueError:
                    print("Некорректный формат даты.")
                    date_string = input("...Введите дату рождения в формате ГГГГ-ММ-ДД.: ")

                gender = input("...Укажите ваш пол: ")
                Employee.create_a_record(
                    name,
                    date_of_birth,
                    gender
                )
            elif number_menu == 3:
                output_of_unique_employees()
            elif number_menu == 4:
                automatic_filling_directory()
            elif number_menu == 5:
                sampling_time_measurement()
        except ValueError:
            print(
                "Ошибка! Введите число от 1 до 5 включительно."
                "Или 0 для выхода"
            )


if __name__ == "__main__":
    print("Добро пожаловать в приложение по работе с базой данных!")
    app = App()
    app.start_app()
    while(app.launch_app):
        app.menu()
