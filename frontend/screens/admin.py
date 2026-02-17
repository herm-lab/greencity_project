import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App

# Добавляем путь к папке frontend в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(frontend_dir)

from api_client import create_user

Builder.load_string('''
<AdminScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Админ-панель'
            font_size: 24
            size_hint_y: None
            height: 50

        TextInput:
            id: name_input
            hint_text: 'Имя ученика'
            size_hint_y: None
            height: 50

        TextInput:
            id: class_input
            hint_text: 'Класс/группа'
            size_hint_y: None
            height: 50

        Button:
            text: 'Создать аккаунт'
            size_hint_y: None
            height: 50
            on_press: root.create_account()

        Button:
            text: 'Управление пользователями'
            size_hint_y: None
            height: 50
            on_press: root.show_user_management()

        Button:
            text: 'Назад'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'home'
''')


class AdminScreen(Screen):
    def create_account(self):
        name = self.ids.name_input.text.strip()
        class_info = self.ids.class_input.text.strip()

        if not name or not class_info:
            self.show_message("Заполните все поля", "Ошибка")
            return

        response = create_user(name, class_info)

        if 'code' in response:
            self.show_message(
                f"Аккаунт создан!\nКод: {response['code']}",
                "Успех"
            )
            self.ids.name_input.text = ""
            self.ids.class_input.text = ""
        else:
            error = response.get('error', 'Неизвестная ошибка')
            self.show_message(f"Ошибка: {error}", "Ошибка создания")

    def show_user_management(self):
        self.manager.current = 'user_management'

    def show_message(self, message, title=""):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.5)
        )
        popup.open()


class AdminApp(App):
    def build(self):
        from kivy.uix.screenmanager import ScreenManager
        from screens.user_management import UserManagementScreen

        sm = ScreenManager()
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(UserManagementScreen(name='user_management'))
        return sm


if __name__ == '__main__':
    AdminApp().run()