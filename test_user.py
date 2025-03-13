from unittest import TestCase
from user import User
from tunepalapi import Song


class TestUser(TestCase):

    def setUp(self):
        self.user = User("username", "password")
        self.user1 = User("username1", "password1")
        self.user1.register("username1", "password1")
        self.song1 = Song("song1", "artist1", "2001")
        self.song2 = Song("song2", "artist2", "2002")

    def test_creating_user(self):
        self.assertEqual(self.user.username, "username")
        self.assertEqual(self.user.password, "password")

    def test_user_register_new_user(self):
        user = self.user.register("username", "password")
        self.assertIn(user, self.user.users)

    def test_user_register_existing_user(self):
        user = self.user.register("username", "password")
        self.assertRaises(ValueError, self.user.register, user.username, "password")

    def test_user_login_successful(self):
        user = self.user.register("username", "password")
        self.user.login("username", "password", "device")
        self.assertTrue(user.is_logged_in)

    def test_user_login_unsuccessful(self):
        self.assertRaises(ValueError, self.user1.login, "username", "wrong_password", "device")

    def test_user_logout_successful(self):
        user = self.user1.login("username1", "password1", "device")
        user.logout("username1", "device")
        self.assertFalse(user.is_logged_in)

    def test_user_logout_unsuccessful(self):
        self.assertRaises(ValueError, self.user1.logout, "username1", "device")

    def test_add_my_song(self):
        self.user1.add_my_song(self.song1)
        self.assertIn(self.song1, self.user1.my_songs)

    def test_add_my_song_duplicate_song(self):
        self.user1.add_my_song(self.song1)
        self.user1.add_my_song(self.song1)
        self.assertEqual(len(self.user1.my_songs), 1)

    def test_add_to_shopping_basket(self):
        self.user1.add_to_shopping_basket(self.song1)
        self.assertIn(self.song1, self.user1.shopping_basket)

    def test_checkout(self):
        self.user1.add_to_shopping_basket(self.song1)
        self.user1.add_to_shopping_basket(self.song2)
        self.user1.checkout()
        self.assertIn(self.song1, self.user1.my_songs)
        self.assertIn(self.song2, self.user1.my_songs)
        self.assertEqual(self.user1.shopping_basket, [])