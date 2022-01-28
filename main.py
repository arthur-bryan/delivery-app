from classes.firebase_manager import FirebaseManager
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from classes.screens.login_screen import LoginScreen
from classes.user import User
from classes.screens.register_screen import RegisterScreen
from classes.screens.delivery_screen import DeliveryScreen
from classes.screens.register_establishment_screen import RegisterEstablishmentScreen
from classes.screens.table_view_screen import TableViewScreen
from classes.screens.user_screen import UserScreen
from classes.screens.view_establishments_screen import ViewEstablishmentsScreen
from classes.screens.in_development_screen import InDevelopmentScreen
from kivy.uix.screenmanager import WipeTransition
from kivy.lang import Builder
from kivymd.toast import toast
from kivyauth.google_auth import initialize_google
from kivy.clock import mainthread
from os import path


CREDENTIALS_FILE = "credentials.json"
GOOGLE_CLIENT_ID = "910209521956-co8gl78jbm5cafl7idr1eu2n37b3ujmh.apps.googleusercontent.com"
GOOGLE_CLIENT_SCRET = "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"


class Manager(ScreenManager):

    def __init__(self):
        super().__init__(transition=WipeTransition())


class App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = Manager()
        self.firebase_manager = FirebaseManager()
        self.credentials = JsonStore(path.join(self.user_data_dir, CREDENTIALS_FILE))
        self.logged_in_user = None
        self.saved_email = ""
        self.saved_password = ""
        self.title_font_size = 38
        self.subtitle_font_size = 32
        self.default_font_size = 20
        self.small_font_size = 14
        self.default_font = "static/fonts/Righteous-Regular.ttf"

    def change_screen(self, target_screen):
        self.screen_manager.current = target_screen

    @staticmethod
    def show_toast_msg(message):
        toast(message)

    @mainthread
    def after_google_login(self, name, email, photo_uri):
        self.change_screen("delivery_screen")
        self.logged_in_user = User(email,
                                   name,
                                   self.firebase_manager.get_user_data(name, email))
        self.firebase_manager.register_user_in_realtime_database(name, email)
        self.show_toast_msg(f"Bem vindo, {name}!")

    def error_listener(self):
        self.show_toast_msg("Falha ao logar!")

    def build_config(self, config):
        try:
            self.credentials.get('login')['username']
        except KeyError:
            self.saved_email = ""
        else:
            self.saved_email = self.credentials.get('login')['username']

        try:
            self.credentials.get('login')['password']
        except KeyError:
            self.saved_password = ""
        else:
            self.saved_password = self.credentials.get('login')['password']

    def show_logged_user(self):
        self.show_toast_msg(self.logged_in_user.name)

    def build(self):
        initialize_google(self.after_google_login,
                          self.error_listener, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SCRET)
        self.icon = "static/images/icon.png"
        Builder.load_file("static/templates/in_development_screen.kv")
        Builder.load_file("static/templates/user_screen.kv")
        Builder.load_file("static/templates/view_establishments_screen.kv")
        Builder.load_file("static/templates/table_view_screen.kv")
        Builder.load_file("static/templates/register_establishment_screen.kv")
        Builder.load_file("static/templates/delivery_screen.kv")
        Builder.load_file("static/templates/register_screen.kv")
        Builder.load_file("static/templates/login_screen.kv")
        self.screen_manager.add_widget(LoginScreen(name="login_screen"))
        self.screen_manager.add_widget(RegisterScreen(name="register_screen"))
        self.screen_manager.add_widget(DeliveryScreen(name="delivery_screen"))
        self.screen_manager.add_widget(RegisterEstablishmentScreen(name="register_establishment_screen"))
        self.screen_manager.add_widget(TableViewScreen(name="table_view_screen"))
        self.screen_manager.add_widget(ViewEstablishmentsScreen(name="view_establishments_screen"))
        self.screen_manager.add_widget(UserScreen(name="user_screen"))
        self.screen_manager.add_widget(InDevelopmentScreen(name="in_development_screen"))
        return self.screen_manager


App().run()
