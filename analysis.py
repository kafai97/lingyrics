import nltk, string

def is_punctuation(word):
	return word in string.punctuation

def is_keyword(lyrics):
	return lyrics.startswith('[') and lyrics.endswith(']')

def pos_tagger(sentence):

	def pos_changer(pos):
		pos_dict = {}
		pos_dict['P', 'N'] = 'n'
		pos_dict['A', 'J'] = 'a'
		pos_dict['V'] = 'v'
		return pos_dict.get(pos[0], '')

	lemmatizer = nltk.stem.WordNetLemmatizer()
	words = nltk.tokenize.word_tokenize(sentence)
	words = [word if word is 'I' else word.lower() for word in words]
	words_with_pos = nltk.pos_tag(words)
	tagged = [(lemmatizer.lemmatize(word, pos=pos_changer(pos))
		if pos_changer(pos) else (lemmatizer.lemmatize(word)), pos)
		for word, pos in words_with_pos if "'" not in word]
	return tagged

def bigram_model(lyrics):
	pos_text = [pos_tagger(line) for line in lyrics if not is_keyword(line)] # remove lines of keyword tag
	bigram_dict = {}
	for line in pos_text:
		bigram_words = [(line[i], line[i+1]) for i in range(len(line)-1)]
		for current_word, next_word in bigram_words:
			(curr, curr_pos) = current_word
			(next, next_pos) = next_word

			if curr in bigram_dict:
				bigram_dict[curr]['pos'].add(curr_pos)
			else:
				bigram_dict[curr] = {'pos': set(curr_pos)}
				
			if next_pos not in bigram_dict[curr]:
				bigram_dict[curr][next_pos] = {next: 1}
			elif next not in bigram_dict[curr][next_pos]:
				bigram_dict[curr][next_pos][next] = 1
			else:
				bigram_dict[curr][next_pos][next] += 1

	return bigram_dict

def monogram_model(lyrics):
	pos_text = [pos_tagger(line) for line in lyrics if not is_keyword(line)]
	monogram_dict = {}
	for line in pos_text:
		for (word, pos) in line:
			if pos not in monogram_dict:
				monogram_dict[pos] = {word: 1}
			elif word not in monogram_dict[pos]:
				monogram_dict[pos][word] = 1
			else:
				monogram_dict[pos][word] += 1

	return monogram_dict
