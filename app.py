from playlist_tool.components import *

# set page configuration
st.set_page_config(
    layout="wide",
    page_title=title,
    page_icon=":minidisc:"
)

# auth_manager = SpotifyOAuth(
#         client_id=client_id,
#         client_secret=client_secret,
#         scope=scope,
#         redirect_uri=redirect_uri,
#         # open_browser=False
#     )
# r = requests.get(auth_manager.get_authorize_url())
# auth = auth_manager.get_access_token(r.url, as_dict=False)
# spotipy.Spotify(auth = auth)
# # auth_manager.get_auth_response()
#
#
# run sidebar based control function
sidebar()
# code = st.experimental_get_query_params()['code']
# st.write(code)

# scope = "user-read-playback-state user-read-currently-playing user-library-read user-top-read user-read-recently-played playlist-read-private playlist-read-collaborative"
# redirect_uri= 'https://example.com/callback/'
# client_id = 'd3c4d26f750f45daa2434a1585745291'
# client_secret = '8912e43e7ebe4b1a84097e3997eb50ec'

# auth_manager=SpotifyOAuth(client_id=client_id,
#                           client_secret=client_secret,
#                           scope=scope,
#                           redirect_uri=redirect_uri,
#                          )
# sp = spotipy.Spotify(auth_manager=auth_manager)
# for i in sp.current_user_top_tracks(10)['items']:
#     st.write(i['name'])