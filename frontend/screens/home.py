import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Настройка путей импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import add_waste

Builder.load_string('''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Сдать вторсырье'
            font_size: 24
            size_hint_y: None
            height: 50

        Spinner:
            id: waste_type
            text: 'Выберите тип'
            values: ['Крышки', 'Пластик', 'Батарейки']
            size_hint_y: None
            height: 50

        TextInput:
            id: amount
            hint_text: 'Количество (кг)'
            input_filter: 'int'
            size_hint_y: None
            height: 50

        Button:
            text: 'Добавить'
            size_hint_y: None
            height: 50
            on_press: root.add_waste()

        Button:
            text: 'Мой профиль'
            size_hint_y: None
            height: 50
            on_press: root.go_to_profile()
''')


class HomeScreen(Screen):
    def add_waste(self):
        """Добавление вторсырья"""
        waste_type = self.ids.waste_type.text.lower()  # Приводим к нижнему регистру
        amount = self.ids.amount.text

        if waste_type == 'выберите тип':
            self.show_message('Выберите тип вторсырья')
            return

        if not amount.isdigit() or int(amount) <= 0:
            self.show_message('Введите корректное количество')
            return

        # Получаем код пользователя
        user_code = self.manager.get_screen('login').user_code

        # Отправляем русские названия как есть
        result = add_waste(user_code, waste_type, int(amount))

        if result.get('success'):
            self.show_message(f"Добавлено: {amount} кг {waste_type}")
            self.ids.amount.text = ''
            self.ids.waste_type.text = 'Выберите тип'
        else:
            self.show_message(f"Ошибка: {result.get('error', 'Неизвестная ошибка')}")


    def go_to_profile(self):
        """Переход в профиль"""
        self.manager.current = 'profile'


    def show_message(self, message):
        """Показ всплывающего уведомления"""
        Popup(
            title='Уведомление',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        ).open()