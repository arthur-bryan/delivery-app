from classes.delivery import Delivery
from classes.establishment import Establishment
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.core.window import Window
from kivy.metrics import dp


class Item(OneLineListItem):
    pass


class DeliveryScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()
        self.default_delivery_value = "4.00"
        self.default_increment_value = "0.50"
        self.delivery_categories = [
            {
                "text": "Comida",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Comida": self.dropdown_product_callback(x)
            },
            {
                "text": "Hamburguer",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Hamburguer": self.dropdown_product_callback(x)
            },
            {
                "text": "Pizza",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Pizza": self.dropdown_product_callback(x)
            },
            {
                "text": "Coxinha",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Coxinha": self.dropdown_product_callback(x)
            },
            {
                "text": "Lanche",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Lanche": self.dropdown_product_callback(x)
            },
            {
                "text": "Fruta",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Fruta": self.dropdown_product_callback(x)
            },
            {
                "text": "Bebida",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Bebida": self.dropdown_product_callback(x)
            },
            {
                "text": "Farmacia",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Farmacia": self.dropdown_product_callback(x)
            },
            {
                "text": "Vestimenta",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Vestimenta": self.dropdown_product_callback(x)
            },
            {
                "text": "Documento",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Documento": self.dropdown_product_callback(x)
            },
            {
                "text": "Mercado",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Mercado": self.dropdown_product_callback(x)
            },
            {
                "text": "Sorvete",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Sorvete": self.dropdown_product_callback(x)
            },
            {
                "text": "Eletronicos",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Eletronicos": self.dropdown_product_callback(x)
            },
            {
                "text": "Outro",
                "viewclass": "Item",
                "height": dp(40),
                "on_release": lambda x="Outro": self.dropdown_product_callback(x)
            }
        ]
        self.delivery_product_menu = MDDropdownMenu(
            caller=self.ids.delivery_product,
            items=self.delivery_categories,
            width_mult=4)

    def on_pre_enter(self, *args):
        self.fill_establishments()
        self.__app.screen_manager.get_screen("delivery_screen").ids.delivery_value.text = self.default_delivery_value
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "login_screen"
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.back)

    def fill_establishments(self):
        establishments = self.__app.firebase_manager.get_establishments()
        data = [{
            "text": establishment,
            "viewclass": "Item",
            "height": dp(40),
            "on_release": lambda x=establishment: self.dropdown_establishment_callback(x)
            } for establishment in establishments]
        self.establishments_menu = MDDropdownMenu(
            caller=self.ids.establishment,
            items=data,
            width_mult=4)

    def dropdown_product_callback(self, delivery_product):
        self.ids.delivery_product.text = delivery_product
        self.delivery_product_menu.dismiss()

    def dropdown_establishment_callback(self, delivery_product):
        self.ids.establishment.text = delivery_product
        self.establishments_menu.dismiss()

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

    def add_delivery(self, product, establishment_name, value):
        if establishment_name == "Nome do estabelecimento":
            self.__app.show_toast_msg("Informe o nome do estabelecimento!")
            return False
        if product == "Tipo do produto":
            self.__app.show_toast_msg("Informe o tipo do produto!")
            return False
        if not value:
            self.__app.show_toast_msg("Informe o valor da entrega!")
            return False
        self.reset_form()
        establishment = Establishment(establishment_name)
        delivery = Delivery(establishment, product, value)
        self.__app.firebase_manager.register_delivery(delivery)
        self.__app.firebase_manager.increase_user_experience()
        self.__app.show_toast_msg("Entrega registrada com sucesso!")
        return True

    def reset_form(self):
        self.ids.delivery_product.text = "Tipo do produto"
        self.ids.establishment.text = "Nome do estabelecimento"
        self.ids.delivery_value.text = self.default_delivery_value
