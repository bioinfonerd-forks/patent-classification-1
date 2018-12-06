import os

import extraction
import preprocessing

directory = '/Users/mainuser/Dropbox/Seminar/working_dataset/'
clean_directory = '/Users/mainuser/Documents/Studium/Text_Mining_Seminar/preprocessed_dataset/'
path_split = 'working_dataset/'

# first 6 files throw ParseError when running ET.parse(path)
# meaning a <cl> is not being closed properly
# 7th files throws TypeError running when findall('txt')
# because there is no patent desciption
faulty_files = ['SE0001854_05042001.xml', 'US0011521_07122000.xml',
				'IB9901525_16032000.xml', 'EP0012293_06062002.xml',
				'US0021074_15022001.xml', 'IT0000317_08022001.xml',
				'EP0010366_10052001.xml']


def ensure_dir(file_path):
    dir = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)

counter = 0

# os.walk() returns root and all directories/files of given path
for root, dirs, files in os.walk(directory):

	for file_ in files:
		
		counter += 1

		print(counter, root, file_)

		if '.xml' in file_:

			if file_ in faulty_files:
				continue
				
			# Extracting and preprocessing xml file
			ipcs, text = extraction.extract_xml(root, file_)
			words = preprocessing.normalize(text)			
			
			# Writing preprocessed file into new directory with same structure
			new_path = clean_directory + root.split(path_split)[1] + '/'
			ensure_dir(new_path)
			f_destination = open('%s%s.txt' % (new_path, file_[0:-4]), 'a', encoding='utf-8')
			f_destination.write(' '.join(words))
			f_destination.close()
