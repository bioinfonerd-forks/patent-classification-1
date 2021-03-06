from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from textblob.wordnet import ADV, NOUN, VERB, ADJ
from contractions import fix
import os

"""	scipt may produce error messages in regards to nltk
	> run python in terminal, then import nltk and run nltk.download();
	> in addition deprecate warnings may occur if anaconda is installed	"""

def replace_contractions(text): #works
	return fix(text)

def tokenise_text(text): #works
	return word_tokenize(text)

def remove_numbers(words): #works
	new_words = []
	for word in words:
		if not word.isdigit():
			new_words.append(word)
		else:
			pass

	return new_words

def remove_stopwords(words): #works
	new_words = []
	for word in words:
		if word not in stopwords.words('english'):
			new_words.append(word)
		else:
			continue

	return new_words

# evtl. remove non ascii 

def remove_punctuation(words): # works maybe improve
	new_words = []
	punctuation = ['.', ',', '?', '!', ';', "'", '"', ':', '(', ')', '§', '$', '%']
    
	for word in words:
		# Remove pure punctuations
		if word not in punctuation:
			
			# Remove words containing punctuations
			p_flag = False
			for p in punctuation:
				
				if p in word:
					p_flag = True
			if not p_flag:
				new_words.append(word)
    
	
	return new_words

def to_lowercase(words):
	new_words = []

	for word in words:
		new_words.append(word.lower())
	
	return new_words # works

def lemmatize(words): # need to investigate words which throw KeyError
	
	tag_words = pos_tag(words) # seems to work correctly

	dic = {
		'JJ': ADJ,
		'JJR': ADJ, 
		'JJS': ADJ, 

		'RB': ADV, 
		'RBR': ADV, 
		'RBS': ADV,

		'NN': NOUN,
		'NNP': NOUN,
		'NNS': NOUN,
		'NNPS': NOUN,

		'VB': VERB,
		'VBG': VERB,
		'VBD': VERB,
		'VBN': VERB,
		'VBP': VERB,
		'VBZ': VERB
	}

	lemmatizer = WordNetLemmatizer()
	new_words = []

	for word in tag_words:
		tag = word[1]
		
		try:
			new_tag = dic[tag]
			lemmatized_word = lemmatizer.lemmatize(word[0], new_tag)
			new_words.append(lemmatized_word)

		except KeyError:
			# need to analyse 
			# print('KeyError on tag @ ', word[0]) 
			pass
		
	return new_words

def normalize(text):
	text = replace_contractions(text)
	words = tokenise_text(text)
	
	
	# artificially limit number of words
	words = words[:200]
	
	words = remove_numbers(words)
	words = remove_stopwords(words)
	words = remove_punctuation(words)
	words = to_lowercase(words)
	words = lemmatize(words)

	return words
