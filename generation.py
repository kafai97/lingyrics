import random
from analysis import bigram_model, monogram_model, pos_tagger, is_keyword
from geniuswrapper import get_songs
import syllables

def Generator(artrist_name):
	artrist = get_songs(artrist_name)
	lyrics = [line for song in artrist.values() for line in song.split('\n')]
	bigram = bigram_model(lyrics)
	monogram = monogram_model(lyrics)

	def weighted_pick(freq_dict):
		total = sum(v for k, v in freq_dict.items())
		pick = random.randint(0, total-1)
		accum = 0
		for k, v in freq_dict.items():
			accum += v
			if accum > pick:
				return k

	def replace(lyrics):
		text_pos = pos_tagger(lyrics)
		result = []
		for i, word_pos_pair in enumerate(text_pos):
			word, pos = word_pos_pair
			prev, _ = text_pos[i-1] if i>0 else word_pos_pair
			syllables_count = syllables.estimate(word)
			try:
				if i > 0 and pos in bigram.get(prev, ''):
					temp_dict = {w: count for w, count in bigram[prev][pos].items() 
							if syllables_count is syllables.estimate(w) and w not in ['’', '”']}
					word_dict = temp_dict if temp_dict else bigram[prev][pos]
				else:
					temp_dict = {w: count for w, count in monogram[pos].items() 
						if syllables_count is syllables.estimate(w) and w not in ['’', '”']}
					word_dict = temp_dict if temp_dict else monogram[pos]

				result += [weighted_pick(word_dict)]
			except:
				result+=[word]
		return ' '.join(result)

	def mixin(target_song):
		return [line if is_keyword(line) else replace(line).capitalize() for line in target_song]

	return mixin