
def parse_cmd_line(argv):
	i = 1
	input_file = None
	output_file = None
	modify_layers = False
	while i<len(argv):
		flag = argv[i]
		if flag=='-i':
			input_file = argv[i+1]
			if output_file==None:
				output_file = input_file
			i+=2
		elif flag=='-o':
			output_file = argv[i+1]
			i+=2
		elif flag=='-m':
			modify_layers = True
		else:
			print 'Unrecognized command '+flag
			sys.exit(0)

	return (input_file, output_file, modify_layers)

def get_layers(filename,dxf_list):
	'''Finds all layers in the dxf_list and asks user which layers to keep
	'''
	layer_table = {}

	i = 0
	while i<len(dxf_list):
		line = dxf_list[i].strip()
		if line=='LINE':
			layer = dxf_list[i+8].strip()
			if layer in layer_table:
				pass
			else:
				layer_table[layer] = 0
			i += 23
		else:
			i += 1

	#get user input to determine which layers to import
	print "\nWould you like to import all layers?[y/n] "
	all_layers = raw_input()=='y'

	if all_layers==False:
		new_layers = {}
		for layer in layer_table:
			import_layer = False
			print "\nWould you like to import layer "+layer+"? [y/n]"
			import_layer = raw_input()=='y'
			if import_layer==True:
				new_layers[layer] = 0

		return list(new_layers)
	else:
		return list(layer_table)