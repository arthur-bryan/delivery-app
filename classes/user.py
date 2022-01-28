from kivy.app import App

RUNNING_APP = App.get_running_app()

class User:

    def __init__(self, email, name, data=None):
        self.email = email
        self.name = name
        if data:
            self.title = data.get("title")
            self.level = data.get("level")
            self.experience = data.get("experience")
            self.deliveries = data.get("deliveries")
            self.registered_establishments = data.get("registered_establishments")
            self.profile_picture = data.get("profile_picture")
