# Tyler Brabham
# Steel Bridge autcad to FEDEASLAB converter.
# 

rawdxf = open('single_line.dxf')

line_index = 0
wait = True
for line in rawdxf:
	current_line = line.strip()
	if wait and current_line=='AcDbEntity':
		wait = False

	if wait:
		pass
	else:
		print line

	line_index += 1

rawdxf.close()