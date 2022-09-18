from playlist_tool.components import *

auth_manager = SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                scope=scope,
                                redirect_uri=redirect_uri,
                                )
try:
    code = st.experimental_get_query_params()['code']
    sp = spotipy.Spotify(auth=auth_manager.get_access_token(code, as_dict=False))
    tracks = sp.current_user_top_tracks(10)['items']
    st.write(f'### {tracks}')

except Exception as e:
    st.write(e)
    authorization_url = auth_manager.get_authorize_url()
    st.write(f'''<h1>
        Please login using this <a target="_self"
        href="{authorization_url}">url</a></h1>''',
             unsafe_allow_html=True)


# set page configuration
# st.set_page_config(
#     layout="wide",
#     page_title=title,
#     page_icon=":minidisc:"
# )

# # run sidebar based control function
# sidebar()





# ?code=AQAjdrurVFXyJvhRStRssqYIkR60RIz2NGKjkZvXAI6pgYUsifbhip_b2nsAjf94xxe-GMCopE8Fq9zvvCkDss9UudlcPI_QBmO8pdnlmEzrQtIsxIkrtQj9FMhZVVRws0kwz4VgQEjhcuJWFgHZ3hO93OAAJIwouybIMCE6_Q7n3R80mFVyqTjThJMFIeyxQ33VDjAX2Sbe1o2MKE-1e6ALq7BdHuBI5G9ZViAsu2hHdjRws-dAX9iSF6kAtnkGV8RErBQhN1ibIs2cL1UQ7922DVnjvCc4JrrP2n1i2f-flsqhnAIjOQ4ntpkR3ok_rt7RmLgMaBPJCTBa5xAbHBvg3RsR9U1Ze-wdvZ0gvo_pn_Qs7z4ZAUx19OPeMdDjuivX-gyJZYlA#_=_