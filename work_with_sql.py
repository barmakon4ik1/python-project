import configparser
from mysql.connector import MySQLConnection, Error
from prettytable import from_db_cursor
import titel_screen
from colorama import init
from colorama import Fore
import logic


init(autoreset=True)
query_color = Fore.LIGHTCYAN_EX
error_color = Fore.RED
info_color = Fore.LIGHTYELLOW_EX
text_color = Fore.LIGHTGREEN_EX
title_color = Fore.GREEN


def read_config(section):
    """ Чтение файла конфигурации config.ini и возвращение словаря с данными для подключения к БД """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        host = config.get(section, 'host')
        user = config.get(section, 'username')
        password = config.get(section, 'password')
        database = config.get(section, 'database')
        dbconfig = {'host': host, 'user': user, 'password': password, 'database': database}
        # print(Fore.LIGHTBLACK_EX + f"Соединение с базой данных {database} установлено")
        return dbconfig
    except Exception as err:
        print(error_color + f"Ошибка при подключении к базе данных: \b{err}")


def disconnect_from_db(conn):
    """ Модуль закрытия подключения к БД.Разрывает соединение и закрывает его."""
    conn.close()


def parting():
    """ Просто прощание """
    print(info_color + "\nНу что ж, выход - так выход. Будем ждать твоего возвращения!\n")
    print(query_color + f"""                       |\\__/,|   (`\\
                       |_ _  |.--.) )
                       ( T   )     /
                      (((^_(((/(((_/""")


def choose_category():
    """  Составляет запрос на показ номера категории и ее название """
    try:
        select = f"SELECT category.category_id AS №, category.name AS Категория"
        from_table = "FROM category"
        return f"{select} {from_table};"
    except Error as err:
        print(error_color + 'Ошибка при составлении запроса: {err}')


def where_constructor(choice, value):
    """ Конструктор специальных запросов и условий """
    release_year = "film.release_year AS Год_выпуска"
    title = "film.title AS Название"
    category = "category.name AS Категория"
    description = "film.description AS Описание"
    if choice == 1:
        select = f"SELECT DISTINCT {release_year}, {title} "
        where = f'WHERE category.category_id = {value}'
    elif choice == 2:
        select = f"SELECT DISTINCT {category}, {release_year}, {title} "
        if value == 0:
            where = ""
        else:
            where = f'WHERE film.release_year {value}'
    elif choice == 3:
        select = f"SELECT DISTINCT {category}, {release_year}, {title} "
        where = f"WHERE film.title LIKE '%{value}%'"
    elif choice == 4:
        select = f"SELECT DISTINCT {description}, {title}, {category}, {release_year} "
        where = f"WHERE film.description LIKE '%{value}%' OR film.title LIKE '%{value}%'"
    elif choice == 5:
        select = f"SELECT DISTINCT {release_year}, {title} "
        where = f'WHERE category.category_id = {value[0]} AND film.release_year {value[1]}'
    else:
        print(error_color + "Непостижимо! Как ты сюда попал? ")
    return select, where


def search_by_title():
    """ Модуль поиска по названию """
    print(text_color + """+---------------------------------------------------------------+
| Будем искать по буквам в названии фильма.                     |
| Предупреждаю, это почти самый сложный выбор!                  |
| Потому что нужно ввести что то из названия фильма.            |
| Или просто нажми ввод и тогда пойдешь к выходу.               |
+---------------------------------------------------------------+""")
    print(query_color + "\nВведи буквы из названия фильма, можно в любом регистре: ")
    title = input().upper()
    if title:
        return title
    else:
        parting()
        return 0


def search_by_description():
    """ Модуль поиска по частям описания """
    print(text_color + """+---------------------------------------------------------------+
| Наконец, самый сложный и непредсказуемый метод!               |
| Он позволяет искать по словам, буквам в описании фильма,      |
| Ну или не вводи ничего и тогда программа будет закрыта        |
+---------------------------------------------------------------+""")
    print(query_color + "\nВведи что то из внятных слов и мы поищем, что подойдет: ")
    description_tail = input()
    if description_tail:
        return description_tail
    else:
        parting()
        return 0


def search_by_year():
    """ Поиск по году выпуска фильма """
    print(text_color + """+---------------------------------------------------------------+
| Будем искать по году выпуска фильма в свет:                   |
|                           точное совпадение              - 1  |
|                           ранее чем вводимый год         - 2  |
|                           позднее, чем выбранный год     - 3  |
| Просто выйти отсюда жми все, что угодно                       |
+---------------------------------------------------------------+""")
    try:
        print(query_color + "\nТвой выбор: ")
        choice = input()
        if choice in ["1", "2", "3"]:
            print(query_color + "Теперь введи желаемый год: ")
            year = int(input())
        if choice == "1":
            sign = " = "
        elif choice == "2":
            sign = " <= "
        elif choice == "3":
            sign = " >= "
        else:
            parting()
            return 0
        return f"{sign} {year}"
    except Exception as e:
        print(error_color + f"Таких фильмов не нашлось, сожалею...")


def order_by_field():
    """ сортировка результата """
    print(info_color + "\nПо какому критерию будем сортировать результат?\n")
    print(text_color + """+---------------------------------------------------------------+
| Сортировка по названию фильма в алфавитном порядке    -   1   |
| или по дате выхода на экран от старого к новому       -   2   |
| если интересуют сперва новее, отсортируем наоборот    -   3   |
| если сортировка нам 'по барабану', жми что хочешь             |
+---------------------------------------------------------------+""")
    try:
        print(query_color + "\nВыбирайте сортировку: ")
        point = input()
        if point == "1":
            return f"ORDER BY film.title "
        elif point == "2":
            return f"ORDER BY film.release_year "
        elif point == "3":
            return f"ORDER BY film.release_year DESC "
        else:
            return ""
    except Exception as e:
        print(error_color + f"Произошла ошибка! {e}")


def choice_limit():
    """ ограничение на показ выборки """
    print(query_color + "\nСколько названий фильмов вывести на экран? Если не укажешь - выведу все: ")
    value = input()
    if value.isdigit() and int(value) > 0:
        print(info_color + f"\nТы ввел ограничение в количестве не более {value} названий: \n")
        return f"LIMIT {value}"
    else:
        print(info_color + "\nОграничений не указано - будут выведены все результаты!\n")
        return "\n"


def query_constructor(choice, value):
    """ Конструктор запросов, принимает выбор критериев и выдает текст для запроса"""
    # Эти значения будут выбраны в любом случае
    from_table = f"FROM film\n"
    join_tables = f"""JOIN film_category ON film.film_id = film_category.film_id
             JOIN category ON film_category.category_id = category.category_id
             JOIN language ON language.language_id = film.language_id
             JOIN film_actor ON film.film_id = film_actor.film_id
             JOIN actor ON film_actor.actor_id = actor.actor_id\n"""
    # далее идут специальные конструкции к выборке (поля, условия, количество)
    if choice != "0":
        select, where = where_constructor(choice, value)
        order_by = order_by_field()
        limit = choice_limit()
        # Возврат готового запроса
        query = f"{select} {from_table} {join_tables} {where} {order_by} {limit};"
        statistic = f" {where} {order_by} {limit}"
        return query, statistic


def search_by_category():
    """ Модуль выбора фильма по категории. Принимает курсор и номер категории """
    flag = True
    try:
        while flag:
            try:
                print(query_color + "\nВведите номер категории или 0 для отмены и выхода: ")
                category = int(input())
                if category == 0:
                    parting()
                    return 0
                elif category < 1 or category > 16:
                    print(info_color + "\nК сожалению, такой категории у нас нет, выбери по-новой")
                else:
                    return category
            except ValueError:
                print(error_color + "Вводить можно только число от 0 до 16. Повторим выбор")
                flag = True
    except Exception as e:
        print(error_color + f"Произошла ошибка! {e}")


def choice_select():
    """ Модуль выбора по критериям. Отсюда стартует разветвление по выборке"""
    print(text_color + """+---------------------------------------------------------------+
|  Сперва нужно выбрать по каким критериям будем отбирать:      |
|  Наверное сначала определимся с категорией фильма?       - 1  |
|  Или лучше отберем фильмы по дате выхода в свет?         - 2  |
|  Понимаю, ни то ни другое не подходит. По названию?      - 3  |
|  Совсем тяжело с выбором - будем искать по описанию.     - 4  |
|  А если скомбинируем? По категории и году?               - 5  |
|  Экспериментальная графическая оболочка                  - 6  |
|  Хочешь выйти?                                           - 0  |
+---------------------------------------------------------------+\n""")
    flag = True
    try:
        while flag:
            print(query_color + "\nНу, выбирай! Смелее! Итак, твой выбор: ")
            choice = int(input())
            if choice not in range(0, 7):
                print(info_color + "\nВыбрать можно только числа от 0 до 6, повтори выбор\n")
                break
            elif choice == 0:
                parting()
            elif choice == 1:
                print(info_color + "\nВыбор сделан - открываю список категорий\n")
            elif choice == 2:
                print(info_color + "\nВыбираем по дате? Отлично!\n")
            elif choice == 3:
                print(info_color + "\nБудем искать по названию\n")
            elif choice == 4:
                print(info_color + """\nТяжелый случай... Но нет ничего невозможного, 
ищем по части слова в названии или описании\n""")
            elif choice == 5:
                print(info_color + "\nДавай пустим в ход тяжелую артиллерию? \n")
            elif choice == 6:
                logic.find_with_window()
            else:
                parting()
            return choice
    except ValueError:
        print(error_color + "\nВводить можно только числа. Ну ладно, выберем по категории\n")
        return 1


def exit_program(cursor, conn):
    """ Выход из БД и разрыв соединения """
    cursor.close()
    disconnect_from_db(conn)


def show(cursor):
    """ Просто выводит выборку на экран"""
    print(from_db_cursor(cursor))


def into_statistics(value):
    try:
        dbconfig = read_config('project_220424_ptm_Alexander_Tutubalin')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "INSERT INTO statistics (user_request) VALUES(%s);"
        args = value
        cursor.execute(query, args)
        conn.commit()

    except Error as err:
        print(error_color + f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        exit_program(cursor, conn)


def request_statistics():
    """ Выдает популярные запросы прошлых поисков пользователя. Информация ДСП!"""
    try:
        dbconfig = read_config('project_220424_ptm_Alexander_Tutubalin')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = """select * from
(select user_request as Запросы, count(*) as counter 
from statistics
group by user_request) as t1
where counter > 1
order by counter DESC
LIMIT 5
;"""
        cursor.execute(query)
        show(cursor)
        print(info_color + "Подробнее надо? Могу предоставить полную информацию о запросах: еще раз 01")
        ask = input()
        if ask == "01":
            query = "SELECT user_request as Запросы FROM statistics"
            cursor.execute(query)
            show(cursor)
        exit_program(cursor, conn)

    except Error as err:
        print(error_color + "Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        exit_program(cursor, conn)


def main_program():
    """Это главный модуль. Он для запуска и связки с остальными модулями"""
    try:
        titel_screen.start_screen()
        dbconfig = read_config('sakila')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        choice = choice_select()

        parameter = 0
        if choice == 1:
            cursor.execute(choose_category())
            show(cursor)
            parameter = search_by_category()
        elif choice == 2:
            parameter = search_by_year()
        elif choice == 3:
            parameter = search_by_title()
        elif choice == 4:
            parameter = search_by_description()
        elif choice == 5:
            cursor.execute(choose_category())
            show(cursor)
            category = search_by_category()
            if category != 0:
                year = search_by_year()
                if year != 0:
                    parameter = [category, year]
        else:
            choice = 0
            exit_program(cursor, conn)
        if parameter != 0:
            query, statistic = query_constructor(choice, parameter)
            cursor.execute(query)
            show(cursor)
            exit_program(cursor, conn)
            into_statistics((statistic,))
    except Error as err:
        print(error_color + f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        exit_program(cursor, conn)


if __name__ == '__main__':
    main_program()
    while True:
        print(title_color + f"""\nОднако программа будет выполняться до тех пор, пока не будет
введено 00 для выхода (2 нуля)! Хочешь выйти?  Нажми 00. Все 
остальное запустит программу по-новой! Итак, твой выбор?: """)
        exit_cond = input()
        if exit_cond == '00':
            print(info_color + "\nЭто точно твое окончательное решение? Ну что ж, очень жаль...\n")
            print(text_color + "До свидания! И до новых встреч!")
            break
        elif exit_cond == '01':
            print(error_color + "Это тайная информация! Слежка за популярными запросами пользователя!")
            request_statistics()
        else:
            main_program()
