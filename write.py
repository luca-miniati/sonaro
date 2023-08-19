import time

import pyautogui

# Sleep for a few seconds before starting
time.sleep(5)

code = """
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
    
for item in data['items']:
playlists.append(item['name'])

return render_template('playlists.html', playlists=playlists)

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
"""

# Type each character with a delay between keystrokes
for char in code:
    pyautogui.write(char)
    time.sleep(0.001)  # Adjust the delay as needed