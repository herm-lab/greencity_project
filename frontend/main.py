import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


#root dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screens.user_management import UserManagementScreen
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.profile import ProfileScreen
from screens.admin import AdminScreen


class GreenCityApp(App):
    def build(self):
        sm = ScreenManager()

        # Создаем экраны
        login_screen = LoginScreen(name='login')
        home_screen = HomeScreen(name='home')
        profile_screen = ProfileScreen(name='profile')
        admin_screen = AdminScreen(name='admin')

        # Добавляем экраны
        sm.add_widget(login_screen)
        sm.add_widget(home_screen)
        sm.add_widget(profile_screen)
        sm.add_widget(admin_screen)

        return sm

if __name__ == '__main__':
    GreenCityApp().run()