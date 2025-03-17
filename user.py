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

    '''Storing users credentials only if nobody else has the same username.'''
    def register(self, username: str, password: str):
        if any(user.username == username for user in self.users):
            raise ValueError("Username already registered")
        new_user = User(username, password)
        self.users.append(new_user)
        return new_user

    '''Loging user on a device only if he already registered and sets correct username and password and increasing number of used devices.'''
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

    '''Log out of user and decreasing number of used devices.'''
    def logout(self):
        if self.is_logged_in:
            self.number_of_used_devices -= 1
            self.is_logged_in = False
        else:
            raise ValueError("User not logged in")

    '''Adding given song into the list of my songs.'''
    def add_my_song(self, song: Song):
        if song not in self.my_songs:
            self.my_songs.append(song)

    '''Adding given song into the shopping basket.'''
    def add_to_shopping_basket(self, song: Song):
        self.shopping_basket.append(song)

    '''Adding songs from shopping basket into the list of my songs and clearing the shopping basket.'''
    def checkout(self):
        self.my_songs.extend(self.shopping_basket)
        self.shopping_basket = []