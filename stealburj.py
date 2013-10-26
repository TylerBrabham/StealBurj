# Tyler Brabham
# Steel Bridge autcad to FEDEASLAB converter.
# Correctly finds the section in which a single group of lines is stated in the dxf file

'''
TODO

Should probably make a lookup table for each xyz coordinate, so that I can quickly
look up node number. This should help when converting the file to MATLAB script.
'''

'''
Returns list of lines (stored as a 6-tuple, 3 indices for each xyz coordinate of each node).
Need to convert these to node and connectivity information.
'''
def build_section_list(raw_list):
	#for now just going to use a 6-tuple, should probably make its own class later
	section = []

	node_count = 0
	i = 0
	n = len(raw_list)
	while i<n:
		line = raw_list[i]

		if line=='AcDbLine':
			#then the next 12 indices will be coordinate name and coordinate position
			node_count += 1
			acadline = (tuple(raw_list[i+2:i+14:2]), node_count)
			section.append(acadline)
			i += 12
		else:
			i+=1

	return section


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
		end_index = current_index
		break

	current_index += 1

#Produces the list of lines that make up this first section
section = build_section_list(dxf_list[start_index:end_index])

print section