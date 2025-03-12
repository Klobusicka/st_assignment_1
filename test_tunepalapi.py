from unittest import TestCase
from tunepalapi import TunePalAPI
from tunepalapi import User
from tunepalapi import Song
from collections import Counter

class TestTunePalAPI(TestCase):
    api = TunePalAPI()

    def setUp(self):
        self.api = TunePalAPI()

    "Testing add_song"
    def test_add_song_one_song(self):
        self.api.add_song("Kde si", "Elán", 2010)
        self.assertIn("Kde si", [song.title for song in self.api.songs])
        self.assertIn("Elán", [song.artist for song in self.api.songs])

    def test_add_song_two_songs(self):
        self.api.add_song("Nie sme zlí", "Elán", 1982)
        self.api.add_song("Nepriznaná", "Vašo Patejdl", 1989)
        self.assertIn("Nie sme zlí", [song.title for song in self.api.songs])
        self.assertIn("Elán", [song.artist for song in self.api.songs])
        self.assertIn("Nepriznaná", [song.title for song in self.api.songs])
        self.assertIn("Vašo Patejdl", [song.artist for song in self.api.songs])

    def test_add_song_twice_same_song(self):
        self.api.add_song("Fero", "Elán", 1985)
        self.api.add_song("Fero", "Elán", 1985)
        self.assertIn("Fero", [song.title for song in self.api.songs])

    def test_add_song_empty_title(self):
        self.api.add_song("", "Jožo Ráž", 2006)
        self.assertIn("Jožo Ráž", [song.artist for song in self.api.songs])
        self.assertIn("", [song.title for song in self.api.songs])

    def test_add_song_same_name_and_artist_different_year(self):
        self.api.add_song("Od Tatier k Dunaju", "Vašo Patejdl", 1989)
        self.api.add_song("Od Tatier k Dunaju", "Vašo Patejdl", 1990)
        self.assertIn(("Od Tatier k Dunaju", "Vašo Patejdl", 1989), [(song.title, song.artist, song.release_year) for song in self.api.songs])
        self.assertIn(("Od Tatier k Dunaju", "Vašo Patejdl", 1990), [(song.title, song.artist, song.release_year) for song in self.api.songs])

    def test_add_song_same_song_added_twice(self):
        self.api.add_song("Kočka", "Ján Baláž", 1994)
        self.api.add_song("Kočka", "Ján Baláž", 1994)
        song_counts = Counter((song.title, song.artist, song.release_year) for song in self.api.songs)
        self.assertEqual(song_counts[("Kočka", "Ján Baláž", 1994)], 1)

    def test_get_songs_without_page_size(self):
        with self.assertRaises(ValueError) as context:
            self.api.get_songs()

    def test_get_songs_check_number_of_songs(self):
        self.api.page_size = 10
        songs_on_page = self.api.get_songs()
        self.assertGreater(len(songs_on_page), 0)
        self.assertEqual(len(songs_on_page), 10)
        self.assertLessEqual(len(songs_on_page), self.api.page_size)

    def test_get_songs_moving_to_next_page(self):
        self.api.page_size = 10
        self.api.current_page_index = 0
        first_page = self.api.get_songs()
        self.api.next_page()
        second_page = self.api.get_songs()
        self.assertNotEqual(first_page, second_page)

    def test_get_songs_checking_songs_in_different_pages(self):
        self.api.page_size = 10
        self.api.current_page_index = 0
        first_page = self.api.get_songs()
        self.api.next_page()
        second_page = self.api.get_songs()
        first_page_songs = [song.title for song in first_page]
        second_page_songs = [song.title for song in second_page]
        self.assertNotEqual(first_page_songs, second_page_songs)

class TestUser(TestCase):

    def setUp(self):
        self.user = User("username", "password")


    def test_creating_user(self):
        self.assertEqual(self.user.username, "username")
        self.assertEqual(self.user.password, "password")

    def test_user_register_new_user(self):
        user = self.user.register("username", "password")
        self.assertIn(user, self.user.users)

    def test_user_register_existing_user(self):
        user = self.user.register("username", "password")
        self.assertRaises(ValueError, self.user.register, user.username, "password")