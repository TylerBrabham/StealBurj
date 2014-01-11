#Bridge Class
#Tyler Brabham

class Bridge():
	'''Overall bridge. Stores nodes and connection data.
	'''
	nodes = None
	connections = None
	layers = []

	def __init__(layers, dxf_list):
		'''List of layers from which to pull nodes/connections, and dxf_list
		the list of raw strings consisting of xyz values.
		'''

	def get_connections():
		return self.connections

	def get_nodes():
		return self.nodes

	def set_nodes(nodes):
		self.nodes = nodes

	def set_connections(connections):
		self.connections = connections

	def build_connection_list(raw_list,node_count):
	'''Returns nodes and connection information, both as tables
	'''
	section = []

	#node_count = 0
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

	return (nodes,indices,connections,conn_count,node_count)

class Node():
	'''Stores data for x,y,z coordinates and boundary constraints. Also stores all
	the layers in which the Node participates.
	'''
	position = None
	bounconstraints = None
	layers = []

	def __init__(self, x, y, z):
		self.position = (x,y,z)

	def __init__(self, x, y, z, boun_x, boun_y, boun_z):
		self.position = (x,y,z)
		self.bounconstraints = (boun_x,boun_y,boun_z)

class Connection():
	'''Stores data for the node endpoints, as well as member type and element porperties. Also stores 
	all the layres in which the Connection participates.
	'''
	source = None
	drain = None
	elemproperties = None

	def __init__(self, source, drain):
		self.source = source
		self.drain = drain

	def __init__(self, source, drain, elemproperties):
		self.source = source
		self.drain = drain
		self.elemproperties = elemproperties

	def get_elemproperties():
		return self.elemproperties

	def get_edge():
		return (self.source,self.drain)

class ElementProperties():
	size = None

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

def nodes_from_intersection(nodes,indices,connections):
	'''Interpolates the line between nodes to look for any other connections that need to
	be added. If it finds extra connections, it breaks the current connection and makes
	two new ones. The process does not require the creation of any new nodes. Currently 
	making the assumption that any node that crosses the path of a connection will satisfy
	the linear equation. May need to do a kind of tolerance check instead.
	'''
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

def write_fedeaslab_script(output_file,node_connection_data,total_nodes,total_connections):
	'''Takes in the nodes as a dict, connections as a dict, and connection count
	and generates the .m file with format expected by FEDEASLab. No Special 
	information right now like boundary conditions
	'''
	output = open(output_file,'w+')

	#clear memory. Clearnstart should be sufficient, but for now do all of them.
	output.write('clear all;\n')
	output.write('close all;\n')
	output.write('clc;\n')
	output.write('CleanStart;\n\n')

	#First initialize the tables.
	output.write('XYZ = zeros('+str(total_nodes)+',3);\n')
	output.write('CON = zeros('+str(total_connections)+',2);\n\n')

	conn_count = 1
	for layer in node_connection_data:
		output.write('%'+'Start of '+layer+'\n')

		(nodes,connections) = node_connection_data[layer]
		for (x,y,z) in nodes:
			index = nodes[(x,y,z)]
			output.write('XYZ('+str(index)+',:) = ['+str(x)+','+str(y)+','+str(z)+'];\n')

		output.write('\n')

		#Now create the connection table.
		#output.write('CON = zeros('+str(conn_count)+',2)\n')
		for node in connections:
			connect_list = connections[node]
			for drain in connect_list:
				output.write('CON('+str(conn_count)+',:) = ['+str(node)+','+str(drain)+'];\n')
				conn_count += 1

		output.write('%'+'End of '+layer+'\n')
		output.write('\n')

	#create boundary information for nodes.
	output.write('BOUN = ones('+str(total_nodes)+',3);\n')
	output.write('BOUN(1,:) = [1, 1, 1];\n')
	output.write('\n')

	#create element name 
	output.write('[ElemName{1:'+str(total_connections)+'}] = deal('+"'Truss'"+');\n')
	output.write('\n')

	#create the model
	output.write('Model = Create_SimpleModel(XYZ,CON,BOUN,ElemName);\n')

	output.close()

if __name__=='__main__':
	main()


