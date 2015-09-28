import numpy as np

aa = np.loadtxt('new_body_result.txt')
cc = np.loadtxt('new_surface_result.txt')
#bb = np.loadtxt('fort.201').astype('int')


pos = 3
ref = min(aa[:,pos])

print ref

node_set = set()
elem_set = set()
offset = 225

for i in range(aa.shape[0]):
	if (abs(aa[i,pos] - ref) < 1e-5):
		node_set.add(int(aa[i,0])) 
		

for i in range(cc.shape[0]):
	if (abs(cc[i,pos] - ref) < 1e-4):
		node_set.add(int(cc[i,0]))
###=======================================


grid = []
print node_set,len(node_set)

for i in range(bb.shape[0]):
	node_list = bb[i,1:9].tolist()
	print node_list
	if(node_set.issuperset(set(node_list))):
		print node_list
		elem_set.add(bb[i,0])
print bb[0,:],bb.shape
print elem_set,len(elem_set)


for i in node_set:
	idn = i - offset -1	
	grid.append((aa[idn,1],aa[idn,2],aa[idn,3]))



grid.sort()

cc = np.matrix(grid)
np.savetxt('matrix_body.txt',cc,fmt = '%12.4f')

