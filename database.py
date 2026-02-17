"""
database.py - модуль для работы с базой данных пользователей
При запуске выводит всех пользователей из users.db
"""
import sqlite3
from pprint import pprint

# Путь к базе данных
DB_PATH = 'backend/users.db'


def get_all_users(db_path: str = DB_PATH) -> list:
    """
    Получает всех пользователей из базы данных
    Возвращает список словарей с данными пользователей
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users")
        # Получаем названия колонок
        columns = [col[0] for col in cursor.description]
        # Создаем список словарей
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return users
    finally:
        conn.close()


def print_all_users():
    """Выводит всех пользователей в удобном формате"""
    users = get_all_users()
    print("\nСписок всех пользователей:")
    print("-" * 50)
    for user in users:
        print(f"Код: {user['code']}")
        print(f"Имя: {user['name']}")
        print(f"Класс: {user['class_info']}")
        print(f"Показатели:")
        print(f"  - Крышки: {user['lids']}")
        print(f"  - Пластик: {user['plastic']}")
        print(f"  - Батарейки: {user['batteries']}")
        print("-" * 50)


if __name__ == '__main__':
    print_all_users()