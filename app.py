import numpy as np
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth




import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state user-read-currently-playing user-library-read user-top-read user-read-recently-played playlist-read-private playlist-read-collaborative"
redirect_uri= 'https://example.com/callback/'
auth_manager = SpotifyOAuth(
    client_id='d3c4d26f750f45daa2434a1585745291',
    client_secret='8912e43e7ebe4b1a84097e3997eb50ec',
    scope=scope,
    redirect_uri=redirect_uri
)
sp = spotipy.Spotify(auth_manager=auth_manager)

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])



# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
title="Playlist Tool"
st.set_page_config(
    # layout="wide",
    page_title=title,
    page_icon=":minidisc:"
)

st.markdown(f'## {title}')

# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    pass
# STREAMLIT APP LAYOUT
data = load_data()

