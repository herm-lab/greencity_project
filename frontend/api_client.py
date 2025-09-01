import requests
from requests.exceptions import RequestException
import os
import sys

# Добавляем путь к backend для тестирования
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..', 'backend'))
sys.path.append(backend_dir)

BASE_URL = "http://localhost:5001/api"

def create_user(name, class_info):
    try:
        response = requests.post(
            f"{BASE_URL}/create-user",
            json={'name': name, 'classInfo': class_info},
            timeout=5
        )
        return response.json()
    except RequestException as e:
        return {'error': str(e)}

def check_user(code):
    try:
        print(f"DEBUG: Отправка запроса для кода: {code}")
        response = requests.post(
            f"{BASE_URL}/check-user",
            json={'code': code},
            timeout=5
        )
        print(f"DEBUG: Ответ сервера: {response.status_code}, {response.text}")
        result = response.json().get('exists', False)
        print(f"DEBUG: Результат проверки: {result}")
        return result
    except RequestException as e:
        print(f"DEBUG: Ошибка соединения: {str(e)}")
        return False
    except Exception as e:
        print(f"DEBUG: Неожиданная ошибка: {str(e)}")
        return False

def delete_user(code):
    try:
        response = requests.delete(
            f"{BASE_URL}/delete-user/{code}",
            timeout=5
        )
        return response.json()
    except RequestException as e:
        return {'error': str(e)}

def get_all_users():
    try:
        response = requests.get(f"{BASE_URL}/get-all-users", timeout=5)
        return response.json()
    except RequestException as e:
        return {'error': str(e)}

def get_user_stats(code):
    """Получает статистику пользователя"""
    try:
        response = requests.get(
            f"{BASE_URL}/user-stats/{code}",
            timeout=5
        )
        return response.json()
    except RequestException as e:
        print(f"[API ERROR] get_user_stats: {str(e)}")
        return {'error': str(e)}

def add_waste(user_code, waste_type, amount):
    try:
        response = requests.post(
            f"{BASE_URL}/add-waste",
            json={
                'userCode': user_code,
                'type': waste_type.lower(),  # Отправляем русские названия в нижнем регистре
                'amount': amount
            },
            timeout=5
        )
        return response.json()
    except RequestException as e:
        return {'error': str(e)}