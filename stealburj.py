# Tyler Brabham
# Steel Bridge autcad to FEDEASLAB converter.
# 

rawdxf = open('single_line.dxf')
dxf_list = [line.strip() for line in rawdxf]
rawdxf.close()

#
current_index = 0
start_index = 0
end_index = 0
wait = True
for line in dxf_list:
	current_line = line.strip()
	if wait and current_line=='LINE':
		start_index = current_index
		wait = False

	if wait:
		pass
	else:
		print current_line

	if not(wait) and current_line=='ENDSEC':
		end_index = current_index
		break

	current_index += 1

print start_index, end_index
print dxf_list[start_index], dxf_list[end_index]
