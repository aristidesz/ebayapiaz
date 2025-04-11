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

from itertools import tee, islice, chain, izip
# from __future__ import print_function


def previous_and_next(some_iterable):
	prevs, items, nexts = tee(some_iterable, 3)
	prevs = chain([None], prevs)
	nexts = chain(islice(nexts, 1, None), [None])
	return izip(prevs, items, nexts)


print "START", datetime.now().time(), datetime.now().date()



file_input = '../dbscanClust/AZF-P-SAllSta.dat'
# file_input = './cleanDataPSISCEHBv2.csv'

data_dictionary = {}





dir_path = os.path.dirname(os.path.realpath(__file__))


myevents=[]


with open(file_input) as openfileobject:
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

with open(file_input) as openfileobject:
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
		# clusterLabel = data[26]
		# uncertainty = data[27]
		# uncertainty = round(float(uncertainty),2)
		# if uncertainty == 0.1:
		# 	uncertainty = 0.5
		# if uncertainty < 0.1:
		# 	uncertainty = 0.5

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
		# arrival_list.append(str(latitude)+"\t"+str(longitude)+"\t"+str(elevation)+"\t"+str(arrdiff.total_seconds())+"\t0.1")
		# data_dictionary[eventid+station+phase] = [station,phase,arrivaldateno[0],arrivaldateno[1],arrivaldateno[2],arrivaltimeno[0],arrivaltimeno[1],arrivaltimeno[2],uncertainty]
		data_dictionary[eventid+station+phase] = [station,phase,arrivaldateno[0],arrivaldateno[1],arrivaldateno[2],arrivaltimeno[0],arrivaltimeno[1],arrivaltimeno[2]]
		# import pdb;pdb.set_trace()

if os.path.exists('data'):
	shutil.rmtree('data')
	os.makedirs('data')
else:
	os.makedirs('data')




for key, elem in data_dictionary.items(): 
	s = re.split('[A-Z]+', key)
	with open('./data/arrival'+str(s[0])+'.in','a') as openfileobject:
		try:
			# import pdb;pdb.set_trace()
			if len(elem[3])==1:
				elem[3] = "%02d" % int(elem[3])
			if len(elem[4])==1:
				elem[4] = "%02d" % int(elem[4])
			if len(elem[5])==1:
				elem[5] = "%02d" % int(elem[5])
			if len(elem[6])==1:
				elem[6] = "%02d" % int(elem[6])
			openfileobject.write('{:<7}{:<5}{:<5}{:<2}{:<7}{:<2}{:<2}{:<2}{:<3}{:<2}{:<5}{:<7}{:<6}{:<8}{:<32}\n'.format(elem[0],
																			"?",
																			"?",
																			"?",
																			elem[1],
																			"?",
																			str(elem[2]),
																			str(elem[3]),
																			str(elem[4]),
																			str(elem[5]),
																			str(elem[6]),
																			str(elem[7]),
																			" GAU",
																			"0.1"," -1.00e+00 -1.00e+00 -1.00e+00"))
																			# str(elem[8])," -1.00e+00 -1.00e+00 -1.00e+00"))
		except Exception as e:
			print e
			# import pdb;pdb.set_trace()






print "END", datetime.now().time(), datetime.now().date()
