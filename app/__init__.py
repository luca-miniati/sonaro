import os

import spotipy
from flask import Flask, redirect, render_template, request, session, url_for
from flask_frozen import Freezer
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
app.config['FREEZER_DESTINATION'] = 'build/freezer'

freezer = Freezer(app)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='http://127.0.0.1:5000/callback',
    scope=['user-library-read', 'user-read-playback-state',
           'user-read-recently-played', 'user-top-read'],
)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect('/profile')


@app.route('/profile')
def profile():
    if 'token_info' not in session:
        return redirect('/login')

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    user_img = user_info['images'][0]['url'] if user_info['images'] \
        else url_for('static', filename='default-profile-picture.jpeg')

    return render_template(
        'profile.html',
        user_display_name=user_info["display_name"], user_img=user_img)


@app.route('/history')
def history():
    if 'token_info' not in session:
        return redirect('/login')

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])

    track_list = []
    data = sp.current_user_recently_played(limit=50)

    for item in data['items']:
        track = item['track']
        track_list.append(track['name'] + ' - ' + track['artists'][0]['name'])

    return render_template('history.html', track_list=track_list)


@app.route('/playlists')
def playlists():
    if 'token_info' not in session:
        return redirect('/login')

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])

    playlists = []
    data = sp.current_user_playlists(limit=50)

    for index, item in enumerate(data['items']):
        playlists.append({'name': item['name'], 'index': index})

    return render_template('playlists.html', playlists=playlists)


@app.route('/playlist-tracks')
def playlist_tracks():
    if 'token_info' not in session:
        return redirect('/login')

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])

    index = int(request.args.get('index'))
    playlists = sp.current_user_playlists(limit=50)
    selected_playlist = playlists['items'][index]

    track_list = []
    tracks = sp.playlist_tracks(selected_playlist['id'])

    for item in tracks['items']:
        track_list.append(
            item['track']['name'] + ' - '
            + item['track']['artists'][0]['name'])

    return render_template('playlist-tracks.html', track_list=track_list)


@app.route('/top-artists')
def top_artists():
    if 'token_info' not in session:
        return redirect('/login')

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])

    artist_list = []
    data = sp.current_user_top_artists(limit=20)

    for item in data['items']:
        artist_list.append(item['name'])

    return render_template('top-artists.html', artist_list=artist_list)


@app.route('/top-tracks')
def top_tracks():
    if 'token_info' not in session:
        return redirect('/login')

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])

    track_list = []
    data = sp.current_user_top_tracks(limit=20)

    for item in data['items']:
        track_list.append(item['name'] + ' - ' + item['artists'][0]['name'])

    return render_template('top-tracks.html', track_list=track_list)


if __name__ == '__main__':
    app.run()
