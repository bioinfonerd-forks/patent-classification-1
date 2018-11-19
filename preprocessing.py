import nltk
from nltk.corpus import stopwords
# from nltk.corpus.wordnet import ADJ, NOUN, VERB, ADJ
from textblob.wordnet import ADJ, NOUN, VERB, ADJ
from nltk.stem import WordNetLemmatizer
import contractions
import os
import string

f = open('/Users/paozer/Documents/patent-classification/AU0000046_03082000.txt', 'r+', encoding='utf-8')

ipc = f.readline().split()
text = f.read()

f.close()

# remove brakets 
# remove contractions
def replace_contractions(text):
	return contractions.fix(text)

# tokenizing
def tokenise_text(text):
	return nltk.word_tokenize(text)

# remove numbers
def remove_numbers(words):
	new_words = []
	for word in words:
		if not word.isdigit():
			new_words.append(word)
		else:
			pass

	return new_words
	
# stop words
def remove_stopwords(words):
	new_words = []
	for word in words:
		if word not in stopwords.words('english'):
			new_words.append(word)
		else:
			pass

# evtl. remove non ascii 
# remove punctuation
def remove_punctuation(words):
	new_words = []
	for word in words:
		foo = word.translate(None, string.punctuation)
		if foo != '':
			new_words.append(foo)
	return new_words

# lower case 
def to_lowercase(words):
	new_words = []
	for word in words:
		new_words.apppend(word.lower())
	return new_words

# lemmatization
def lemmatize(words):
	new_words = []

	tag_words = nltk.pos_tag(words)
	lemmatizer = WordNetLemmatizer()
	
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

	for word in tag_words:
		
		tag = word[1]
		try:
			new_tag = dic[tag]
			foo = lemmatizer.lemmatize(word[0], new_tag)
			new_words.append(foo)

		except KeyError:
			print('KeyError on tag @ ', word[0])
		
	return new_words

text = replace_contractions(text)
words = tokenise_text(text)
words = remove_numbers(words)
words = remove_stopwords(words)
words = remove_punctuation(words)
words = to_lowercase(words)
words = lemmatize(words)

print(words)
