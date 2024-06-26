import configparser
from mysql.connector import MySQLConnection, Error
import fs
from prettytable import from_db_cursor


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
        return dbconfig
    except Exception as err:
        print(f"Ошибка при подключении к базе данных: \b{err}")


def disconnect_from_db(conn):
    """ Модуль закрытия подключения к БД.Разрывает соединение и закрывает его."""
    conn.close()


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
        print(f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")
    finally:
        exit_program(cursor, conn)


def request_statistics():
    """ Выдает популярные запросы прошлых поисков пользователя. Информация ДСП!"""
    try:
        dbconfig = read_config('project_220424_ptm_Alexander_Tutubalin')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = """SELECT * FROM
(SELECT user_request AS Запросы, count(*) AS Счетчик 
FROM statistics
GROUP BY user_request) AS t1
WHERE counter > 1
ORDER BY counter DESC
LIMIT 5
;"""
        cursor.execute(query)
        show(cursor)
        exit_program(cursor, conn)

    except Error as err:
        print("Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        exit_program(cursor, conn)


def sql_constructor(category, year_start, year_end, title, description):
    str_cat = f" category.name = '{category}' " if category else None
    if year_start and not year_end:
        str_year = f" film.release_year >= '{year_start}' "
    elif year_end and not year_start:
        str_year = f" film.release_year <= '{year_end}' "
    elif year_start and year_end:
        if year_start > year_end:
            year_start, year_end = year_end, year_start
        str_year = f"film.release_year BETWEEN '{year_start}' AND '{year_end}' "
    else:
        str_year = ""
    str_title = f" film.title LIKE '%{title}%' " if title else None
    str_desc = f" film.description LIKE '%{description}%' " if description else None
    sql = [str_cat, str_year, str_title, str_desc]
    return sql


def where_constructor(sql):
    str_cat, str_year, str_title, str_desc = sql
    """ Конструктор специальных запросов и условий """
    if str_cat:
        if str_year:
            if str_title:
                return f"WHERE {str_cat} AND {str_year} AND {str_title} AND {str_desc}" if str_desc else \
                    f"WHERE {str_cat} AND {str_year} AND {str_title} "
            else:
                return f"WHERE {str_cat} AND {str_year} AND {str_desc}" if str_desc else \
                    f"WHERE {str_cat} AND {str_year} "
        else:
            if str_title:
                return f"WHERE {str_cat} AND {str_title} AND {str_desc}" if str_desc else \
                    f"WHERE {str_cat} AND {str_title} "
            else:
                return f"WHERE {str_cat} AND {str_desc}" if str_desc else f"WHERE {str_cat} "
    else:
        if str_year:
            if str_title:
                return f"WHERE {str_year} AND {str_title} AND {str_desc}" if str_desc else \
                    f"WHERE {str_year} AND {str_title} "
            else:
                return f"WHERE {str_year} AND {str_desc}" if str_desc else f"WHERE {str_year} "
        else:
            if str_title:
                return f"WHERE {str_desc}" if str_desc else f"WHERE{str_title} "
            else:
                return f"WHERE {str_desc}" if str_desc else f""


def sort_constructor(sort):
    if sort == 'alphabetically':
        return f" ORDER BY film.title "
    elif sort == 'new_first':
        return f" ORDER BY film.release_year DESC "
    elif sort == 'old_first':
        return f" ORDER BY film.release_year ASC "
    else:
        return ""


def query_constructor(where, sort, qty):
    """ Конструктор запросов, принимает выбор критериев и выдает текст для запроса"""
    from_table = f"FROM film "
    join_tables = f"""JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    JOIN language ON language.language_id = film.language_id
    JOIN film_actor ON film.film_id = film_actor.film_id
    JOIN actor ON film_actor.actor_id = actor.actor_id """
    sort = sort_constructor(sort)
    limit = f" LIMIT {qty}" if qty else ""
    return f""" SELECT DISTINCT category.name AS Категория,
    film.title AS Название, film.release_year AS Год_выпуска,
    film.description AS Описание
    {from_table}
    {join_tables}
    {where}
    {sort}
    {limit};
    """


def find_with_window():
    """Это главный модуль. Он для запуска и связки с остальными модулями"""
    try:
        dbconfig = read_config('sakila')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        try:
            category, year_start, year_end, title, description, sort, qty = fs.main_window()
            where = where_constructor(sql_constructor(category, year_start, year_end, title, description))
            query = query_constructor(where, sort, qty)

            cursor.execute(query)
            show(cursor)
            cursor.close()
            disconnect_from_db(conn)
            into_statistics((query,))

        except Exception as e:
            pass
        finally:
            cursor.close()
            disconnect_from_db(conn)

    except Error as err:
        print(f"Соединение с базой данных разорвано ао неизвестной причине\n{err}")

    finally:
        cursor.close()
        disconnect_from_db(conn)


# if __name__ == '__main__':
#     find_with_window()



