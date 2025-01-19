"""
    Python script to generate song images off of cover of album and song name
"""

import typing
from typing import IO
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

    def song_photo_download(self, song_json: typing.Dict, song_list_text: IO) -> None:
        song = song_json["track"]
        picture_url = song["album"]["images"][-2]["url"]
        song_name = song["name"]

        album_cover_data = requests.get(picture_url, timeout=10).content

        album_cover = Image.open(BytesIO(album_cover_data))

        album_cover_drawer = ImageDraw.Draw(album_cover)

        font = ImageFont.truetype("./Arial.ttf", size=15)
        album_cover_drawer.text(
            (0, 0),
            song_name,
            fill="black",
            stroke_fill="white",
            stroke_width=3,
            font=font,
        )

        song_list_text.write(f"Song: {song_name}\n")

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


song_list_file = open("./songList.txt", "w")

while song_catalog_json:
    for songJSON in song_catalog_json["items"]:
        spUnit.song_photo_download(song_json=songJSON, song_list_text=song_list_file)
    song_catalog_json = spUnit.next(song_catalog_json)
