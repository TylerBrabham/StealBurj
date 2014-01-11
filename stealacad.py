# Tyler Brabham
# Fall 2013

import sys
from acobjects import acobject
from parsers import parser

##########################
# Entry Point of Program #
##########################
def main(argv):
	'''Parses input, determines input name, output name, and layers.
	'''
	(input_file, output_file) = parser.parse_cmd_line(argv)

	#open the file and create the list of strings in the file
	rawdxf = open(input_file)
	dxf_list = [line.strip() for line in rawdxf]
	rawdxf.close()

	print "\nImporting from file "+input_file+' and outputting to file '+output_file

	#find all the layers in the input file, and create corresponding layer table 
	layers = parser.get_layers(input_file,dxf_list)
	print "\nImporting "+str(len(layers))+" layers"

	layer_table = {}
	for layer in layers:
		layer_table[layer] = []

	i = 0
	#Searches through raw list to find all nodes associated with a layer, stores lists in a table
	while i<len(dxf_list):
		line = dxf_list[i].strip()
		if line=='LINE':
			layer = dxf_list[i+8].strip()
			if layer in layer_table:
				layer_list = layer_table[layer]
				layer_list = layer_list + dxf_list[i:i+23]
				layer_table[layer] = layer_list
				i += 23
			else:
				i += 1
		else:
			i += 1

	print layer_table
	#Create a acadobject for this file data
	acadstructure = acobject.AutoCadObject(layer_table)

if __name__=="__main__":
	main(sys.argv)