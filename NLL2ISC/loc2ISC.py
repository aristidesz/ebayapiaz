from os import listdir
from os.path import isfile, join
import os 
from itertools import cycle
import re
from datetime import datetime
import calendar
from collections import Counter
from itertools import tee, islice, chain, izip
import time

print "START", datetime.now().time(), datetime.now().date()

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

myevents= []

minrms = 10
myIFile = 'AZF-P-SAllSta.dat'
inputFile = '../dbscanClust/'+myIFile
# inputFile = './cleanDataPSISCEHBv2.csv'
inputLocFile = '/home/rpgsbs/r02az15/Documents/aris/nonlinloc/src/AZF-P-SAllStaLoc/'

with open(inputFile) as openfileobject:
	flag = True
	for line in openfileobject:
		data = line.replace(" ","")
		data = data.split(",")
		myevents.append(data[0])


template_file = []
dir_path = os.path.dirname(inputLocFile)
template_file = []
for f in listdir(dir_path):
	if f.endswith(('.hyp')):
		template_file.append(f)


tempeventID=0


arrivals = {}
event_dict = {}

with open(inputFile) as openfileobject:
	for line, j in zip(openfileobject, previous_and_next(myevents)):
		data = line.replace(" ","").strip()
		data = data.split(",")
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
		compareDT = str(arrivaldateno[0])+str(arrivaldateno[1])+str(arrivaldateno[2])+str(arrivaltimeno[0])+str(arrivaltimeno[1])+str(arrivaltimeno[2])
		arrivals[compareDT] = eventid

# import pdb;pdb.set_trace()
counterFound = 0
connectionEventID = {}
eventsNLL = set()
for i in range(len(template_file)):
	with open(inputLocFile+template_file[i], 'r') as myfile:
		data=myfile.read().splitlines()
		rms = str(data[7].split()[8])
		if float(rms) < minrms:
			# import pdb;pdb.set_trace()
			year = data[6].split()[2]
			month = data[6].split()[3]
			day = data[6].split()[4]
			hour = data[6].split()[5]
			minutes = data[6].split()[6]
			seconds = data[6].split()[7]
			seconds = str(round(float(seconds),4))

			azdatetime = year+"-"+month+"-"+day+" "+hour+":"+minutes+":"+seconds
			try:
				origin_datetime = datetime.strptime(azdatetime, "%Y-%m-%d %H:%M:%S.%f")
			except Exception as e:
				print e
				# import pdb;pdb.set_trace()

			dateNtime = find_between(data[0],"global.",".grid0")
			spdateNtime = dateNtime.split(".")
			nllCompareDT = spdateNtime[0]+spdateNtime[1]+"."+spdateNtime[2]

			try:
				eventsNLL.add(arrivals[nllCompareDT])
				
			except Exception as e:
				print e
				# print "Arrival Not Found!"

newinputFile = myIFile.replace('.dat','NLLData.dat')

fNLL = open(newinputFile,'w')
with open(inputFile) as openfileobject:
	for line in openfileobject:
		data = line.replace(" ","").strip()
		data = data.split(",")
		if data[0] in eventsNLL:
			fNLL.write(line)

print "END", datetime.now().time(), datetime.now().date()