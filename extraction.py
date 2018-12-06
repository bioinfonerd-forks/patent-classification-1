import xml.etree.ElementTree as ET
import os


def extract_xml(root, file_):
	
	ipcs = []
	text = ""
	
	path = os.path.join(root, file_)

	# constructs a tree of xml file and gets its root
	xml_tree = ET.parse(path)
	root_tree = xml_tree.getroot()

	# if only 1 classification 'code' it's in node before 'ips' ('ipcs')
	for elem in root_tree.findall('ipcs'):
		ipcs.append(str(elem.attrib['mc']))

	for elem in root_tree:

		# additional classifications and description are on same
		# level tree
		for subelem in elem.findall('ipc'):
			#f.write('\n' + str(subelem.attrib['ic']))
			ipcs.append(str(subelem.attrib['ic']))

		for subelem in elem.findall('txt'):
			text = subelem.text
			
	return ipcs, text
