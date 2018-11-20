from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from textblob.wordnet import ADV, NOUN, VERB, ADJ
from contractions import fix

"""	scipt may produce error messages in regards to nltk
	run python in terminal, then import nltk and run nltk.download;
	in addition deprecate warnings may occur if anaconda is installed	"""

f = open('/Users/paozer/Documents/patent-classification/AU9700836_18061998.txt', 'r+', encoding='utf-8')

ipc = f.readline().split()
text = f.read()

f.close()

# remove brakets 

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
	punctuation = ['.', ',', '?', '!', ';', "'", '"', ':', '(', ')']

	for word in words:		
		if word not in punctuation:
			new_words.append(word)
	
	return new_words

def to_lowercase(words):
	new_words = []

	for word in words:
		new_words.append(word.lower())
	
	return new_words

# lemmatization
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
			print('KeyError on tag @ ', word[0])
		
	return new_words

print("> removing contractions")
text = replace_contractions(text)
print("> tokenising text")
words = tokenise_text(text)
print("> removing numbers")
words = remove_numbers(words)
print("> removing stopwords")
words = remove_stopwords(words)
print("> remove punctuation")
words = remove_punctuation(words)
print("> to lowercase")
words = to_lowercase(words)
print("> lemmatizing")
words = lemmatize(words)
print(words)
