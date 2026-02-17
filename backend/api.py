from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import re
import random
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

# Правильная инициализация пути к базе данных
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    code = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_info = db.Column(db.String(50), nullable=False)
    lids = db.Column(db.Integer, default=0)        # Крышки
    plastic = db.Column(db.Integer, default=0)     # Пластик
    batteries = db.Column(db.Integer, default=0)   # Батарейки

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'classInfo': self.class_info,
            'waste': {
                'lids': self.lids,
                'plastic': self.plastic,
                'batteries': self.batteries
            }
        }


# Путь к файлу users.txt
USERS_FILE = os.path.join(basedir, 'users.txt')


def write_to_log(action, data):
    """Записывает действие в лог-файл"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {action}: {data}\n"

    with open(USERS_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def init_db():
    """Инициализация базы данных с тестовыми данными"""
    with app.app_context():
        db.create_all()

        # Проверяем соединение с базой
        try:
            test_result = db.session.execute(text('SELECT 1')).scalar()  # Исправлено здесь
            print(f"Подключение к базе успешно: {test_result}")
        except Exception as e:
            print(f"Ошибка подключения к базе: {e}")
            return

        # Проверяем существующие данные
        user_count = User.query.count()
        print(f"Найдено пользователей в базе: {user_count}")

        # Добавляем тестовых пользователей только если база пустая
        if user_count == 0:
            print("Добавляем тестовых пользователей...")
            test_users = [
                User(code='A12345', name='Иван Иванов', class_info='8А', lids=5, plastic=3, batteries=2),
                User(code='B54321', name='Мария Петрова', class_info='9Б', lids=3, plastic=4, batteries=1)
            ]
            db.session.bulk_save_objects(test_users)
            db.session.commit()
            print("Тестовые пользователи добавлены!")

        # Показываем всех пользователей
        users = User.query.all()
        print("Список пользователей в базе:")
        for user in users:
            print(f"  {user.code}: {user.name} ({user.class_info})")


@app.route('/api/check-user', methods=['POST'])
def check_user():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'Требуется код пользователя'}), 400

    code = data['code'].upper()
    print(f"DEBUG: Проверка пользователя с кодом: {code}")

    # Проверка формата
    if not re.match(r'^[A-Z]\d{5}$', code):
        print(f"DEBUG: Неверный формат кода: {code}")
        return jsonify({'exists': False})

    # Проверка существования в базе
    user = User.query.get(code)
    exists = user is not None

    print(f"DEBUG: Пользователь {code} существует: {exists}")
    if exists:
        print(f"DEBUG: Данные пользователя: {user.name}, {user.class_info}")

    return jsonify({'exists': exists})


@app.route('/api/user-stats/<code>', methods=['GET'])
def get_user_stats(code):
    user = User.query.get(code.upper())
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    return jsonify(user.to_dict())


@app.route('/api/add-waste', methods=['POST'])
def add_waste():
    data = request.get_json()
    if not all(field in data for field in ['userCode', 'type', 'amount']):
        return jsonify({'error': 'Не хватает данных'}), 400

    waste_type = data['type']
    # Принимаем русские названия
    if waste_type not in ['крышки', 'пластик', 'батарейки']:
        return jsonify({'error': 'Неверный тип вторсырья'}), 400

    user = User.query.get(data['userCode'].upper())
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    try:
        amount = int(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Количество должно быть положительным'}), 400
    except ValueError:
        return jsonify({'error': 'Количество должно быть числом'}), 400

    # Обновляем соответствующие поля в БД
    if waste_type == 'крышки':
        user.lids += amount
    elif waste_type == 'пластик':
        user.plastic += amount
    elif waste_type == 'батарейки':
        user.batteries += amount

    db.session.commit()

    return jsonify({'success': True, 'newCount': getattr(user,
                                                         'lids' if waste_type == 'крышки' else
                                                         'plastic' if waste_type == 'пластик' else
                                                         'batteries')})


@app.route('/api/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'classInfo' not in data:
        return jsonify({'error': 'Необходимы имя и класс'}), 400

    # Генерация кода
    letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    new_code = f"{letter}{numbers}"

    new_user = User(
        code=new_code,
        name=data['name'],
        class_info=data['classInfo'],
        lids=0,
        plastic=0,
        batteries=0
    )

    db.session.add(new_user)
    db.session.commit()

    # Логирование
    user_data = f"Код: {new_code}, Имя: {data['name']}, Класс: {data['classInfo']}"
    write_to_log('СОЗДАНИЕ', user_data)

    return jsonify({
        'code': new_code,
        'success': True
    })


@app.route('/api/delete-user/<code>', methods=['DELETE'])
def delete_user(code):
    user = User.query.get(code.upper())
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Сохраняем данные перед удалением
    user_data = f"Код: {user.code}, Имя: {user.name}, Класс: {user.class_info}"

    db.session.delete(user)
    db.session.commit()

    # Логирование
    write_to_log('УДАЛЕНИЕ', user_data)

    return jsonify({
        'success': True,
        'deleted_user': user_data
    })


@app.route('/api/get-all-users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'code': u.code,
        'name': u.name,
        'class': u.class_info,
        'lids': u.lids,
        'plastic': u.plastic,
        'batteries': u.batteries
    } for u in users])


if __name__ == '__main__':
    init_db()

    app.run(debug=True, port=5001, host='0.0.0.0')