from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
import os


class UserScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__app = App.get_running_app()
        self.dialog = None
        self.file_manager = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager,
            preview=True
        )
        self.manager_open = False
        self.user = None
        self.user_deliveries = None

    def close_dialog(self, obj):
        self.dialog.dismiss()


    def on_pre_enter(self, *args):
        self.user = self.__app.logged_in_user
        self.user.profile_photo = self.__app.firebase_manager.get_user_profile_photo(self.user.name)
        self.user_deliveries = self.__app.firebase_manager.get_deliveries()
        total_in_deliveries = self.get_total_value_from_deliveries()
        user_screen = self.__app.screen_manager.get_screen("user_screen")
        user_screen.ids.user_image.source = self.user.profile_photo
        user_screen.ids.user_label.text = f"Nome: {self.user.name}"
        user_screen.ids.email_label.text = f"Email: {self.user.email}"
        user_screen.ids.deliveries_number_label.text = f"Total de entregas: {str(len(self.user_deliveries))}"
        user_screen.ids.deliveries_value_label.text = f"Total em entregas: R$ {str(round(total_in_deliveries, 2))}"
        user_screen.ids.level_label.text = f"Nivel: {self.__app.firebase_manager.get_user_info('level')}"
        user_screen.ids.experience_label.text = f"Experiencia: {self.__app.firebase_manager.get_user_info('experience')}"
        user_screen.ids.title_label.text = f"Titulo: {self.__app.firebase_manager.get_user_info('title')}"
        Window.bind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key in (27, 1001):
            self.__app.screen_manager.current = "delivery_screen"
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.back)

    def get_total_value_from_deliveries(self):
        total_value = 0
        if len(self.user_deliveries) > 0:
            for delivery in self.user_deliveries:
                total_value += float(delivery["value"])
        return total_value

    def change_profile_picture(self, new):
        if os.path.isfile(new):
            self.ids.user_image.source = new

    def file_manager_open(self):
        self.file_manager.show(self.__app.user_data_dir)
        self.manager_open = True

    def select_path(self, path):
        if os.path.isfile(path):
            Clock.schedule_once(lambda x: self.change_profile_picture(path), 1)
            self.__app.firebase_manager.update_profile_photo(self.user, path)
        self.exit_manager()
        return path

    def exit_manager(self):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
