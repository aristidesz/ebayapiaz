from collections import defaultdict
from os import walk
from os import listdir
from os.path import isfile, join
from os import listdir
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
mypath = dir_path+"/sources/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def addcounter(fname):
	fopen = open('./sources/sourceslocal.in','w')
	with open(fname) as f:
		azlineno = 1
		for i, l in enumerate(f):
			if i != 0 and float((i-1) % 3) == 0:
				newstr = "  ".join((l.strip(),str(azlineno)+'\n'))
				fopen.write(newstr)
				azlineno += 1
				# import pdb;pdb.set_trace()
			else:
				fopen.write(l)
			pass
	# import pdb;pdb.set_trace()
	return i + 1,azlineno

def addFirstLine(azfile,NotoAdd):
	# import pdb;pdb.set_trace()
	with open(azfile, 'r') as original: data = original.read()
	with open(azfile, 'w') as modified: modified.write("{:<12}\n".format(int(NotoAdd)) + data)


file = 'sourceswa.in'
ii,azlineno = addcounter('./sources/'+file)