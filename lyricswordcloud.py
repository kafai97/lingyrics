from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
from geniuswrapper import get_songs
from analysis import is_keyword

def create_word_cloud(lyrics, artrist):
   maskArray = np.array(Image.open(f'img/{artrist}.png'))
   cloud = WordCloud(background_color = "white", max_words = 200, mask = maskArray)
   cloud.generate(lyrics)
   cloud.to_file(f'wordcloud/{artrist}.wordcloud.png')

def mask(sent):
	sent = sent.replace('-', ' ')
	sent = sent.replace(',', ' ')
	words = sent.lower().split()
	ban = ['oo', 'oh', 'wow', 'la', 'yeah']
	return ' '.join([word for word in words if word not in ban])

def make_lyrics_wordcloud(artrist):
	coldplay = get_songs(artrist)

	lyrics = '\n'.join([mask(line) 
			for song in coldplay.values() 
			for line in song.split('\n') 
			if not is_keyword(line)] )

	create_word_cloud(lyrics, artrist)