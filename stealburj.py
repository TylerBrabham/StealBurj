# Tyler Brabham
# Steel Bridge autocad to FEDEASLAB converter.
# Correctly finds the section in which a single group of lines is stated in the dxf file
# 

'''
TODO

Should probably make a lookup table for each xyz coordinate, so that I can quickly
look up node number. This should help when converting the file to MATLAB script.

Boundary is per node not per connection

Remove layer 0 and any other guide layers

Function to determine extra connections not specified in autocad due to lines being 
within some small tolerance of each other

Function to import individual layers at a time, or at least to organize and label 
layers near each other in the .m file.

Update the BOUN matrix creation

input output for filenames

store coordinates as floats instead of strings to reduce casting

Add error messages when receiving bad input
'''

import math
import sys

'''
Returns nodes and connection information, both as tables
'''
def build_connection_list(raw_list):
	#for now just going to use a 6-tuple, should probably make its own class later
	section = []

	node_count = 0
	nodes = {}
	indices = {}
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
				indices[node1] = (x1,y1,z1)
				connections[node1] = [] #list of connections

			if (x2,y2,z2) in nodes:
				node2 = nodes[(x2,y2,z2)]
			else:
				node_count += 1
				node2 = node_count
				nodes[(x2,y2,z2)] = node2
				indices[node2] = (x2,y2,z2)
				connections[node2] = [] #list of connections

			#connect the two nodes together in the connection table
			node_list = connections[node1]
			node_list.append(node2)
			connections[node1] = node_list #this might not be necessary

			i += 12
			conn_count += 1
		else:
			i+=1

	return (nodes,indices,connections,conn_count)

'''
Interpolates the line between nodes to look for any other connections that need to
be added. If it finds extra connections, it breaks the current connection and makes
two new ones. The process does not require the creation of any new nodes. Currently 
making the assumption that any node that crosses the path of a connection will satisfy
the linear equation. May need to do a kind of tolerance check instead.

'''
def nodes_from_intersection(nodes,indices,connections):
	#for each connection check all nodes that might pass through the line
	#continue the process until no change is made
	tol = .000001
	change = True

	#count of new connections made
	count = 0
	while change:
		#change back to True if find a new connection on this iteraton
		change = False

		new_connections = {}
		for key in connections:
			new_connections[key] = []

		for source in connections:
			conn_list = connections[source]
			(x1,y1,z1) = indices[source]

			x1 = float(x1)
			y1 = float(y1)
			z1 = float(z1)

			#try each connection to this node
			for drain in conn_list:
				(x2,y2,z2) = indices[drain]

				x2 = float(x2)
				y2 = float(y2)
				z2 = float(z2)

				vec1 = (x2-x1,y2-y1,z2-z1)

				#normalize
				v1 = (0,0,0)
				norm1 = vec1[0]*vec1[0]+vec1[1]*vec1[1]+vec1[2]*vec1[2]
				if norm1>0.0:
					length1 = math.sqrt(norm1)
					v1 = (vec1[0]/length1,vec1[1]/length1,vec1[2]/length1)

				#see if any intermediate nodes satisfy the equation of the line. If so, find
				#the closest one!
				min_len = float('inf')
				closest_node = None
				intersection = False
				for node in nodes:
					(x,y,z) = (float(node[0]),float(node[1]),float(node[2]))
					vec2 = (x-x1,y-y1,z-z1)

					v2 = (0,0,0)
					norm2 = vec2[0]*vec2[0]+vec2[1]*vec2[1]+vec2[2]*vec2[2]
					if norm2>0.0:
						length2 = math.sqrt(norm2)
						v2 = (vec2[0]/length2,vec2[1]/length2,vec2[2]/length2)

					#check dot prod is 1 and then update node connections if it is.
					dotprod = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
					if abs(1.0-dotprod)<tol and length2<length1 and length2<min_len:
						#then this new node is closer than the previous node, so it should
						#form a connection.
						intersection = True
						min_len = length2
						closest_node = node

				#Split current connection in two. source->closest_node, closest_node->drain
				if not(intersection):
					new_list = new_connections[source]
					new_list.append(drain)
					new_connections[source] = new_list
				else:
					change = True
					count += 1
					new_connections[source].append(nodes[closest_node])
					new_connections[nodes[closest_node]].append(drain)
		connections = new_connections
	return (connections,count)

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
	output.write('XYZ = zeros('+str(n)+',3)\n')

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
	output.write('BOUN = ones('+str(n)+',3);\n')
	output.write('BOUN(1,:) = [1, 1, 1]\n')
	output.write('\n')

	#create element name 
	output.write('[ElemName{1:'+str(conn_count)+'}] = deal('+"'Truss'"+');\n')
	output.write('\n')

	#create the model
	output.write('Model = Create_SimpleModel(XYZ,CON,BOUN,ElemName);\n')

	output.close()

i = 1
input_file = None
out_file = None
layers = []
while i<len(sys.argv):
	flag = sys.argv[i]
	if flag=='-i':
		input_file = sys.argv[i+1]
		output_file = input_file.repalce('.dxf','')+'.m'
		i+=2
	elif flag=='-o':
		output_file = sys.argv[i+1]
		i+=2
	elif flag=='-f':
		layers = sys.argv[i+1].split(',')
		i+=2

#open the file and create the list of strings in the file
rawdxf = open(input_file)
dxf_list = [line.strip() for line in rawdxf]
rawdxf.close()

#move through the input and determine the indices where all layers are specified.
current_index = 0
start_index = 0
end_index = 0
wait = True
for line in dxf_list:
	current_line = line.strip()
	if wait and current_line=='LINE':
		start_index = current_index
		wait = False

	if not(wait) and current_line=='ENDSEC':
		#found all layers, exit loop
		end_index = current_index
		break

	current_index += 1

# layer_data = {}
# #now find the particular layers needed. Should combine into previous loop
# line_list = []
# for i in range(start_index, end_index):
# 	line = dxf_list[i].strip()
# 	if line=='AcDbEntity':
# 		layer = dxf_list[i+2].strip()
# 		if layer in layers:
# 			line_list += dxf_list[i:i+24]
# 	else:
# 		i+=1 



#Produces the list of lines that make up this first section
(nodes,indices,connections,conn_count) = build_connection_list(dxf_list[start_index:end_index])

#Add intermediate connections if there are any
(connections,extra_count) = nodes_from_intersection(nodes,indices,connections)

#produces matlab script to generate the structure in FEDEASLAB
write_fedeaslab_script(nodes,connections,conn_count+extra_count)