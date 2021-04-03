def SpotifyPlaylistSongExtract(PLAYLIST_ID):
    from API_Keys import CLIENT_ID, CLIENT_SECRET
    import pandas as pd
    import requests

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']


    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    TrackID_List = []
    Song_List = []
    Artist_List = []
    ReleaseYear_List = []

    r = requests.get(BASE_URL + 'playlists/' + PLAYLIST_ID, headers=headers)
    r = r.json()

    Playlist_Length = len(r['tracks']['items'])

    for i in range(Playlist_Length):
        
        TrackID = r['tracks']['items'][i]['track']['id']    
        Song = r['tracks']['items'][i]['track']['name']
        Artist = r['tracks']['items'][i]['track']['album']['artists'][0]['name']
        ReleaseYear = r['tracks']['items'][i]['track']['album']['release_date'].split('-')[0]
        
        TrackID_List.append(TrackID)
        Song_List.append(Song)
        Artist_List.append(Artist)
        ReleaseYear_List.append(ReleaseYear)


    Danceability_List = []
    Energy_List = []
    Key_List = []
    Loudness_List = []
    Mode_List = []
    Speechiness_List = []
    Acousticness_List = []
    Instrumentalness_List = []
    Liveness_List = []
    Valence_List = []
    Tempo_List = []
    DurationMS_List = []
    TimeSignature_List = []

    for track in TrackID_List:
        r = requests.get(BASE_URL + 'audio-features/' + track, headers=headers)
        r = r.json()
        
        Danceability_List.append(r['danceability'])
        Energy_List.append(r['energy'])
        Key_List.append(r['key'])
        Loudness_List.append(r['loudness'])
        Mode_List.append(r['mode'])
        Speechiness_List.append(r['speechiness'])
        Acousticness_List.append(r['acousticness'])
        Instrumentalness_List.append(r['instrumentalness'])
        Liveness_List.append(r['liveness'])
        Valence_List.append(r['valence'])
        Tempo_List.append(r['tempo'])
        DurationMS_List.append(r['duration_ms'])
        TimeSignature_List.append(r['time_signature'])  

    Playlist_DF = pd.DataFrame({'TrackID': TrackID_List, 'Song': Song_List, 'Artist': Artist_List, 'ReleaseYear': ReleaseYear_List,
                                'Danceability': Danceability_List, 'Energy': Energy_List, 'Key': Key_List, 'Loudness': Loudness_List,
                                'Mode': Mode_List, 'Speechiness': Speechiness_List, 'Acousticness': Acousticness_List,
                                'Instrumentalness': Instrumentalness_List, 'Liveness': Liveness_List, 'Valence': Valence_List,
                                'Tempo': Tempo_List, 'DurationMS': DurationMS_List, 'TimeSignature': TimeSignature_List})
    
    return Playlist_DF