from geniuswrapper import get_lyrics
from generation import Generator
from lyricswordcloud import make_lyrics_wordcloud

artrists = ['Coldplay', 'Luke Bryan']
generators = {artrist: Generator(artrist) for artrist in artrists}

def write_song(artrist, target_song):
	target_lyrics = get_lyrics(target_song[0], target_song[1])
	new_song = generators[artrist](target_lyrics.split('\n'))
	new_song = '\n'.join(new_song)
	with open(f'result/{target_song[0].lower()}-{artrist.lower()}.txt', mode='w') as file:
		file.writelines(new_song)

target_song = ('Dancing Queen', 'ABBA')
for artrist in artrists:
	make_lyrics_wordcloud(artrist)

write_song('Coldplay', target_song)
write_song('Luke Bryan', target_song)

target_song = ('The Scientist', 'Coldplay')
write_song('Coldplay', target_song)

target_song = 'Play It Again', 'Luke Bryan'
write_song('Luke Bryan', target_song)
