import pyrebase
from requests import exceptions
from kivy.app import App
from classes.user import User
import json


firebase_config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "storageBucket": "",
    "serviceAccount": ""
}

firebase = pyrebase.initialize_app(firebase_config)


class FirebaseManager:

    def __init__(self):
        self.__app = App.get_running_app()
        self.__auth = firebase.auth()
        self.__db = firebase.database()

    def get_error_by_json(self, error_json):
        error_message = json.loads(error_json)["error"]["message"].split(":")[0].strip()
        errors_map = {
            "EMAIL_NOT_FOUND": "Email nao encontrado!",
            "INVALID_PASSWORD": "Senha invalida!",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Muitas tentativas invalidas. Conta bloqueada!",
            "EMAIL_EXISTS": "Email ja cadastrado!",
            "INVALID_EMAIL": "Email invalido!",
            "MISSING_PASSWORD": "Informe a senha!"
        }
        try:
            self.__app.show_toast_msg(errors_map.get(error_message))
        except KeyError:
            self.__app.show_toast_msg("Erro desconhecido!")
        return

    def send_reset_password_email(self):
        self.__auth.send_password_reset_email(self.__app.logged_in_user.email)
        self.__app.show_toast_msg("Email para alteracao da senha enviado!")

    def get_user_data(self, name, email):
        data = self.__db.child("users").child(name).get().val()
        if data:
            return data
        self.register_user_in_realtime_database(name, email)
        self.get_user_data(name, email)
        self.update_user_data()

    def update_user_data(self):
        self.__app.logged_in_user = User(self.__app.logged_in_user.email,
                                         self.__app.logged_in_user.name,
                                         self.get_user_data(self.__app.logged_in_user.name,
                                                            self.__app.logged_in_user.email))

    def register_user(self, email, password):
        try:
            self.__auth.create_user_with_email_and_password(email, password)
            user = User(email, email.split("@")[0])
            self.__app.firebase_manager.register_user_in_realtime_database(user.name, email)
            return True
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            if type(error) == exceptions.HTTPError:
                self.get_error_by_json(error.args[1])
            elif type(error) == exceptions.ConnectionError:
                self.__app.show_toast_msg("Erro de conexao!")
            return False

    def register_user_in_realtime_database(self, user, email):
        data = {
            "email": user.name,
            "name": user.email,
            "title": "Aprendiz do Grau",
            "level": 1,
            "experience": 0,
            "registered_establishments": [],
            "deliveries": [],
            "profile_picture": "static/images/user_icons/default_user.png"
        }
        self.__db.child("users").child(user.name).set(data)

    def update_profile_photo(self, user, new_photo):
        data = {
            "name": user.name,
            "email": user.email,
            "profile_picture": new_photo
        }
        self.__db.child("users").child(user.name).set(data)

    def login_user(self, email, password):
        try:
            return self.__auth.sign_in_with_email_and_password(email, password)
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            if type(error) == exceptions.HTTPError:
                self.get_error_by_json(error.args[1])
            elif type(error) == exceptions.ConnectionError:
                self.__app.show_toast_msg("Erro de conexao!")
            return None

    def get_user_info(self, attribute):
        user_name = self.__app.logged_in_user.name
        return self.__db.child("users").child(user_name).child(attribute).get().val()

    def register_delivery(self, delivery):
        data = {
            "establishment": {
                "name": delivery.establishment.name,
                "default_delivery_value": delivery.establishment.default_delivery_value
            },
            "product": delivery.product,
            "date": delivery.registered_date,
            "hour": delivery.registered_hour,
            "value": delivery.value
        }
        self.__db.child("users").child(self.__app.logged_in_user.name).child("deliveries").push(data)
        self.update_user_data()

    def get_user(self, user):
        users = self.__db.child("users").get()
        if not users.each() is None:
            all_users = [user.val() for user in users.each()]
            return list(filter(lambda _: _["email"] == user.email, all_users))
        return []

    def get_deliveries(self):
        """Get deliveries registered by the specified user.

        Returns:
            (:obj:`list`): A list of deliveries registered by the specified user.
        """
        deliveries = self.__db.child("users").child(self.__app.logged_in_user.name).child("deliveries").get()
        if not self.is_empty(deliveries):
            all_deliveries = [delivery.val() for delivery in deliveries.each()]
            return all_deliveries
        return []

    def get_registered_establishments_data(self):
        establishments = self.__db.child("users").child(self.__app.logged_in_user.name).child("registered_establishments").get()
        deliveries = self.get_deliveries()
        establishments_data = []
        if not self.is_empty(establishments):
            # and not len(deliveries) == 0:
            all_establishments = [establish.val() for establish in establishments.each()]
            for establish in all_establishments:
                total_deliveries = 0
                total_value = 0
                for delivery in deliveries:
                    if delivery.get("establishment").get("name") == establish.get("name"):
                        total_deliveries += 1
                        total_value += float(delivery.get("value"))
                establishments_data.append(
                    {
                        "name": establish.get("name"),
                        "total_deliveries": total_deliveries,
                        "default_delivery_value": establish.get("default_delivery_value"),
                        "total_value": total_value
                    }
                )
            return establishments_data
        return None

    def get_user_profile_photo(self, user):
        users = self.__db.child("users").get()
        if not self.is_empty(users):
            for _ in users.each():
                if _.val()["name"] == user:
                    return _.val()["profile_picture"]
        return None

    def increase_user_experience(self):
        user_name = self.__app.logged_in_user.name
        current = int(self.__db.child("users").child(user_name).child("experience").get().val())
        self.__db.child("users").child(user_name).update({"experience": str(current + 10)})
        self.perform_level_upgrade(current)

    def update_title(self, level):
        user_name = self.__app.logged_in_user.name
        level_title_map = {
            1: "Iniciante do Grau",
            2: "Delivery Boy",
            3: "Concorrente do Sedex",
            4: "Fast in Food",
            5: "Mata Fome",
            6: "Google Maps em Pessoa"
        }
        self.__db.child("users").child(user_name).update({"title": level_title_map.get(level)})

    def perform_level_upgrade(self, current_experience):
        user_name = self.__app.logged_in_user.name
        if current_experience + 10 <= 100:
            self.update_title(1)
            self.__db.child("users").child(user_name).update({"level": str(1)})
        elif 100 < current_experience + 10 <= 500:
            self.update_title(2)
            self.__db.child("users").child(user_name).update({"level": str(2)})
        elif 500 < current_experience + 10 <= 1000:
            self.update_title(3)
            self.__db.child("users").child(user_name).update({"level": str(3)})
        elif 3000 < current_experience + 10 <= 3000:
            self.update_title(4)
            self.__db.child("users").child(user_name).update({"level": str(4)})
        elif 5000 < current_experience + 10 <= 5000:
            self.update_title(5)
            self.__db.child("users").child(user_name).update({"level": str(5)})
        else:
            self.update_title(6)
            self.__db.child("users").child(user_name).update({"level": str(6)})

    def register_establishment(self, establishment):
        data = {
            "name": establishment.name,
            "default_delivery_value": establishment.default_delivery_value
        }
        self.__db.child("users").child(self.__app.logged_in_user.name).child("registered_establishments").child(establishment.name).set(data)
        self.update_user_data()

    def establishment_exists(self, establishment):
        establishments = self.__app.logged_in_user.registered_establishments
        if establishments:
            for establish in establishments:
                if establish == establishment.name:
                    del establishments
                    return True
        del establishments
        return False

    def increase_stablishment_deliveries(self, establishment):
        current_value = self.__db.child("establishments").child(establishment.name).child(
            "total_deliveries").get().val()
        self.__db.child("establishments").child(establishment.name).update(
            {"total_deliveries": current_value + 1})

    def get_establishments(self):
        if self.__app.logged_in_user is not None:
            establishments = self.__db.child("users").child(self.__app.logged_in_user.name).child("registered_establishments").get()
            if not self.is_empty(establishments):
                all_establishments = [establishment.val().get("name") for establishment in establishments.each()]
                return all_establishments
        return []

    @staticmethod
    def is_empty(establishments):
        if establishments.each() is None:
            return True
        return False
