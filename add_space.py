def add_space(filename):
	path = './tmp/'+filename+'.txt'
	l = []	
	f = open(path,'r')
	aa = f.readlines()
	f.close()
	for i in range(1,len(aa)):
		s1 = aa[i-1].split()[0]
		s2 = aa[i].split()[0]
		if not(s1 == s2):
			l.append(i)
	for i in l[::-1]:
		aa.insert(i,'\n')
	path = './'+filename+'_gnuplt.txt' 
	f = open(path,'w')
	f.writelines(aa)
	f.close()


		
