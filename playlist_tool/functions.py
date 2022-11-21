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
    response = {'next': 1}
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
        try:
            new_row = {'track': row['track']['name'],
                       'artists': ', '.join([str(artist['name']) for artist in row['track']['artists']]),
                       'album': row['track']['album']['name'],
                       'duration': get_duration(row['track']['duration_ms']),
                       'date added': row['added_at'].split('T')[0],
                       'popularity': row['track']['popularity'],
                       'images': row['track']['album']['images'],
                       'id': row['track']['id'],
                       'preview_url': row['track']['preview_url']}
            new_rows.append(new_row)
        except TypeError as e:
            pass
    return pd.DataFrame(new_rows)


def get_duration(ms):
    duration = ':'.join(str(datetime.timedelta(milliseconds=ms)).split('.')[0].split(':')[1:])
    if duration[0] == '0':
        duration = duration[1:]
    return duration


@st.experimental_singleton
def get_all_playlist_items(user_df, _authenticated_client):
    all_playlist_items_df = pd.DataFrame()
    progress_bar = st.progress(0)
    for index, playlist_id in enumerate(list(user_df['id'])):
        playlist_df, playlist_items_df, playlist_name, playlist_url, playlist_owner, playlist_owner_url, playlist_images\
            = get_playlist_attributes(playlist_id, user_df, _authenticated_client)
        tracklist_df = get_tracklist(playlist_items_df)
        tracklist_df['playlist'] = playlist_name
        tracklist_df['id'] = playlist_id
        all_playlist_items_df = pd.concat([all_playlist_items_df, tracklist_df])
        # Update progress bar
        percent_complete = int((index + 1) / len(user_df['id']) * 100)
        progress_bar.progress(percent_complete)
    progress_bar.empty()
    return all_playlist_items_df


def get_search_results(all_playlist_items_df, search_term):
    return all_playlist_items_df[all_playlist_items_df['track'].str.strip().str.lower().str.contains(search_term)
                                 | all_playlist_items_df['playlist'].str.strip().str.lower().str.contains(search_term)
                                 | all_playlist_items_df['artists'].str.strip().str.lower().str.contains(search_term)]
