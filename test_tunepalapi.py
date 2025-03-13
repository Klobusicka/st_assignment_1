from unittest import TestCase
from tunepalapi import TunePalAPI
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

    def test_previous_page(self):
        self.api.page_size = 10
        self.api.current_page_index = 5
        page_five = self.api.get_songs()
        self.api.previous_page()
        page_four = self.api.get_songs()
        self.assertNotEqual(page_five, page_four)
        self.assertEqual(self.api.current_page_index, 4)

    def test_next_page(self):
        self.api.page_size = 10
        self.api.current_page_index = 5
        page_five = self.api.get_songs()
        self.api.next_page()
        page_six = self.api.get_songs()
        self.assertNotEqual(page_five, page_six)
        self.assertEqual(self.api.current_page_index, 6)

    def test_set_page_size(self):
        self.api.page_size = 10
        self.assertEqual(self.api.page_size, 10)

    def test_search_by_name_one_result(self):
        self.api.set_page_size(1)
        self.api.add_song("Královna bielych tenisiek", "Elán", 1985)
        result = self.api.search("Královna bielych tenisiek")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Královna bielych tenisiek")
        self.assertEqual(result[0].artist, "Elán")
        self.assertEqual(result[0].release_year, 1985)

    def test_search_by_name_two_results(self):
        self.api.set_page_size(2)
        self.api.add_song("Kočka", "Ján Baláž", 1994)
        self.api.add_song("Kočka Kočka", "Elán", 2001)
        result = self.api.search("Kočka")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Kočka")
        self.assertEqual(result[0].artist, "Ján Baláž")
        self.assertEqual(result[0].release_year, 1994)
        self.assertEqual(result[1].title, "Kočka Kočka")
        self.assertEqual(result[1].artist, "Elán")
        self.assertEqual(result[1].release_year, 2001)

    def test_search_by_artist_one_result(self):
        self.api.set_page_size(1)
        self.api.add_song("Od Tatier k Dunaju", "Vašo Patejdl", 1989)
        result = self.api.search("Vašo")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Od Tatier k Dunaju")
        self.assertEqual(result[0].artist, "Vašo Patejdl")
        self.assertEqual(result[0].release_year, 1989)

    def test_search_by_artist_two_results(self):
        self.api.set_page_size(2)
        self.api.add_song("Od Tatier k Dunaju", "Vaso Patejdl", 1989)
        self.api.add_song("Nepriznaná", "Vaso Patejdl", 1989)
        result = self.api.search("Vaso Patejdl")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Od Tatier k Dunaju")
        self.assertEqual(result[0].artist, "Vaso Patejdl")
        self.assertEqual(result[0].release_year, 1989)
        self.assertEqual(result[1].title, "Nepriznaná")
        self.assertEqual(result[1].artist, "Vaso Patejdl")
        self.assertEqual(result[1].release_year, 1989)

    def test_search_by_year_one_result(self):
        self.api.set_page_size(1)
        result = self.api.search("1985")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Take On Me")
        self.assertEqual(result[0].artist, "a-ha")
        self.assertEqual(result[0].release_year, "1985")

    def test_search_by_year_two_results(self):
        self.api.set_page_size(2)
        result = self.api.search("2002")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "When I'm Gone")
        self.assertEqual(result[0].artist, "3 Doors Down")
        self.assertEqual(result[0].release_year, "2002")
        self.assertEqual(result[1].title, "Like a Stone")
        self.assertEqual(result[1].artist, "Audioslave")
        self.assertEqual(result[1].release_year, "2002")

    def test_no_found_songs(self):
        self.api.set_page_size(1)
        result = self.api.search("0000")
        self.assertEqual(len(result), 0)

    def test_get_songs_since_valid_year(self):
        self.api.set_page_size(2)
        result = self.api.get_songs_since("2000")
        self.assertEqual(len(result), 2)

    def test_get_songs_since_invalid_year(self):
        self.api.set_page_size(2)
        result = self.api.get_songs_since("500000")
        self.assertEqual(len(result), 0)

    def test_equal_songs(self):
        song1 = Song("Nie sme zlí", "Elán", 1982)
        song2 = Song("Nie sme zlí", "Elán", 1982)
        self.assertTrue(song1 == song2)

    def test_not_equal_songs(self):
        song1 = Song("Nie sme zlí", "Elán", 1982)
        song2 = Song("Nepriznaná", "Vašo Patejdl", 1989)
        self.assertFalse(song1 == song2)

    def test_non_valid_song(self):
        song1 = Song("Nie sme zlí", "Elán", 1982)
        song2 = "song"
        self.assertFalse(song1 == song2)