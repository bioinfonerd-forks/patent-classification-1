import os
import pandas as pd
import numpy as np


from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV


directory = '/Users/mainuser/Documents/Studium/Text_Mining_Seminar/preprocessed_dataset/'
path_split = 'preprocessed_dataset/'


def import_data(label_level):
	
	result_df =  pd.DataFrame(columns = ['documents', 'targets'])
	
	for root, dirs, files in os.walk(directory):

		for file_ in files:
			
			if '.txt' in file_:
			
				path = os.path.join(root, file_)
			
				label_string = root.split(path_split)[1]
				label_level_list = label_string.split('/')
			
				label = ''
				# ist das konsistent mit dem aufbau der ipc klassifikation ?
				for i in range(0, label_level):
					label += label_level_list[i]  
			
				document = open(path, encoding="utf-8", errors='ignore').read()
			
				df_entry = {'documents': document, 'targets': label}
				result_df = result_df.append(df_entry, ignore_index=True)
			
	return result_df
	

	
def encode_targets(df):
	
	df['targets'] = df['targets'].astype('category')
	target_names = df['targets'].cat.categories
	df['targets'] = df['targets'].cat.codes
	
	return df, target_names
	
	
def create_classifier_pipeline(type, gs_parameters):
	
	# Create Classifier Pipeline
	if type == "nb":
		clf_pipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
	
	elif type == 'svm':
		clf_pipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SGDClassifier())])
	
	
	# Apply GridSearch within given parameter range to find the best classifier parameter setting	
	gs_clf_pipeline = GridSearchCV(clf_pipeline, gs_parameters)
	
	return gs_clf_pipeline
	
	


############### ML Model Code ######################	
				
# Importing data and encoding target values		
df = import_data(2)
df, target_names = encode_targets(df)

X = df['documents']
y = df['targets']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, shuffle=True)

# Define GridSearch parameters and create optimized classifer pipeline
gs_parameters = {'tfidf__use_idf': (True, False),'clf__alpha': (1e-2, 1e-3)}
clf = create_classifier_pipeline('nb', gs_parameters)
clf.fit(X_train, y_train)

predicted = clf.predict(X_test)
print(np.mean(predicted == y_test))
