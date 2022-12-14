from playlist_tool.functions import *


def playlists(user_df, authenticated_client):
    options_dict = {f"{name} - {owner['display_name']}": id for name, owner, id in
                    zip(user_df['name'], user_df['owner'], user_df['id'])}
    selected_playlist = st.selectbox('Select a Playlist:', options=options_dict.keys())
    playlist_id = options_dict[selected_playlist]
    playlist_df, playlist_items_df, playlist_name, playlist_url, playlist_owner, playlist_owner_url, playlist_images \
        = get_playlist_attributes(playlist_id, user_df, authenticated_client)
    col1, col2, col3 = st.columns([2, 6, 2])

    # Load data
    playlist_image = get_image(playlist_images)
    tracklist_df = get_tracklist(playlist_items_df)
    track_df = tracklist_df.sample(n=1).iloc[0]
    track_images = track_df['images']
    preview_url = track_df['preview_url']
    track_image = get_image(track_images)
    track_audio = get_audio(preview_url)

    # Column 1
    col1.markdown(f"### [{playlist_name}]({playlist_url}) \n [{playlist_owner}]({playlist_owner_url})")
    col1.image(playlist_image)
    pull_track = col1.button('Pull Random Track')

    # Column 2
    visible_columns = ['track', 'artists', 'album', 'date added', 'duration', 'popularity']
    col2.dataframe(tracklist_df[visible_columns].assign(temp='').set_index('temp'))

    # Column 3
    col3.markdown(f"#### {track_df['track']} \n {' '.join(track_df['artists'])}")
    col3.image(track_image)
    col3.audio(track_audio)


def search(user_df, authenticated_client):
    search_term = st.text_input('Search:').lower()
    start_search = st.button('Submit')
    if start_search:
        with st.spinner('Retrieving your Library...'):
            all_playlist_items_df = get_all_playlist_items(user_df, authenticated_client)
        with st.spinner('Searching...'):
            columns = ['track', 'artists', 'album', 'duration', 'date added', 'popularity', 'id', 'playlist']
            search_results = get_search_results(all_playlist_items_df, search_term)
            search_results = search_results[columns].drop_duplicates().reset_index(drop=True)
            st.dataframe(search_results, use_container_width=True)


def sidebar():
    if redirect_uri not in ["https://erickfm-minidisc-app-pxiqru.streamlitapp.com/", 'https://minidisc.streamlit.app/']:
        authenticated_client = get_authenticated_client_local()
    else:
        # get redirect url params code
        code = st.experimental_get_query_params()['code']
        # get authenticated client
        authenticated_client = get_authenticated_client(code)
    # show a title
    st.sidebar.markdown(f'# :minidisc: {title}')
    page = st.sidebar.selectbox(label='Main Menu', options=['Playlists', 'Search'])
    # get user playlists
    user_df = get_all(authenticated_client.current_user_playlists)
    # conditionals on page selection
    if page == 'Playlists':
        playlists(user_df, authenticated_client)
    if page == 'Search':
        search(user_df, authenticated_client)
