from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable

MAX_ROWS = 200


class TableViewScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()
        self.layout = MDFloatLayout()
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        delivery_objects = self.fill_deliveries()
        self.data_table = MDDataTable(
            size_hint=(.94, .8),
            pos_hint={"center_x": 0.5, "center_y": 0.42},
            column_data=[
                ("No.", dp(10)),
                ("Estabelecimento", dp(36), self.sort_by_type),
                ("Valor", dp(22), self.sort_by_value),
                ("Data", dp(30), self.sort_by_date),
                ("Hora", dp(22), self.sort_by_hour)
            ],
            row_data=delivery_objects,
            rows_num=len(delivery_objects)
        )
        self.layout.add_widget(self.data_table)
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "delivery_screen"
            return True

    def on_pre_leave(self, *args):
        self.data_table.column_data = []
        self.layout.remove_widget(self.data_table)
        Window.unbind(on_keyboard=self.back)

    def fill_deliveries(self):
        deliveries = self.__app.firebase_manager.get_deliveries()
        if deliveries:
            data = [
                (
                    f"{num + 1}",
                    handle_category(delivery),
                    ("currency-brl", [.1, .8, .1, 1], delivery["value"]),
                    ("calendar", [.3, .3, .3, .5], delivery["date"]),
                    ("clock", [.3, .3, .3, .5], delivery["hour"])
                ) for num, delivery in enumerate(deliveries)
            ]
            return data
        return "", "", "", "", ""

    def sort_by_type(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][1][0]
            )
        )

    def sort_by_value(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][2]
            )
        )

    def sort_by_date(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][3]
            )
        )

    def sort_by_hour(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][4]
            )
        )


def handle_category(delivery):
    icon_categories = {
        "Hamburguer": {"icon": "hamburger",
                       "color": [.7, .3, 0, 1],
                       "name": delivery["establishment"]["name"]
                       },
        "Pizza": {"icon": "pizza",
                  "color": [.8, .7, 0, 1],
                  "name": delivery["establishment"]["name"]
                  },
        "Sorvete": {"icon": "ice-cream",
                    "color": [.25, .0, .5, .8],
                    "name": delivery["establishment"]["name"]
                    },
        "Lanche": {"icon": "food",
                   "color": [.9, 0, 0, 1],
                   "name": delivery["establishment"]["name"]
                   },
        "Coxinha": {"icon": "food-drumstick",
                    "color": [8, .75, .62, 1],
                    "name": delivery["establishment"]["name"]
                    },
        "Comida": {"icon": "food-turkey",
                   "color": [.9, 0, 0, 1],
                   "name": delivery["establishment"]["name"]
                   },
        "Fruta": {"icon": "food-apple",
                  "color": [.2, 1, .2, 1],
                  "name": delivery["establishment"]["name"]
                  },
        "Bebida": {"icon": "beer",
                   "color": [.94, 0, .05, 1],
                   "name": delivery["establishment"]["name"]
                   },
        "Farmacia": {"icon": "pharmacy",
                     "color": [.3, 9, 2, 1],
                     "name": delivery["establishment"]["name"]
                     },
        "Eletronicos": {"icon": "tablet-cellphone",
                        "color": [.2, .2, .2, 1],
                        "name": delivery["establishment"]["name"]
                        },
        "Documento": {"icon": "file-document",
                      "color": [0, 0, 0, 1],
                      "name": delivery["establishment"]["name"]
                      },
        "Vestimenta": {"icon": "tshirt-crew",
                       "color": [.8, .8, 0, 1],
                       "name": delivery["establishment"]["name"]
                       },
        "Mercado": {"icon": "storefront",
                    "color": [1, .5, .5, .8],
                    "name": delivery["establishment"]["name"]
                    },
        "Outro": {"icon": "null",
                  "color": [0, 0, 0, 1],
                  "name": delivery["establishment"]["name"]
                  },
    }
    return (icon_categories.get(delivery["product"]).get("icon"),
            icon_categories.get(delivery["product"]).get("color"),
            icon_categories.get(delivery["product"]).get("name"))
