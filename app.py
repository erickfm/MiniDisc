from playlist_tool.components import *

# set page configuration
st.set_page_config(
    layout="wide",
    page_title=title,
    page_icon=":minidisc:"
)

if redirect_uri not in ["https://erickfm-minidisc-app-pxiqru.streamlitapp.com/", 'https://minidisc.streamlit.app/']:
    sidebar()
else:
    try:
        # run sidebar based control function
        sidebar()
    except:
        # set authentication manager
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            redirect_uri=redirect_uri
        )
        # get authentication url for login
        authorization_url = auth_manager.get_authorize_url()
        # display login link
        st.write(f"# [Login]({authorization_url})")
