from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window


class InDevelopmentScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "delivery_screen"
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.back)
