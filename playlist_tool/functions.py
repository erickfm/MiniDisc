import streamlit as st
import pandas as pd
import requests
import datetime
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlist_tool.constants import *

client_id = st.secrets['spotify']['client_id']
client_secret = st.secrets['spotify']['client_secret']


@st.experimental_singleton
def get_all(_spotify_client_items, arg=None, step=20):
    offset = 0
    response = {'next':1}
    user_items = pd.DataFrame()
    while response['next']:
        response = _spotify_client_items(arg, offset=offset)
        user_items = pd.concat([user_items, pd.DataFrame(response['items'])])
        offset += step
    return user_items


def get_image(images):
    raw_image = requests.get(images[0]['url'], stream=True).raw
    im = Image.open(raw_image)
    width, height = im.size
    new_width = new_height = min(width, height)
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    im = im.crop((left, top, right, bottom))
    return im


def get_audio(audio_url):
    raw_audio = requests.get(audio_url, stream=True).raw
    audio_bytes = raw_audio.read()
    return audio_bytes


@st.experimental_singleton
def get_authenticated_client(code):
    # set authentication manager
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        redirect_uri=redirect_uri
    )
    # authenticate with spotify api
    return spotipy.Spotify(auth=auth_manager.get_access_token(code, as_dict=False))


@st.experimental_singleton
def get_authenticated_client_local():
    # set authentication manager
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        redirect_uri=redirect_uri
    )
    # authenticate with spotify api
    return spotipy.Spotify(auth_manager=auth_manager)


def get_playlist_attributes(playlist_id, user_df, authenticated_client):
    playlist_df = user_df[user_df['id'] == playlist_id]
    playlist_items_df = get_all(authenticated_client.playlist_items, arg=playlist_id)
    playlist_name = playlist_df.iloc[0]['name']
    playlist_url = playlist_df.iloc[0]['external_urls']['spotify']
    playlist_owner = playlist_df.iloc[0]['owner']['display_name']
    playlist_owner_url = playlist_df.iloc[0]['owner']['external_urls']['spotify']
    playlist_images = playlist_df.iloc[0]['images']
    return playlist_df, playlist_items_df, playlist_name, playlist_url, playlist_owner, playlist_owner_url, playlist_images


def get_tracklist(playlist_items_df):
    new_rows = []
    for row in playlist_items_df.iloc:
        new_row = {}
        new_row['track'] = row['track']['name']
        new_row['artists'] = [artist['name'] for artist in row['track']['artists']]
        new_row['album'] = row['track']['album']['name']
        new_row['duration'] = get_duration(row['track']['duration_ms'])
        new_row['date added'] = row['added_at'].split('T')[0]
        new_row['popularity'] = row['track']['popularity']
        new_row['images'] = row['track']['album']['images']
        new_row['id'] = row['track']['id']
        new_row['preview_url'] = row['track']['preview_url']
        new_rows.append(new_row)
    return pd.DataFrame(new_rows)


def get_duration(ms):
    duration = ':'.join(str(datetime.timedelta(milliseconds=ms)).split('.')[0].split(':')[1:])
    if duration[0] == '0':
        duration = duration[1:]
    return duration