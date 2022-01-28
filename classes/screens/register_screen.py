from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window


class RegisterScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()

    def on_pre_enter(self, *args):
        self.reset_form()
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "login_screen"
            return True

    def on_pre_leave(self, *args):
        self.reset_form()
        Window.unbind(on_keyboard=self.back)

    def do_register(self, email, password, confirm_password):
        if any(map(lambda arg: not arg, (email, password, confirm_password))):
            self.__app.show_toast_msg("Preencha todos os campos!")
            return False
        if len(password) < 6:
            self.__app.show_toast_msg("Senha deve ter ao menos 6 caracteres!")
            return False
        if password != confirm_password:
            self.__app.show_toast_msg("Senhas não conferem!")
            return False
        register_result = self.__app.firebase_manager.register_user(email, password)
        if register_result:
            self.__app.show_toast_msg("Registrado com sucesso!")
            self.reset_form()
            self.manager.current = "login_screen"
        return True

    def reset_form(self):
        self.ids.email_text_field.text = ""
        self.ids.password_text_field.text = ""
        self.ids.confirm_password_text_field.text = ""
