# Tyler Brabham
# Steel Bridge autcad to FEDEASLAB converter.
# Correctly finds the section in which a single group of lines is stated in the dxf file

'''
TODO

Should probably make a lookup table for each xyz coordinate, so that I can quickly
look up node number. This should help when converting the file to MATLAB script.
'''

'''
Returns nodes and connection information, both as tables
'''
def build_connection_list(raw_list):
	#for now just going to use a 6-tuple, should probably make its own class later
	section = []

	node_count = 0
	nodes = {}
	connections = {}
	conn_count = 0
	i = 0
	n = len(raw_list)
	while i<n:
		line = raw_list[i]

		if line=='AcDbLine':
			#then the next 12 indices will be coordinate name and coordinate position
			(x1,y1,z1,x2,y2,z2) = tuple(raw_list[i+2:i+14:2])

			#Determine if either of the two nodes have been used before. Else, increment node number
			if (x1,y1,z1) in nodes:
				node1 = nodes[(x1,y1,z1)]
			else:
				node_count += 1
				node1 = node_count
				nodes[(x1,y1,z1)] = node1
				connections[node1] = [] #list of connections

			if (x2,y2,z2) in nodes:
				node2 = nodes[(x2,y2,z2)]
			else:
				node_count += 1
				node2 = node_count
				nodes[(x2,y2,z2)] = node2
				connections[node2] = [] #list of connections

			#connect the two nodes together in the connection table
			node_list = connections[node1]
			node_list.append(node2)
			connections[node1] = node_list #this might not be necessary

			#connect the second node to the first node as well. Might not be necessary
			# node_list = connections[node2]
			# node_list.append(node1)
			# connections[node2] = node_list

			i += 12
			conn_count += 1
		else:
			i+=1

	return (nodes,connections,conn_count)

'''
Takes in the nodes as a dict, connections as a dict, and connection count
and generates the .m file with format expected by FEDEASLab. No Special 
information right now like boundary conditions
'''
def write_fedeaslab_script(nodes,connections,conn_count):
	output = open('testfile.m','w+')

	#clear memory 
	output.write('CleanStart;\n\n')

	#First create the XYZ table. One for each node
	n = len(nodes)
	output.write('XYZ = zeroes('+str(n)+',3)\n')

	for (x,y,z) in nodes:
		index = nodes[(x,y,z)]
		output.write('XYZ('+str(index)+',:) = ['+str(x)+','+str(y)+','+str(z)+'];\n')

	output.write('\n')

	#Now create the connection table.
	count = 1
	output.write('CON = zeros('+str(conn_count)+',2)\n')
	for node in connections:
		connect_list = connections[node]
		for drain in connect_list:
			output.write('CON('+str(count)+',:) = ['+str(node)+','+str(drain)+'];\n')
			count += 1

	output.write('\n')

	#create boundary information for nodes.
	output.write('BOUN = ones('+str(conn_count)+',2);\n')
	output.write('BOUN(1,:) = [1, 1]\n')
	output.write('\n')

	#create element name 
	output.write('[ElemName{1:'+str(conn_count)+'}] = deal('+"'DeckTruss'"+');\n')
	output.write('\n')

	#create the model
	output.write('Model = Create_SimpleModel(XYZ,CON,BOUN,ElemName);\n')

	output.close()

#Parses input and determines the first section of LINE data
rawdxf = open('DSASB_1.dxf')
dxf_list = [line.strip() for line in rawdxf]
rawdxf.close()

current_index = 0
start_index = 0
end_index = 0
wait = True
for line in dxf_list:
	current_line = line.strip()
	if wait and current_line=='LINE':
		start_index = current_index
		wait = False

	# if wait:
	# 	pass
	# else:
	# 	print current_line

	if not(wait) and current_line=='ENDSEC':
		#end section, reset process to the next line and create this section
		end_index = current_index
		break

	current_index += 1

#Produces the list of lines that make up this first section
(nodes,connections,conn_count) = build_connection_list(dxf_list[start_index:end_index])

#produces matlab script to generate the structure in FEDEASLAB
write_fedeaslab_script(nodes,connections,conn_count)

print nodes,
print connections