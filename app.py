import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth






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







scope = "user-read-playback-state user-read-currently-playing user-library-read user-top-read user-read-recently-played playlist-read-private playlist-read-collaborative"
redirect_uri = 'https://example.com/callback/'
# redirect_uri = 'http://localhost:8080/callback/'
auth_manager = SpotifyOAuth(
    client_id='d3c4d26f750f45daa2434a1585745291',
    client_secret='8912e43e7ebe4b1a84097e3997eb50ec',
    scope=scope,
    redirect_uri=redirect_uri
)
sp = spotipy.Spotify(auth_manager=auth_manager)

results = sp.current_user_saved_tracks()
st.write('hiii')
st.write('uh',results)


for i in sp.current_user_top_tracks(10)['items']:
    st.write(i['name'])
st.write(sp.user('123954053'))

def get_all_user_playlists(spotify_client):
    offset=0
    response = spotify_client.current_user_playlists(offset=offset)
    user_playlists = pd.DataFrame(response['items'])
    offset+=50
    while response['next']:
        response = spotify_client.current_user_playlists(offset=offset)
        user_playlists = pd.concat([user_playlists, pd.DataFrame(response['items'])])
        offset+=50
    return user_playlists

playlist_df = get_all_user_playlists(sp)

st.dataframe(playlist_df)

