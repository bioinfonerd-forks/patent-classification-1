from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from textblob.wordnet import ADV, NOUN, VERB, ADJ
from contractions import fix
from re import sub
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

# must improve! 
# check out clean text files where some punctuation has not been removed
def remove_punctuation(words):
	new_words = []
	punctuation = ['.', ',', '?', '!', ';', "'", '"', ':', '(', ')']
	regex = r"[,?!;':()]\w*"

	for word in words:		
		if word not in punctuation:
			new_word = sub(regex, "", word)
			new_words.append(new_word)

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
	words = remove_numbers(words)
	words = remove_stopwords(words)
	words = remove_punctuation(words)
	words = to_lowercase(words)
	words = lemmatize(words)


	return words# works

directory = '/Users/paozer/Documents/patent-classification/2_clean_text/'
clean_directory = '/Users/paozer/Documents/patent-classification/3_clean_feature/'

for file in os.listdir(directory):

	f_source = open(directory + file, 'r+', encoding='utf-8')

	ipc = f_source.readline().split()
	text = f_source.read()

	f_source.close()

	words = normalize(text)

	# think about how to store the data more efficiently
	# text files do not seem appropriate
	f_destination = open(clean_directory + file, 'w', encoding='utf-8')
	f_destination.write('\n'.join(ipc))
	f_destination.write('\n')
	f_destination.write('\n'.join(words))
