import xml.etree.ElementTree as ET
import os

# paths for the patent xml files & directory for clean text files
directory = '/Users/paozer/Documents/python/xml_stuff/xml/'
clean_directory = '/Users/paozer/Documents/python/xml_stuff/clean_data/'

# first 6 files throw ParseError when running ET.parse(path)
# meaning a <cl> is not being closed properly
# 7th files throws TypeError running when findall('txt')
# because there is no patent desciption
faulty_files = ['SE0001854_05042001.xml', 'US0011521_07122000.xml',
				'IB9901525_16032000.xml', 'EP0012293_06062002.xml',
				'US0021074_15022001.xml', 'IT0000317_08022001.xml',
				'EP0010366_10052001.xml']

# os.walk() returns root and all directories/files of given path
for root, dirs, files in os.walk(directory):

	for file_ in files:
		path = os.path.join(root, file_)

		if '.xml' in path:
			
			if file_ in faulty_files:
				continue

			# constructs a tree of xml file and gets its root
			xml_tree = ET.parse(path)
			root_tree = xml_tree.getroot()

			# encoding is necessary to avoid UnicodeEncodeError
			f = open('%s%s.txt'
				% (clean_directory, file_[0:-4]), 'a', encoding='utf-8')

			# if only 1 class 'code' it's in  node before 'ips' ('ipcs')
			for elem in root_tree.findall('ipcs'):
				f.write(str(elem.attrib['mc']))

			for elem in root_tree:

				# additional classifications and description are 
				# at the same depth in the tree
				for subelem in elem.findall('ipc'):
					f.write(' ' + str(subelem.attrib['ic']))

				for subelem in elem.findall('txt'):
					f.write('\n' + subelem.text)

		else:
			continue

		f.close()
