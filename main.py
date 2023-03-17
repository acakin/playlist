from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Please type the date in YYYY-MM-DD format: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")
songs = []
artists = []
songs_name = soup.select("html body div main div div div div div div div ul li ul li h3")
artist_name = soup.select("html body div main div div div div div div div ul li ul li span")
for song in songs_name:
    songs.append(song.get_text())
for artist in artist_name:
    artists.append(artist.get_text())

songs = [song.replace('\t', '').replace('\n', '') for song in songs]
artists = [artist.replace('\t', '').replace('\n', '') for artist in artists]
new_artists = []
for num in range(len(artists)):
    if num % 7 == 0:
        new_artists.append(artists[num])
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="************************",
        client_secret="*******************",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for num in range(100):
    result = sp.search(q=f"{songs[num]} {new_artists[num]}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{songs[num]} by {new_artists[num]} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
