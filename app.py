from playlist_tool.components import *

set page configuration
st.set_page_config(
    layout="wide",
    page_title=title,
    page_icon=":minidisc:"
)

try:
    # run sidebar based control function
    sidebar()
except Exception as e:
    authorization_url = auth_manager.get_authorize_url() + '&output=embed'
    st.write(f"[url]({authorization_url})")
    # st.write(f'''<h1>
    #     Please login using this <a target="_self"
    #     href="{authorization_url}">url</a></h1>''',
    #          unsafe_allow_html=True)
