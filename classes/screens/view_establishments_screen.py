from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
import os
import random


class ViewEstablishmentsScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()
        self.carousel = MDCarousel()
        self.add_widget(self.carousel)

    def on_pre_enter(self, *args):
        establishments_data = self.__app.firebase_manager.get_registered_establishments_data()
        if establishments_data:
            self.populate_carousel(establishments_data)
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "delivery_screen"
            return True

    def on_pre_leave(self, *args):
        self.carousel.clear_widgets()
        Window.unbind(on_keyboard=self.back)

    def populate_carousel(self, data):
        images_path = "static/images/establishments"
        for establishment in data:
            random_image = random.choice(os.listdir(images_path))
            layout = MDFloatLayout()
            card = MDCard(
                orientation="vertical",
                size_hint=(.9, .58),
                pos_hint={"center_x": .5, "center_y": .5}
            )
            image = Image(
                source=os.path.join(images_path, random_image),
                size_hint=(1, .6),
                pos_hint={"center_x": .5, "center_y": .8}
            )
            name_label = MDLabel(
                padding_x=10,
                text=f"Nome: {establishment.get('name')}",
                font_name=self.__app.default_font,
                font_size=dp(self.__app.small_font_size),
                size_hint_y=0.07
            )
            total_deliveries_label = MDLabel(
                padding_x=10,
                text=f"Total de entregas: {establishment.get('total_deliveries')}",
                font_name=self.__app.default_font,
                font_size=dp(self.__app.small_font_size),
                size_hint_y=0.07
            )
            default_value_label = MDLabel(
                padding_x=10,
                text=f"Valor padrao da entrega: {establishment.get('default_delivery_value')}",
                font_name=self.__app.default_font,
                font_size=dp(self.__app.small_font_size),
                size_hint_y=0.07
            )
            total_value_label = MDLabel(
                padding_x=10,
                text=f"Valor total em entregas: R$ {establishment.get('total_value')}",
                font_name=self.__app.default_font,
                font_size=dp(self.__app.small_font_size),
                size_hint_y=0.07
            )
            edit_button = MDIconButton(
                disabled=True,
                icon="pencil",
                pos_hint={'center_x': .65, 'center_y': .1},
                md_bg_color=(.98, .72, .0)
            )
            card.add_widget(image)
            card.add_widget(name_label)
            card.add_widget(total_deliveries_label)
            card.add_widget(default_value_label)
            card.add_widget(total_value_label)
            layout.add_widget(edit_button)
            layout.add_widget(card)
            self.carousel.add_widget(layout)

