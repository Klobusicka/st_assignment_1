from unittest import TestCase
from tunepalapi import TunePalAPI

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