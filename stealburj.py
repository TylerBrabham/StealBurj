# Tyler Brabham
# Steel Bridge autocad to FEDEASLAB converter.

'''
TODO
#############################
Get MATLAB working on ubuntu or windows

Function to import individual layers at a time, or at least to organize and label 
layers near each other in the .m file.
	- Working prototype. Check correctness later

Update the BOUN matrix creation

Improve parser to be more robust to errors, and to alert user of errors

Consider using OOP to improve encapsulation, readability, organization

store coordinates as floats instead of strings to reduce casting

Make UI question and answer form

Fix layer issue. RIght now it makes new nodes when it should reuse previously
made nodes at the same xyz coordinate
'''

import sys
from acobjects import bridge
from parsers import parser
##########################
# Entry Point of Program #
##########################
def main(argv):
	'''Parses input, determines input name, output name, and layers.
	'''
	(input_file, output_file, modify_layers) = parser.parse_cmd_line(argv)

	#open the file and create the list of strings in the file
	rawdxf = open(input_file)
	dxf_list = [line.strip() for line in rawdxf]
	rawdxf.close()

	print "\nImporting from file "+input_file+' and outputting to file '+output_file

	if modify_layers==False:
		#find all the layers in the input file, and create corresponding layer table 
		layers = parser.get_layers(input_file,dxf_list)
		print "\nImporting "+str(len(layers))+" layers"

		layer_table = {}
		for layer in layers:
			layer_table[layer] = []

		i = 0
		#Searches through raw list to find all nodes associated with a layer, stores lists in a table
		while i<len(dxf_list):	#find all the layers in the input file, and create corresponding layer table 
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
				if layer in layer_table or all_layers==True:
					layer_list = layer_table[layer]
					layer_list = layer_list + dxf_list[i:i+23]
					layer_table[layer] = layer_list
					i += 23
				else:
					i += 1
			else:
				i += 1
			line = dxf_list[i].strip()
			if line=='LINE':
				layer = dxf_list[i+8].strip()
				if layer in layer_table or all_layers==True:
					layer_list = layer_table[layer]
					layer_list = layer_list + dxf_list[i:i+23]
					layer_table[layer] = layer_list
					i += 23
				else:
					i += 1
			else:
				i += 1
	else:
		pass

	#Create a bridge object for this file data
	steelbridge = bridge.Bridge(layers,dxf_list)
	
	# #build node and connection data for each layer and store in dictionary
	# node_connection_data = {}
	# total_nodes = 0
	# total_connections = 0
	# node_count = 0
	# for layer in layer_table:
	# 	(nodes,indices,connections,conn_count,node_count) = build_connection_list(layer_table[layer],node_count)
	# 	#Add intermediate connections if there are any
	# 	(connections,extra_count) = nodes_from_intersection(nodes,indices,connections)

	# 	#set this layer
	# 	node_connection_data[layer] = (nodes,connections)

	# 	total_nodes += len(nodes)
	# 	total_connections += (conn_count + extra_count)

	# #uses the layer table to create node and connection data and then write it to layer_table
	# write_fedeaslab_script(output_file,node_connection_data,total_nodes,total_connections)

if __name__=="__main__":
	main(sys.argv)