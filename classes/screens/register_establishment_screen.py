from classes.establishment import Establishment
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivy.core.window import Window
from kivy.metrics import dp


class Item(OneLineListItem):
    pass


class RegisterEstablishmentScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()
        self.default_delivery_value = "0.00"
        self.default_increment_value = "0.50"

    def on_pre_enter(self, *args):
        self.__app.screen_manager.get_screen("delivery_screen").ids.delivery_value.text = self.default_delivery_value
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "delivery_screen"
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.back)

    def decrease_delivery_value(self, current):
        text_field = self.ids.delivery_value
        try:
            float(current)
        except (ValueError, TypeError):
            text_field.text = self.default_delivery_value
        else:
            if float(current) - float(self.default_increment_value) >= 0:
                text_field.text = f"{float(current) - float(self.default_increment_value):.2f}"

    def increase_delivery_value(self, current):
        text_field = self.ids.delivery_value
        try:
            float(current)
        except (ValueError, TypeError):
            text_field.text = self.default_delivery_value
        else:
            text_field.text = f"{float(current) + float(self.default_increment_value):.2f}"

    def add_establishment(self, establishment_name, default_delivery_value):
        if not establishment_name:
            self.__app.show_toast_msg("Informe o nome do estabelecimento!")
            return False
        if default_delivery_value == "":
            default_delivery_value = 0.0
        self.reset_form()
        establishment = Establishment(establishment_name.title(), default_delivery_value)
        if self.__app.firebase_manager.establishment_exists(establishment):
            self.__app.show_toast_msg(f"'{establishment.name}' ja foi registrado!")
        else:
            self.__app.firebase_manager.register_establishment(establishment)
            self.__app.show_toast_msg(f"'{establishment.name}' registrado com sucesso!")
        self.reset_form()
        return True

    def reset_form(self):
        self.ids.establishment_name.text = ""
        self.ids.delivery_value.text = self.default_delivery_value
