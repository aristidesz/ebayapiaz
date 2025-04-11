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

with open('./AZF-P-S-ISC-EHB.dat') as openfileobject:
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

with open('./AZF-P-S-ISC-EHB.dat') as openfileobject:
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
				if phase == 'P' or phase == 'Pn':
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
	if float(elem[2]) < 63:
		with open('./data/pick'+key[0]+'.p.C','a') as openfileobject:
			# import pdb;pdb.set_trace()
			if key[0] not in key_lstC:
				# import pdb;pdb.set_trace()
				fsources.write('{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1)))
				print '{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1))
				fsources.write('%s\n' % "1")
				print '%s\n' % "1"
				mystr = "1	1	pick"+str(key[0])+".p.C"
				print mystr
				fsources.write('%s\n' % mystr)
				counter += 1
			openfileobject.write('{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(elem[0],elem[1],str(elem[2]),str(elem[6].total_seconds()),"0.5"))
			# import pdb;pdb.set_trace()
			key_lstC.append(key[0])
	elif float(elem[2]) > 67:
		with open('./data/pick'+key[0]+'.p.M','a') as openfileobject:
			# import pdb;pdb.set_trace()
			if key[0] not in key_lstM:
				fsources.write('{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1)))
				print '{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],str(float(elem[5])*1/1000*-1))
				fsources.write('%s\n' % "1")
				print '%s\n' % "1"
				mystr = "2	1	pick"+str(key[0])+".p.M"
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
