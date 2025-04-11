from os import listdir
from os.path import isfile, join
import os 
from itertools import cycle
import re
from datetime import datetime
import calendar
from collections import Counter
import shutil
import os 
from itertools import tee, islice, chain, izip
import json
from math import floor
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator
from numpy import linspace, zeros, array
import numpy as np
from mayavi.mlab import *
from mpl_toolkits.basemap import Basemap

minlat = -30
maxlat = 30
minlon = 75
maxlon = 165
mindepth = 1.5
maxdepth = -1600

r=30
l=40
lo=60

dicingNS = 20
dicingEW = 20

rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

fDInterface = open('./files/gridint1.z','r')
linesID = fDInterface.readlines()
# fileR = 'AZF-P-S-ISC-EHB.dat'
fileR = 'AZF-P-S-ISC-EHB.dat'


try:
    mode=int(raw_input('Get interface from crust1.0 (1) or FMTOMO (2):'))
except ValueError:
    print "Not a number"

try:
    pltswitch=int(raw_input('Plot crust (1) or not (2):'))
except ValueError:
    print "Not a number"

try:
    azphaseswitch=raw_input('P-wave (p) or s-wave (s):')
except ValueError:
    print "Not a number"

if azphaseswitch == 'p':
	phase1 = 'P'
	phase2 = 'Pn'
	phnot = 'p'
elif azphaseswitch == 's':
	phase1 = 'S'
	phase2 = 'Sn'
	phnot = 's'
else:
	exit()

if mode == 2:
	idcounter = 0
	interfaceDepthDicing = {}
	arrMlab = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1),dtype=float)
	for j in xrange(0,(lo-1)*dicingEW+1):
		reallon = (j)*rlon/dicingEW+minlon
		for i in xrange(0,(l-1)*dicingNS+1):
			reallat = (i)*rlat/dicingNS+minlat
			azrdepth = float(linesID[idcounter])
			arrMlab[i][j] = azrdepth*5
			interfaceDepthDicing[str(round(reallat,1))+","+str(round(reallon,1))] = azrdepth
			idcounter += 1

	interfaceDepth = interfaceDepthDicing
	# import pdb;pdb.set_trace()
elif mode == 1:
	fInterface = open('./files/crust1.0I304060.in','r')
	linesI = fInterface.readlines()
	r = r+2
	l = l+2
	lo = lo+2
	lat_lst = []
	interfaceDepth = {}
	icounter = 0
	dd_lst = []
	for j in xrange(0,l):
		reallat = (j)*rlat-rlat+minlat
		lon_lst = []
		depth_lst = []
		for z in xrange(0,lo):
			reallon = (z)*rlon-rlon+minlon
			lon_lst.append(round(reallon,1))
			depth_lst.append(float(linesI[icounter].strip()))
			icounter += 1

		lat_lst.append(round(reallat,1))
		dd_lst.append(depth_lst)


	x = lon_lst
	y = lat_lst
	xx, yy = np.meshgrid(x, y)
	z = dd_lst
	f = interpolate.interp2d(x, y, z, kind='cubic')

	xnew = np.arange(min(lon_lst), max(lon_lst), 0.1)
	ynew = np.arange(min(lat_lst), max(lat_lst), 0.1)
	xnew = np.around(xnew,decimals=1)
	ynew = np.around(ynew,decimals=1)
	znew = f(xnew, ynew)
	z = np.array(z)
	for laa in range(len(ynew)):
		for loo in 	range(len(xnew)):
			if ynew[laa] == -0.0:
				ynew[laa] = 0.0
				
			interfaceDepth[str(ynew[laa])+","+str(xnew[loo])] = znew[laa][loo]

else:
	exit()
# import pdb;pdb.set_trace()

if pltswitch == 1:
	azsurf = surf(arrMlab)
	show()
elif pltswitch == 2:
	pass
else:
	exit()

dd = json.load(open("./files/azcrust1.0Depthv3.txt"))
crust1d = dd['crust1.0']


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

print "START", datetime.now().time(), datetime.now().date()



dir_path = os.path.dirname(os.path.realpath(__file__))
def addFirstLine(azfile,NotoAdd):
	# import pdb;pdb.set_trace()
	with file(azfile, 'r') as original: data = original.read()
	with file(azfile, 'w') as modified: modified.write("{:<12}\n".format(int(NotoAdd)) + data)

myevents=[]

with open('./'+fileR) as openfileobject:
	flag = True
	for line in openfileobject:
		data = line.replace(" ","")
		data = data.split(",")
		myevents.append(data[0])

if os.path.exists('sources'):
	shutil.rmtree('sources')
	os.makedirs('sources')
else:
    os.makedirs('sources')

fcorrect_events=open('./P-wave_correct.dat', 'w')

x =0

fopen = open('sources/sourceswa.in','w')
# print mytemp
sta_list = []
reporter_lst = []
arrival_list = []
myitems = []
eventid_lst = []
# fopen.write("		%s\n" % len(myevents))
no_of_events = 0
# print myevents

with open('./'+fileR) as openfileobject:
	flag = True
	for line, j in zip(openfileobject, previous_and_next(myevents)):
	# for line in openfileobject:
		data = line.replace(" ","")
		data = data.split(",")
	# for previous, item, nxt in previous_and_next(myevents):
		item = j[1]
		nxt = j[2]
		previous = j[0]
		# print sample_data
		eventid = data[0]
		reporter = data[1]
		station = data[2]
		phase = data[3]
		oarrivaldateno = [data[4],data[5],data[6]]
		oarrivaltimeno = [data[7],data[8],data[9]]
		arrivaldateno = [data[10],data[11],data[12]]
		arrivaltimeno = [data[13],data[14],data[15]]
		distance = data[16]
		latitude = data[17]
		longitude = data[18]
		elevation = data[19]
		origin_latitude = data[20]
		origin_longitude = data[21]
		origin_depth = data[22]
		magnitude = data[23]
		residual = data[24]
		channel = data[25]
		#import pdb;pdb.set_trace()
		# if station not in sta_list + reporter_lst:
		# 	sta_list.append(station)
		# 	reporter_lst.append(reporter)
		try:
			origin_depth = float(origin_depth) * (-1)
		except:
			import pdb; pdb.set_trace()


		timesecond = arrivaltimeno[2].split(".")
		otimesecond = oarrivaltimeno[2].split(".")

		arrival_datetime = datetime(int(arrivaldateno[0]), int(arrivaldateno[1]), int(arrivaldateno[2]), int(arrivaltimeno[0]), int(arrivaltimeno[1]), int(timesecond[0]))
		oarrival_datetime = datetime(int(oarrivaldateno[0]), int(oarrivaldateno[1]), int(oarrivaldateno[2]), int(oarrivaltimeno[0]), int(oarrivaltimeno[1]), int(otimesecond[0]))

		arrdiff = arrival_datetime - oarrival_datetime

		# import pdb;pdb.set_trace()
		if float(origin_depth) < 1.5 and float(origin_longitude) > 81 and float(origin_longitude) < 159 and float(origin_latitude) > -26 and float(origin_latitude) < 24:
			origin_depth = float(origin_depth) * (-1)


			if float(elevation) < 1200 and float(longitude) > 81 and float(longitude) < 159 and float(latitude) > -26 and float(latitude) < 24:
				# import pdb;pdb.set_trace()
				if phase == phase1 or phase == phase2:
					if float(distance) <= 25 and abs(float(residual))<7.5:
						# import pdb;pdb.set_trace()
						fcorrect_events.write(str(line))
					elif float(distance) > 25 and abs(float(residual))<3.5:
						fcorrect_events.write(str(line))
					else:
						pass
fcorrect_events.close()
	
myevents=[]


with open('./P-wave_correct.dat') as openfileobject:
	flag = True
	for line in openfileobject:
		data = line.replace(" ","")
		data = data.split(",")
		myevents.append(data[0])

# if os.path.exists('data'):
# 	shutil.rmtree('data')
# 	os.makedirs('data')
# else:
# 	os.makedirs('data')


x =0

sta_list = []
reporter_lst = []
counter1=0
# f1=open('./testfile', 'w+')
# print mytemp
arrival_list = []
eventid_lst = []
arrival_list_print = []
myitems = []

station_arrivals = {}
with open('./P-wave_correct.dat') as openfileobject:
	flag = True
	for line, j in zip(openfileobject, previous_and_next(myevents)):
	# for line in openfileobject:
		data = line.replace(" ","")
		data = data.split(",")
	# for previous, item, nxt in previous_and_next(myevents):
		item = j[1]
		nxt = j[2]
		previous = j[0]
		# print sample_data
		eventid = data[0]
		reporter = data[1]
		station = data[2]
		phase = data[3]
		oarrivaldateno = [data[4],data[5],data[6]]
		oarrivaltimeno = [data[7],data[8],data[9]]
		arrivaldateno = [data[10],data[11],data[12]]
		arrivaltimeno = [data[13],data[14],data[15]]
		distance = data[16]
		latitude = data[17]
		longitude = data[18]
		elevation = data[19]
		origin_latitude = data[20]
		origin_longitude = data[21]
		origin_depth = data[22].strip()


		timesecond = arrivaltimeno[2].split(".")
		otimesecond = oarrivaltimeno[2].split(".")

		arrival_datetime = datetime(int(arrivaldateno[0]), int(arrivaldateno[1]), int(arrivaldateno[2]), int(arrivaltimeno[0]), int(arrivaltimeno[1]), int(timesecond[0]))
		oarrival_datetime = datetime(int(oarrivaldateno[0]), int(oarrivaldateno[1]), int(oarrivaldateno[2]), int(oarrivaltimeno[0]), int(oarrivaltimeno[1]), int(otimesecond[0]))

		arrdiff = arrival_datetime - oarrival_datetime

		#import pdb;pdb.set_trace()
		station_arrivals[station,reporter,eventid,phase] = [origin_latitude,origin_longitude,origin_depth,latitude,longitude,elevation,arrdiff]


if os.path.exists('data'):
	shutil.rmtree('data')
	os.makedirs('data')
else:
	os.makedirs('data')

if os.path.exists('sources'):
	shutil.rmtree('sources')
	os.makedirs('sources')
else:
    os.makedirs('sources')

fsources = open('./sources/sourceswa.in','w')
# import pdb;pdb.set_trace()
key_lstC = []
key_lstM = []
counter = 0
for key, elem in station_arrivals.items():
	# import pdb;pdb.set_trace()
	if str(round(float(elem[0]),1)) == '-0.0':
		 elem[0] = '0.0'
	mylatlot = str(round(float(elem[0]),1))+","+str(round(float(elem[1]),1))
	mohoD = interfaceDepth[mylatlot]
	if float(elem[2]) < float(mohoD)*-1 -10:
		with open('./data/pick'+key[0]+'.'+phnot+'.C','a') as openfileobject:
			# import pdb;pdb.set_trace()
			if key[0] not in key_lstC:
				# import pdb;pdb.set_trace()
				fsources.write('{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1)))
				print '{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1))
				fsources.write('%s\n' % "1")
				print '%s\n' % "1"
				mystr = "1	1	pick"+str(key[0])+"."+phnot+".C"
				print mystr
				fsources.write('%s\n' % mystr)
				counter += 1
			openfileobject.write('{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(elem[0],elem[1],str(elem[2]),str(elem[6].total_seconds()),"0.5"))
			# import pdb;pdb.set_trace()
			key_lstC.append(key[0])
	elif float(elem[2]) > float(mohoD)*-1 +10:
		with open('./data/pick'+key[0]+'.'+phnot+'.M','a') as openfileobject:
			# import pdb;pdb.set_trace()
			if key[0] not in key_lstM:
				fsources.write('{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1)))
				print '{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1))
				fsources.write('%s\n' % "1")
				print '%s\n' % "1"
				mystr = "2	1	pick"+str(key[0])+"."+phnot+".M"
				print mystr
				fsources.write('%s\n' % mystr)
				counter += 1
			openfileobject.write('{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(elem[0],elem[1],str(elem[2]),str(elem[6].total_seconds()),"0.5"))
			# import pdb;pdb.set_trace()
			key_lstM.append(key[0])
	else:
		pass
print counter
addFirstLine('./sources/sourceswa.in',str(counter))


template_file = []
dir_path = os.path.dirname('./data/')
template_file = []
for f in listdir(dir_path):
	# print f
	template_file.append(f)



# print template_file
for i in range(len(template_file)):
	with open('./data/'+template_file[i], 'r') as myfile:
		# print './data/'+template_file[i]
		noPicks = file_len('./data/'+template_file[i])
		addFirstLine('./data/'+template_file[i],str(noPicks))
		# import pdb;pdb.set_trace()
# print no_of_events
print "END", datetime.now().time(), datetime.now().date()
