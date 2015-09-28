# This program is implemented to generate sorted grid output for gnuplot display
# require file is 
#	1.surface result file 
#	2.node list file


import numpy as np
import potential as pt
import sfunc as sf
import add_space as adf
# surface node start from 1

aa = np.loadtxt('./input/new_surface_result.txt')
nl_m= np.loadtxt("./input/fort.200")
nl = nl_m.astype('int')

x = aa[:,1]# x pos
y = aa[:,2]# y pos
z = aa[:,4]# computed result
exact = aa[:,5]# exact value

# Read existing mesh info
grid = [(x[i],y[i],z[i]) for i in range(len(x))]
grid2 = [(x[i],y[i],exact[i]) for i in range(len(x))]

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

for i in range(nl.shape[0]):
	node_list = nl[i,1:9]
	# get node list
	fst = node_list[0] - 1
	sec = node_list[4] - 1
	# get corresponding node index for 1st and 5th node
	new_x = 0.5*(aa[fst,1]+aa[sec,1])
	new_y = 0.5*(aa[fst,2] + aa[sec,2])
	# get cntr pt x,y position
	new_v = 0.
	# initialization for new_value
	for j in range(8):
		new_v += sf[j]*aa[node_list[j]-1,4]
	# calc new_v use sf 
	v2 = pt.cal_p.dinp(new_x,new_y,0)[-1]
	# get exact value use dinp in teng's lib
	grid.append((new_x,new_y,new_v))
	grid2.append((new_x,new_y,v2))
	
# Sort grid to get data in correct order for gnuplot
grid.sort()
grid2.sort()

# Output data
#	1. cacluted data mesh
#	2. surface mesh
# 	3. exact data mesh
cc = np.matrix(grid)
np.savetxt('./tmp/matrix_computed.txt',cc,fmt = '%12.4f')

cc[:,2] = 0.
np.savetxt('./tmp/mesh_saved.txt',cc,fmt = '%12.4f')

dd = np.matrix(grid2)
np.savetxt('./tmp/matrix_exact.txt',dd,fmt = '%12.4f')

adf.add_space('matrix_computed')
adf.add_space('mesh_saved')
adf.add_space('matrix_exact')
print "==================Data Output Finished==========================="




