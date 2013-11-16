#Bridge Class
#Tyler Brabham

class Bridge():
	'''Overal bridge. Stores nodes and connection data.
	'''
	nodes = None
	connections = None

	def get_connections():
		return self.connections

	def get_nodes():
		return self.nodes

class Node():
	'''Stores data for x,y,z coordinates and boundary constraints.
	'''
	position = None
	bounconstrains = None

	def __init__(self, x, y, z):
		self.position = (x,y,z)

	def __init__(self, x, y, z, boun_x, boun_y, boun_z):
		self.position = (x,y,z)
		self.bounconstrains = (boun_x,boun_y,boun_z)

class Connection():
	'''Stores data for the node endpoints, as well as member type and element porperties
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

def main():
	print 'here'
	return None

if __name__=='__main__':
	main()