"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os
import psycopg2


def get_data_from_csv(file_name):
    """Читает csv-файл и возвращает список словарей с данными"""
    dir_ = os.path.dirname(__file__)
    file_path = os.path.join(dir_, 'north_data\\' + file_name)
    with open(file_path, encoding='utf8') as file:
        data = list(csv.DictReader(file))
        return data


def fill_table(data, table, base):
    """Создает соединение с базой данных, заполняет ее,
    звкрывает соединение (закрытие курсора и коммит выполняется контекстным менеджером)"""
    connection = psycopg2.connect(host='localhost', database=base, user='postgres', password='12345')
    quantity = ", ".join(["%s"] * len(data[0]))
    try:
        with connection:
            with connection.cursor() as cursor:
                for dict_ in data:
                    cursor.execute(f'INSERT INTO {table} VALUES ({quantity})', tuple(dict_.values()))
                connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()


employees_list = get_data_from_csv('employees_data.csv')
customers_list = get_data_from_csv('customers_data.csv')
orders_list = get_data_from_csv('orders_data.csv')
base = 'north'
