import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_user_stats

Builder.load_string('''
<ProfileScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Мой профиль'
            font_size: 24

        Label:
            id: user_info
            font_size: 18

        BoxLayout:
            orientation: 'vertical'
            spacing: 10

            Label:
                text: 'Статистика:'
                font_size: 18

            Label:
                id: stats_info

        Button:
            text: 'Назад'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'home'
''')


class ProfileScreen(Screen):
    def on_pre_enter(self):
        stats = get_user_stats(self.manager.get_screen('home').user_code)
        if 'error' in stats:
            self.show_error(stats['error'])
            return

        self.ids.user_info.text = f"{stats['name']}, {stats['classInfo']}"

        stats_text = [
            f"Крышки: {stats['waste']['lids']} шт",
            f"Пластик: {stats['waste']['plastic']} шт",
            f"Батарейки: {stats['waste']['batteries']} шт",
            f"\nВсего баллов: {stats.get('total_points', 0)}"
        ]

        self.ids.stats_info.text = '\n'.join(stats_text)

    def show_error(self, message):
        Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        ).open()