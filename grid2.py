import numpy as np
import add_space as adf
import potential as pt
import sfunc as sf
#---------0-----------1-------2------3-------4---------5-------
#-------node id------x--------y------z-----unknown---exact
aa = np.loadtxt('./input/new_body_result.txt')
cc = np.loadtxt('./input/new_surface_result.txt')
bb = np.loadtxt('./input/fort.201').astype('int')

c_set = {1,2,3}
pos = 2 #y
c_set.remove(pos)
ref = min(aa[:,pos])

print ref

node_set = set()
elem_set = set()
offset = 225 #225 node in surface mesh
grid = []
grid2 = []
grid3 = []
for i in range(aa.shape[0]):
	if (abs(aa[i,pos] - ref) < 1e-5):
		node_set.add(int(aa[i,0])) 
		grid.append((aa[i,1],aa[i,2],aa[i,3]))
		if pos == 2:
			grid2.append([aa[i,1],aa[i,4],aa[i,3]])

for i in range(cc.shape[0]):
	if (abs(cc[i,pos] - ref) < 1e-4):
		node_set.add(int(cc[i,0]))
		grid.append((cc[i,1],cc[i,2],cc[i,3]))
		if pos == 2:
			grid2.append([cc[i,1],cc[i,4],cc[i,3]])
		#pass
###=======================================
#print node_set,len(node_set)

# this is prepared for call dinp, need to change to be more versatile
pt.cal_p.amp = .5
pt.cal_p.h = -120.
pt.cal_p.wk = 1.5
pt.cal_p.timerk = 0. 
pt.cal_p.w1 = 3.83543
pt.cal_p.beta = 0.
pt.cal_p.g = 9.81

# need sf array to get center point value
sf,dsf = sf.spfunc8(0,0)

elem_dict = {}

for i in range(bb.shape[0]):
	node_list = bb[i,1:9].tolist()
	if(node_set.issuperset(set(node_list))):
		elem_set.add(bb[i,0])
		elem_dict[bb[i,0]] = node_list


for i in elem_set:
	node_list = elem_dict[i]
	print node_list
	# get node list
	fst = node_list[0]
	sec = node_list[4]
	if fst <= offset:
		fst_pos = cc[fst-1,1:4]
	else:
		fst_pos = aa[fst-offset-1,1:4]
	
	if sec <= offset:
		sec_pos = cc[sec-1,1:4]
	else:
		sec_pos = aa[sec-offset-1,1:4]
	# get corresponding node index for 1st and 5th node
	tmp = [0,0,0]
	print "==================",fst_pos,sec_pos	
	for j in c_set:
		print j
		tmp[j-1] = 0.5*(fst_pos[j-1]+sec_pos[j-1])
		# get cntr pt x,y position
	new_v = 0.
	# initialization for new_value
	

	sf_p = [0. for i in range(8)]
	for j in range(8):
		if node_list[j] <= offset:
			sf_p[j] = cc[fst-1,4]
		else:
			sf_p[j] = aa[fst-offset-1,4]
	
	
	new_v = np.dot(sf,sf_p)
	# calc new_v use sf 
	
	if pos == 2:
		v2 = pt.cal_p.poxy(tmp[0],ref,tmp[2])
		# get exact value use dinp in teng's lib
		grid.append((tmp[0],ref,tmp[2]))
		grid2.append([tmp[0],new_v,tmp[2]])
		grid3.append((tmp[0],v2,tmp[2]))
	if pos == 1:
		v2 = pt.cal_p.poxy(ref,tmp[1],tmp[2])
		# get exact value use dinp in teng's lib
		grid.append((ref,tmp[1],tmp[2]))
		grid2.append([new_v,tmp[1],tmp[2]])
		grid3.append((v2,tmp[1],tmp[2]))
	if pos == 3:
		v2 = pt.cal_p.poxy(tmp[0],tmp[1],ref)
		# get exact value use dinp in teng's lib
		grid.append((tmp[0],tmp[1]),ref)
		grid2.append([tmp[0],tmp[1],new_v])
		grid3.append((tmp[1],tmp[2],v2))

grid2 = np.matrix(grid2)
e = grid2[:,1]
grid2[:,1] = grid2[:,2]
grid2[:,2] = e
grid2 = grid2.tolist()
grid.sort()
grid2.sort()

cc = np.matrix(grid)
dd = np.matrix(grid2)
np.savetxt('./tmp/matrix_body.txt',cc,fmt = '%12.4f')
np.savetxt('./tmp/matrix_body_computed.txt',dd,fmt = '%12.4f')
adf.add_space('matrix_body_computed')
adf.add_space('matrix_body')
