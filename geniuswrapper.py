import lyricsgenius, pickle

def get_songs(artist_name, max_songs=30):
	path = f'data/{artist_name.lower()}-{max_songs}.songs'

	try:
		with open(path, mode='rb') as file:
			lyrics = pickle.load(file)

	except FileNotFoundError:
		genius_api_key = 'ROpo4PSBZYAUqeAQvnQOC07d9jiYqZkTllSzLprkNQ86IzaKmcqxqOujoFeSFWH0'
		api = lyricsgenius.Genius(genius_api_key)

		artist = api.search_artist(artist_name, max_songs=max_songs)
		lyrics = {song.title: api.search_song(song.title, artist.name).lyrics for song in artist.songs}

		with open(path, mode='wb') as file:
			pickle.dump(lyrics, file)

	return lyrics

def get_lyrics(song_title, artist_name):
	path = f'data/single.{song_title.lower()}.song'
	try:
		with open(path, mode='rb') as file:
			lyrics = pickle.load(file)
			
	except FileNotFoundError:
		genius_api_key = 'ROpo4PSBZYAUqeAQvnQOC07d9jiYqZkTllSzLprkNQ86IzaKmcqxqOujoFeSFWH0'
		api = lyricsgenius.Genius(genius_api_key)
		lyrics = api.search_song(song_title, artist_name).lyrics

		with open(path, mode='wb') as file:
			pickle.dump(lyrics, file)

		with open(f'data/{song_title.lower()}-origin.txt', mode='w') as file:
			file.write(lyrics)

	return lyrics