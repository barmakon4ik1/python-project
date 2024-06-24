import configparser
from mysql.connector import MySQLConnection, Error
from prettytable import from_db_cursor, PrettyTable


def read_config(section):
    """
    Чтение файла конфигурации config.ini и возвращение словаря с данными для подключения к БД
    """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        host = config.get(section, 'host')
        user = config.get(section, 'username')
        password = config.get(section, 'password')
        database = config.get(section, 'database')
        dbconfig = {'host': host, 'user': user, 'password': password, 'database': database}
        # print(f"Соединение с базой данных {database} установлено")
        return dbconfig
    except Exception as err:
        print(f"Ошибка при подключении к базе данных: \b{err}")


def disconnect_from_db(conn):
    """
    Модуль закрытия подключения к БД.
    Разрывает соединение и закрывает его.
    """
    conn.close()


def parting():
    """ Просто прощание """
    print("\nНу что ж, выход - так выход. Будем ждать твоего возвращения!\n")
    print(f"""                       |\\__/,|   (`\\
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
        print(f"Ошибка при составлении запроса: {err}")


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
        where = f"WHERE film.description LIKE '%{value}%'"
    elif choice == 5:
        select = f"SELECT DISTINCT {release_year}, {title} "
        where = f'WHERE category.category_id = {value[0]} AND film.release_year {value[1]}'
    else:
        print("Непостижимо! Как ты сюда попал? ")
    return select, where


def search_by_title():
    """ Модуль поиска по названию """
    print("+---------------------------------------------------------------+")
    print("| Будем искать по буквам в названии фильма.                     |")
    print("| Предупреждаю, это почти самый сложный выбор!                  |")
    print("| Потому что нужно ввести что то из названия фильма.            |")
    print("| Или не вводи ничего и тогда программа будет закрыта           |")
    print("+---------------------------------------------------------------+")
    title = input("\nВведи полное название фильма, можно в любом регистре: \n").upper()
    if title == "":
        parting()
        return 0
    else:
        return title


def search_by_description():
    """ Модуль поиска по частям описания """
    print("+---------------------------------------------------------------+")
    print("| Наконец, самый сложный и непредсказуемый метод!               |")
    print("| Он позволяет искать по словам, буквам в описании фильма,      |")
    print("| чем больше запрос, тем точнее выбор.                          |")
    print("| Ну или не вводи ничего и тогда программа будет закрыта        |")
    print("+---------------------------------------------------------------+")
    description_tail = input("""\nВведи что то из внятных слов и мы поищем, что подойдет: \n""")
    if description_tail == "":
        parting()
        return 0
    else:
        return description_tail


def search_by_year():
    """ Поиск по году выпуска фильма """
    print("+---------------------------------------------------------------+")
    print("| Будем искать по году выпуска фильма в свет:                   |")
    print("|                           точное совпадение              - 1  |")
    print("|                           ранее чем вводимый год         - 2  |")
    print("|                           позднее, чем выбранный год     - 3  |")
    print("| Просто выйти отсюда жми все, что угодно                       |")
    print("+---------------------------------------------------------------+")
    try:
        choice = input("\nТвой выбор: ")
        if choice in ["1", "2", "3"]:
            year = int(input("\nТеперь введи желаемый год: "))
        if choice == "1":
            return f"= {year}"
        elif choice == "2":
            return f"<= {year}"
        elif choice == "3":
            return f">= {year}"
        else:
            parting()
            return 0
    except Exception as e:
        print(f"Таких фильмов не нашлось, сожалею...")


def order_by_field():
    """ сортировка результата """
    print("\nПо какому критерию будем сортировать результат?\n")
    print("+---------------------------------------------------------------+")
    print("| Сортировка по названию фильма в алфавитном порядке    -   1   |")
    print("| или по дате выхода на экран от старого к новому       -   2   |")
    print("| если интересуют сперва новее, отсортируем наоборот    -   3   |")
    print("| если сортировка нам 'по барабану', жми что хочешь             |")
    print("+---------------------------------------------------------------+")
    try:
        point = input("\nВыбирайте сортировку: ")
        if point == "1":
            return f"ORDER BY film.title\n"
        elif point == "2":
            return f"ORDER BY film.release_year\n"
        elif point == "3":
            return f"ORDER BY film.release_year DESC\n"
        else:
            return f"\n"
    except Exception as e:
        print(f"Произошла ошибка! {e}")


def choice_limit():
    """ ограничение на показ выборки """
    value = input("\nСколько названий фильмов вывести на экран? Если не укажешь - выведу все: ")
    if value.isdigit() and int(value) > 0:
        print(f"\nТы ввел ограничение в количестве не более {value} названий:")
        return f"LIMIT {value}"
    else:
        print("\nОграничений не указано - будут выведены все результаты!\n")
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
                choice = int(input("\nВведите номер категории или 0 для отмены и выхода: "))
                if choice == 0:
                    parting()
                    return 0
                elif choice < 1 or choice > 16:
                    print("К сожалению, такой категории у нас нет, выбери по-новой")
                    flag = True
                else:
                    return choice
            except ValueError:
                print(f"Вводить можно только число от 0 до 16. Повторим выбор")
                flag = True
    except Exception as e:
        print(f"Произошла ошибка! {e}")


def choice_select():
    """ Модуль выбора по критериям. Отсюда стартует разветвление по выборке"""
    print("+---------------------------------------------------------------+")
    print("|  Сперва нужно выбрать по каким критериям будем отбирать:      |")
    print("|  Наверное сначала определимся с категорией фильма?        - 1 |")
    print("|  Или лучше отберем фильмы по дате выхода в свет?          - 2 |")
    print("|  Понимаю, ни то ни другое не подходит. По названию?       - 3 |")
    print("|  Совсем тяжело с выбором - будем искать по описанию.      - 4 |")
    print("|  А если скомбинируем? По категории и году?                - 5 |")
    print("|  Хочешь выйти?                                            - 0 |")
    print("+---------------------------------------------------------------+\n")
    flag = True
    try:
        while flag:
            choice = int(input("Ну, выбирай. Смелее. Итак, наш выбор: "))
            if choice == 0:
                parting()
                flag = False
            elif choice == 1:
                print("\nВыбор сделан - открываю список категорий\n")
                flag = False
            elif choice == 2:
                print("\nВыбираем по дате? Отлично!\n")
                flag = False
            elif choice == 3:
                print("\nБудем искать по названию\n")
                flag = False
            elif choice == 4:
                print("\nТяжелый случай... Но нет ничего невозможного, ищем по части слова в названии или описании\n")
                flag = False
            elif choice == 5:
                print("\nДавай пустим в ход тяжелую артиллерию? \n")
                flag = False
            else:
                print("\nВыбрать можно только числа от 0 до 5, повтори выбор\n")
            return choice
    except ValueError:
        print("\nВводить можно только числа. Ну ладно, выберем по категории\n")
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

        # Строки для проверки добавления индекса в БД запросов:
        # if cursor.lastrowid:
        #     print('Последний добавленный индекс id ', cursor.lastrowid)
        # else:
        #     print('Последний добавленный индекс id не найден')

        conn.commit()

    except Error as err:
        print(f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")

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
;"""
        cursor.execute(query)
        show(cursor)
        print("Подробнее надо? Могу предоставить полную информацию о запросах: еще раз 01")
        ask = input()
        if ask == "01":
            query = "SELECT user_request as Запросы FROM statistics"
            cursor.execute(query)
            show(cursor)
        exit_program(cursor, conn)

    except Error as err:
        print(f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        exit_program(cursor, conn)


def main_program():
    """Это главный модуль. Он для запуска и связки с остальными модулями"""
    print("+---------------------------------------------------------------+")
    print("|  Привет! Рады видеть тебя на нашем портале!                   |")
    print("|  Хочешь провести вечер за просмотром хорошего фильма?         |")
    print("|  Но не знаешь что посмотреть? Ты правильно пришел к нам,      |")
    print("|  потому что у нас самая большая база для выбора фильмов       |")
    print("|  Начнем?     +-----------------------+                        |")
    print("|              |       /\\_/\\           |                        |")
    print("|              |      (>°.°<)  |       |                        |")
    print("|              |       (\")(\")_/        |                        |")
    print("|              |   КИНОПОИСК МЯУ-МЯУ   |                        |")
    print("|              +-----------------------+                        |")
    print("|                                                               |")
    print("|    /^--^\\     /^--^\\     /^--^\\     /^--^\\     /^--^\\         |")
    print("|    \\____/     \\____/     \\____/     \\____/     \\____/         |")
    print("|   /      \\   /      \\   /      \\   /      \\   /      \\        |")
    print("|  |        | |        | |        | |        | |        |       |")
    print("|   \\__  __/   \\__  __/   \\__  __/   \\__  __/   \\__  __/        |")
    print("|^ ^ ^ \\ \\^ ^ ^ ^/ /^ ^ ^ ^ ^\\ \\^ ^ ^ ^ \\ \\^ ^ ^ ^/ /^ ^ ^ ^ ^ ^|")
    print("|###### \\#\\#####/ /###########\\#\\########\\#\\#####/ /############|")
    print("| | | | / / | | \\ \\| | | | | |/ /| | | | / /| | |\\ \\| | | | | | |")
    print("| | | | \\/| | | |\\/| | | | | |\\/ | | | | \\/ | | | \\/| | | | | | |")
    print("#################################################################")
    print("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |")
    print("| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |")
    print("+---------------------------------------------------------------+\n")
    try:
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
            exit_program(cursor, conn)

        if parameter != 0:
            query, statistic = query_constructor(choice, parameter)
            cursor.execute(query)
            show(cursor)
            exit_program(cursor, conn)
            into_statistics((statistic,))
    except Error as err:
        print(f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        exit_program(cursor, conn)


if __name__ == '__main__':
    main_program()
    while True:
        print("\nОднако программа будет выполняться до тех пор, пока не будет введено 00 для выхода (2 нуля)!")
        exit_cond = input("Хочешь выйти? Нажми 00. Все остальное запустит программу по-новой. Твой выбор?: \n")
        if exit_cond == '00':
            print("\nЭто точно твое окончательное решение? Ну что ж, очень жаль...\n")
            print("До свидания! И до новых встреч!")
            break
        elif exit_cond == '01':
            print("Это тайная информация! Слежка за популярными запросами пользователя!")
            request_statistics()
        else:
            main_program()
