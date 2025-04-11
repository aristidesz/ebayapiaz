from os import listdir
from os.path import isfile, join
import os 
from itertools import cycle
import re
from datetime import datetime
import calendar
from collections import Counter
import shutil
from obspy.geodetics.base import gps2dist_azimuth
import os 
import time
import re

import collections
from itertools import tee, islice, chain, izip
# from __future__ import print_function


def previous_and_next(some_iterable):
	prevs, items, nexts = tee(some_iterable, 3)
	prevs = chain([None], prevs)
	nexts = chain(islice(nexts, 1, None), [None])
	return izip(prevs, items, nexts)

def mergeDictsOverwriteEmpty(d1, d2):
	res = d2.copy()
	for k,v in d2.items():
		if k not in d1 or d1[k] == '':
			res[k] = v
	return res

print "START", datetime.now().time(), datetime.now().date()






data_dictionary = {}





dir_path = os.path.dirname(os.path.realpath(__file__))


myevents=[]


with open('./P-S-ISC-EHB-AllSta.dat') as openfileobject:
	flag = True
	for line in openfileobject:
		data = line.replace(" ","")
		data = data.split(",")
		myevents.append(data[0])




x =0

sta_list = []
reporter_lst = []
counter1=0
f1=open('./testfile', 'w+')
# print mytemp
eventid_lst = []
arrival_list = []
arrival_list_print = []
myitems = []
d = {}
with open('./P-S-ISC-EHB-AllSta.dat') as openfileobject:
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
		latitude = data[3]
		longitude = data[4]
		elevation = data[5]
		channel = data[6]
		if channel == '':
			channel = '-100'
		distance = data[7]
		baz  = data[8]
		phase = data[9]
		arrival_date = data[10]
		arrival_time = data[11]
		residual = data[12]
		try:
			tdef = data[13]
		except:
			tdef = -100
		try:
			amplitude = data[14]
		except:
			amplitude = -100
		try:
			per = data[15]
		except:
			per = -100
		try:
			author = data[16]
		except:
			author = -100
		try:
			origin_date = data[17]
		except:
			continue
		origin_time = data[18]
		origin_latitude  = data[19]
		origin_longitude = data[20]
		origin_depth = data[21]
		if origin_depth == '':
			continue
		author1 = data[22]
		magnitude_type = data[23]
		magnitude = data[24].strip()
		if magnitude == '':
			magnitude = '-100'

		# import pdb;pdb.set_trace()
		arrivaldateno = arrival_date.split("-")
		arrivaltimeno = arrival_time.split(":")
		timesecond = arrivaltimeno[2].split(".")

		oarrivaldateno = origin_date.split("-")
		oarrivaltimeno = origin_time.split(":")
		try:
			otimesecond = oarrivaltimeno[2].split(".")
		except:
			import pdb;pdb.set_trace()
		arrival_datetime = datetime(int(arrivaldateno[0]), int(arrivaldateno[1]), int(arrivaldateno[2]), int(arrivaltimeno[0]), int(arrivaltimeno[1]), int(timesecond[0]))
		oarrival_datetime = datetime(int(oarrivaldateno[0]), int(oarrivaldateno[1]), int(oarrivaldateno[2]), int(oarrivaltimeno[0]), int(oarrivaltimeno[1]), int(otimesecond[0]))
		arrdiff = arrival_datetime - oarrival_datetime
		# arrival_list.append(str(latitude)+"\t"+str(longitude)+"\t"+str(elevation)+"\t"+str(arrdiff.total_seconds())+"\t0.1")
		# data_dictionary[eventid] = [station,phase,arrivaldateno[0],arrivaldateno[1],arrivaldateno[2],arrivaltimeno[0],arrivaltimeno[1],arrivaltimeno[2]]
		# import pdb;pdb.set_trace()
		if eventid in data_dictionary:
		# append the new number to the existing array at this slot
			data_dictionary[eventid].append([[reporter,station,phase,
			oarrivaldateno[0],
			oarrivaldateno[1],
			oarrivaldateno[2],
			oarrivaltimeno[0],
			oarrivaltimeno[1],
			oarrivaltimeno[2],
			arrivaldateno[0],
			arrivaldateno[1],
			arrivaldateno[2],
			arrivaltimeno[0],
			arrivaltimeno[1],
			arrivaltimeno[2],
			distance,
			latitude,
			longitude,
			elevation,
			origin_latitude,
			origin_longitude,
			origin_depth,
			magnitude,
			residual,
			channel]])
		else:
			# create a new array in this slot
			data_dictionary[eventid] = [[reporter,station,phase,
			oarrivaldateno[0],
			oarrivaldateno[1],
			oarrivaldateno[2],
			oarrivaltimeno[0],
			oarrivaltimeno[1],
			oarrivaltimeno[2],
			arrivaldateno[0],
			arrivaldateno[1],
			arrivaldateno[2],
			arrivaltimeno[0],
			arrivaltimeno[1],
			arrivaltimeno[2],
			distance,
			latitude,
			longitude,
			elevation,
			origin_latitude,
			origin_longitude,
			origin_depth,
			magnitude,
			residual,
			channel]]

if os.path.exists('data'):
	shutil.rmtree('data')
	os.makedirs('data')
else:
	os.makedirs('data')

# newlist = sorted(data_dictionary)
# , key=lambda k: k['name']) 



od = collections.OrderedDict(sorted(data_dictionary.items()))

result = {}

for key, elem in od.items(): 
    if elem not in result.values():
        result[key] = elem

# import pdb;pdb.set_trace()
fwrite = open('GroupedAllDatav2AllSta.dat','w')

for key, elem in result.items(): 
	for i in elem:
		# import pdb;pdb.set_trace()
		if len(i) == 1:
			i = i.pop(0)
		try:
			print key+","+i[0]+","+i[1]+","+i[2]+","+i[3]+","+i[4]+","+i[5]+","+i[6]+","+i[7]+","+i[8]+","+i[9]+","+i[10]+","+i[11]+","+i[12]+","+i[13]+","+i[14]+","+i[15]+","+i[16]+","+i[17]+","+i[18]+","+i[19]+","+i[20]+","+i[21]+","+i[22]+","+i[23]+","+i[24]
			fwrite.write(key+","+i[0]+","+i[1]+","+i[2]+","+i[3]+","+i[4]+","+i[5]+","+i[6]+","+i[7]+","+i[8]+","+i[9]+","+i[10]+","+i[11]+","+i[12]+","+i[13]+","+i[14]+","+i[15]+","+i[16]+","+i[17]+","+i[18]+","+i[19]+","+i[20]+","+i[21]+","+i[22]+","+i[23]+","+i[24]+"\n")
		except:
			import pdb;pdb.set_trace()


# for key, elem in data_dictionary.items(): 
#   s = re.split('[A-Z]+', key)
#   with open('./data/arrival'+str(s[0])+'.in','a') as openfileobject:
#       try:
#           # import pdb;pdb.set_trace()
#           openfileobject.write('{:<7}{:<5}{:<5}{:<2}{:<7}{:<2}{:<2}{:<2}{:<3}{:<2}{:<5}{:<7}{:<45}\n'.format(elem[0],
#                                                                           "?",
#                                                                           "?",
#                                                                           "?",
#                                                                           elem[1],
#                                                                           "?",
#                                                                           str(elem[2]),
#                                                                           str(elem[3]),
#                                                                           str(elem[4]),
#                                                                           str(elem[5]),
#                                                                           str(elem[6]),
#                                                                           str(elem[7]),
#                                                                           " GAU  1.00e-00 -1.00e+00 -1.00e+00 -1.00e+00"))
#       except Exception as e:
#           print e
#           # import pdb;pdb.set_trace()






print "END", datetime.now().time(), datetime.now().date()
