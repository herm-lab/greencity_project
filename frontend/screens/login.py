import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Правильный импорт api_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import check_user

Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'GreenCity - Вход'
            font_size: 24

        TextInput:
            id: code_input
            hint_text: 'Ваш код (A12345)'
            multiline: False
            font_size: 18
            size_hint_y: None
            height: 50
            input_filter: lambda text, from_undo: text.upper() if len(text) == 1 else (text if text.isdigit() else '')

        Button:
            text: 'Войти'
            size_hint_y: None
            height: 50
            on_press: root.login()
''')

class LoginScreen(Screen):
    def login(self):
        code = self.ids.code_input.text
        if not self.validate_code(code):
            self.show_error("Неверный формат кода! Пример: A12345")
            return

        if check_user(code):
            # Сохраняем код пользователя в самом экране логина
            self.user_code = code.upper()
            self.manager.current = 'home'
            # Передаем код в home screen
            self.manager.get_screen('home').user_code = self.user_code
        else:
            self.show_error("Пользователь не найден")

    def validate_code(self, code):
        return (len(code) == 6
                and code[0].isupper()
                and code[0].isalpha()
                and code[1:].isdigit())

    def show_error(self, message):
        Popup(title='Ошибка',
              content=Label(text=message),
              size_hint=(0.8, 0.4)).open()