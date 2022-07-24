from classes.user import User
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivyauth.google_auth import login_google, logout_google


class LoginScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()

    def on_pre_leave(self, *args):
        if not self.ids.remember_login_switch.active:
            self.reset_form()

    def do_login(self, switch, email, password):
        user = self.__app.firebase_manager.login_user(email, password)
        if user is not None:
            user_name = email.split("@")[0]
            if switch.active:
                self.__app.credentials.put("login",
                                           username=email,
                                           password=password)
                self.__app.saved_email = email
                self.__app.saved_password = password
            else:
                self.__app.credentials.put("login",
                                           username="",
                                           password="")
            self.__app.logged_in_user = User(email,
                                             user_name,
                                             self.__app.firebase_manager.get_user_data(user_name, email))
            self.__app.show_toast_msg(f"Bem vindo(a), {self.__app.logged_in_user.name}!")
            self.manager.current = "delivery_screen"
            return True
        return False

    @staticmethod
    def do_google_login():
        login_google()

    def reset_form(self):
        self.ids.username_text_field.text = ""
        self.ids.password_text_field.text = ""



