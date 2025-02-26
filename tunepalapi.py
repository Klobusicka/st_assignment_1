from typing import List
import csv


class Song:
    title: str = ''
    artist: str = ''
    release_year: str = ''

    def __init__(self, title: str, artist: str, release_year: str):
        self.title = title
        self.artist = artist
        self.release_year = release_year


class TunePalAPI:

    songs: List[Song] = [] # holds all songs available from this API
    page_size: int # allows the user to decide how many songs are returned per page
    current_page_index: int

    def __init__(self, page_size=None):

        self.page_size = page_size
        self.current_page = 0
        with open('songlist.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['Song Clean']
                artist = row['ARTIST CLEAN']
                release_year = row['Release Year']
                self.songs.append(Song(title, artist, release_year))

    """Takes a list of songs and returns a smaller window using the 
    current_page_index and page_size"""
    def _build_song_window(self, song_list: List[Song]):
        first_index = self.current_page_index * self.page_size
        last_index = first_index + self.page_size
        return song_list[first_index:last_index]

    """Adds a song, but only if it isn't already in the list"""
    def add_song(self, title: str, artist: str, release_year: str):
        self.songs.add(Song(artist, title, release_year))

    """Return a page of songs, use next_page and previous_page to change the window"""
    def get_songs(self):
        return self._build_song_window(self.songs)

    """Tells the API to move to the previous page"""
    def next_page(self):
        self.current_page = self.current_page + 1

    """Tells the API to move to the next page"""
    def previous_page(self):
        self.current_page_index = self.current_page_index - 1

    """Set the page_size parameter, controllinig how many songs are returned"""
    def set_page_size(self, page_size: int):
        self.page_size = page_size

    """The search() function matches any songs whose title or artist starts
        with the query provided. E.G. a query of "The" would match "The Killers"
        "The Libertines" etc.
    """
    def search(self, starts_with_query: str):
        hits = []
        for song in self.songs:
            if song.title.startswith(starts_with_query):
                hits.append(song)
        return self._build_song_window(hits)

    """Allows users to filter out old-person music. Filter songs to only return
        songs released since a certain date. e.g. a query of 2022 would only return
        songs released this year 
    """
    def get_songs_since(self, release_year: str):
        hits = []
        for song in self.songs:
            if song.release_year > release_year:
                hits.append(song)
        return self._build_song_window(hits)