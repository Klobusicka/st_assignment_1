from tunepalapi import TunePalAPI
from tunepalapi import Song


class User:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.my_songs = []
        self.shopping_basket = []
        self.users = []
        self.is_logged_in = False
        self.number_of_used_devices = 0

    def register(self, username: str, password: str):
        if any(user.username == username for user in self.users):
            raise ValueError("Username already registered")
        new_user = User(username, password)
        self.users.append(new_user)
        return new_user

    def login(self, username: str, password: str, device: str):
        for user in self.users:
            if user.username == username and user.password == password:
                self.is_logged_in = True
                if self.number_of_used_devices >= 2:
                    raise ValueError("Max 2 devices allowed")
                else:
                    self.number_of_used_devices += 1
                return user

        raise ValueError("Invalid username or password")

    def logout(self):
        if self.is_logged_in:
            self.number_of_used_devices -= 1
            self.is_logged_in = False
        else:
            raise ValueError("User not logged in")

    def add_my_song(self, song: Song):
        if song not in self.my_songs:
            self.my_songs.append(song)

    def add_to_shopping_basket(self, song: Song):
        self.shopping_basket.append(song)

    def checkout(self):
        self.my_songs.extend(self.shopping_basket)
        self.shopping_basket = []