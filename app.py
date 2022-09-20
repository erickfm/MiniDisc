from playlist_tool.components import *

# set page configuration
st.set_page_config(
    layout="wide",
    page_title=title,
    page_icon=":minidisc:"
)

try:
    # run sidebar based control function
    sidebar()
except:
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        redirect_uri=redirect_uri
    )
    authorization_url = auth_manager.get_authorize_url()
    st.write(f"# [Login]({authorization_url})")

