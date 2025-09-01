import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

# Правильная настройка путей импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(frontend_dir)

from api_client import get_all_users, delete_user  # Теперь импорт будет работать

Builder.load_string('''
<UserRow>:
    orientation: 'horizontal'
    spacing: 10
    size_hint_y: None
    height: 50
    padding: 10

    Label:
        text: root.user_text
        size_hint_x: 0.7
        font_size: 16
        halign: 'left'
        valign: 'middle'
        text_size: self.width, None

    Button:
        text: 'Удалить'
        size_hint_x: 0.3
        on_press: root.delete_user()

<UserManagementScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Управление пользователями'
            font_size: 24
            size_hint_y: None
            height: 50

        ScrollView:
            GridLayout:
                id: users_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 10

        Button:
            text: 'Обновить список'
            size_hint_y: None
            height: 50
            on_press: root.load_users()

        Button:
            text: 'Назад'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'admin'
''')


class UserRow(BoxLayout):
    user_text = StringProperty('')
    user_code = StringProperty('')

    def delete_user(self):
        if delete_user(self.user_code).get('success'):
            self.parent.remove_widget(self)


class UserManagementScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_users()

    def load_users(self):
        users_container = self.ids.users_container
        users_container.clear_widgets()

        users = get_all_users()
        if isinstance(users, list):
            for user in users:
                row = UserRow()
                row.user_text = f"{user['name']} ({user['class']}) | Код: {user['code']}"
                row.user_code = user['code']
                users_container.add_widget(row)
        else:
            self.show_message("Ошибка загрузки пользователей", "Ошибка")

    def show_message(self, message, title=""):
        Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        ).open()


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager


    class TestApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(UserManagementScreen(name='user_management'))
            return sm


    TestApp().run()