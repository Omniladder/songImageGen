"""
    Python script to generate song images off of cover of album and song name
"""

import typing
import requests


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json


class SpotifyUnit:
    """

    Attributes:
        USERNAME (str): the username of the profile to get data from
        sp (Spotify): the authentication and api object

    Methods:
        __init__ (user_name: str): Creates the Initial object
        get_username() -> str: gets the inputted user name
        get_artist(artist_urn: str) -> str: returns name of artist based on URN
    """

    def __init__(self, user_name: str) -> None:
        """
        Used to handle document autentication

        Arguments:
            user_name(str): Gives the Username to access api from
        """
        self.user_name = user_name

        auth_manager = SpotifyClientCredentials()

        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        # self.sp.user(self.user_name)

    def get_username(self) -> str:
        """
        Simple function for getting the saved usong_namesername from object
        """
        return self.user_name

    def get_artist(self, artist_urn: str) -> str:
        """
        Function that returns an artists name given a URN

        Arguments:
            artist_urn(str): the URN of the desired artist
        """
        return self.sp.artist(artist_urn)

    def get_user_playlists(self, user: str) -> typing.Dict:
        """_summary_

        Arguments:
            user -- user you want play lists from

        Returns:
            _description_
        """
        return self.sp.user_playlists(user)

    def get_playlist(self, playlist_id: str) -> typing.Dict:
        """_summary_

        Arguments:
            playlist_id -- _description_

        Returns:
            _description_
        """
        return self.sp.playlist(playlist_id)

    def song_photo_download(self, songJSON: typing.Dict):
        song = songJSON["track"]
        picture_url = song["album"]["images"][0]["url"]
        song_name = song["name"]

        album_cover_data = requests.get(picture_url, timeout=10).content

        album_cover = Image.open(BytesIO(album_cover_data))

        album_cover_drawer = ImageDraw.Draw(album_cover)

        font = ImageFont.truetype("./Arial.ttf", size=50)
        album_cover_drawer.text(
            (0, 50),
            song_name,
            fill="black",
            stroke_fill="white",
            stroke_width=3,
            font=font,
        )

        album_cover.save(f"./pics/{song_name}.png")

    def next(self, catalog_json: typing.Dict) -> typing.Dict:
        """_summary_

        Arguments:
            catalogJSON -- _description_

        Returns:
            _description_
        """
        return self.sp.next(catalog_json)


spUnit = SpotifyUnit("Omniladder")

USER_ID = "mc77wtpksybaewjw9dm8n6nt5"
INITIAL_PLAYLIST_ID = "588iUCnGGcUQ8uw3GAWj2E"

# PIL.show(album_cover)

song_catalog_json = spUnit.get_playlist(playlist_id=INITIAL_PLAYLIST_ID)["tracks"]

"""
print(song_catalog_json["tracks"].keys())

file = open("./songCatalog", "w")
json.dump(song_catalog_json, file)
"""

while song_catalog_json:
    for songJSON in song_catalog_json["items"]:
        spUnit.song_photo_download(songJSON=songJSON)
    song_catalog_json = spUnit.next(song_catalog_json)
