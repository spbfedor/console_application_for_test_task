from datetime import datetime
from database import create_table, delete_table
from models import create_a_record


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
                lats_name = input("...Введите фамилию: ")
                first_name = input("...Введите имя: ")
                patronymic = input("...Введите отчество: ")
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

                create_a_record(
                    lats_name,
                    first_name,
                    patronymic,
                    date_of_birth,
                    gender
                )
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


if __name__ == "__main__":
    print("Добро пожаловать в приложение по работе с базой данных!")
    app = App()
    app.start_app()
    while(app.launch_app):
        app.menu()
