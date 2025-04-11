import os
import pandas as pd
import datetime
import shutil
import numpy as np

print "START", datetime.datetime.now().time(), datetime.datetime.now().date()


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

azpcDir = '/home/rpgsbs/r02az15/Documents/aris/nonlinloc/src/clusteredWeightedNLLloc/'

dir_path = os.path.dirname(os.path.realpath(__file__))
def addFirstLine(azfile,NotoAdd):
	# import pdb;pdb.set_trace()
	with file(azfile, 'r') as original: data = original.read()
	with file(azfile, 'w') as modified: modified.write("{:<12}\n".format(int(NotoAdd)) + data)

dir_path = os.path.dirname(azpcDir)
template_file = []
for f in os.listdir(dir_path):
	if f.endswith(('.hyp')):
		template_file.append(f)

station_arrivals = {}
for i in range(len(template_file)):
	with open(dir_path+"/"+template_file[i], 'r') as myfile:
		print template_file[i]
		lines = myfile.readlines()
		# import pdb;pdb.set_trace()
		linesArrivals = [','.join(line.split()).split(",") for line in lines[16:-3]]
		# df = pd.DataFrame.from_records(df[1].tolist(), index=df[0],
  #                          columns=list('ABC')).reset_index()
  		try:
			arrivals = pd.DataFrame.from_records(linesArrivals,columns=["PHASE", "ID","Ins", "Cmp", "Pha",
			  "FM", "Date",     "HrMn",   "Sec",     "Err",  "ErrMag",
			      "Coda",      "Amp",       "Per",  ">",   "TTpred",
			          "Res",       "Weight","X", "Y","Z",
			                  "SDist",    "SAzim",
			                    "RAz",  "RDip", "RQual",    "Tcorr"])
		except Exception as e:
			print e
			continue
		
		eventid = lines[0].split(".")[2]+lines[0].split(".")[3]
		
		line = lines[5].split()
		# print data[5].split()
		origin_longitude = float(line[2])
		origin_latitude = float(line[4])
		origin_depth = float(line[6])
		line = lines[7].split()
		rms = float(line[8])
		

		#Check on residuals not to be more than 10 seconds
		if rms > 10:
			continue

		#Check that event lie in interested area
		if origin_depth < 1.5 or origin_longitude < 81 or origin_longitude > 159 or origin_latitude < -24 or origin_latitude > 24:
			continue
		
		#Expectation Value rather maxLikelihood
		# expectationVal = []
		# line = lines[10].split()
		# # print data[5].split()
		# expectationVal.append(line[4])
		# expectationVal.append(line[2])
		# expectationVal.append(line[6])

		
		year = lines[6].split()[2]
		month = lines[6].split()[3]
		day = lines[6].split()[4]
		hour = lines[6].split()[5]
		minutes = lines[6].split()[6]
		seconds = lines[6].split()[7]
		

		try:
			azdatetime = year+"-"+month+"-"+day+" "+hour+":"+minutes+":"+seconds
			origin_datetime = datetime.datetime.strptime(azdatetime, "%Y-%m-%d %H:%M:%S.%f")

			# import pdb;pdb.set_trace()

			arrivals['year'] = pd.Series(arrivals.Date.str[:4], index=arrivals.index)
			arrivals['month'] = pd.Series(arrivals.Date.str[4:6], index=arrivals.index)
			arrivals['day'] = pd.Series(arrivals.Date.str[6:8], index=arrivals.index)
			arrivals['hour'] = pd.Series(arrivals.HrMn.str[:2], index=arrivals.index)
			arrivals['minute'] = pd.Series(arrivals.HrMn.str[2:4], index=arrivals.index)
			arrivals['second'] = pd.Series(arrivals.Sec, index=arrivals.index)
			

			

			arrival_datetime = pd.to_datetime(dict(year = arrivals.year,
				month=arrivals.month,day=arrivals.day,
				hour=arrivals.hour,minute=arrivals.minute,
			second=arrivals.second))

			arrdiff = arrival_datetime - origin_datetime
			# tt = arrdiff.dt.total_seconds()
			arrivals['tt'] = pd.Series(arrdiff, index=arrivals.index)
			
			

			#Checks that data lie in my model and selection criteria
			selectedArrivals = arrivals[(arrivals.Z.astype(float) < 1.2) & (arrivals.X.astype(float) > 81) & (arrivals.X.astype(float) < 159) & (arrivals.Y.astype(float) > -24) & (arrivals.Y.astype(float) < 24)]
			selectedArrivals = selectedArrivals[(selectedArrivals['Pha'] == 'P') | (selectedArrivals['Pha'] == 'Pn')] 
			selectedArrivals = selectedArrivals[(selectedArrivals['SDist'].astype(float) <= 25)
										& (np.absolute(selectedArrivals['Res'].astype(float)) < 7.5)
										| (selectedArrivals['SDist'].astype(float) > 25)
										& (np.absolute(selectedArrivals['Res'].astype(float)) < 3.5)] 
			
			for index, row in selectedArrivals.iterrows():
				station_arrivals[str(row.PHASE),str(eventid),str(row.Pha)] = [origin_latitude,origin_longitude,origin_depth,row.Y,row.X,str(float(row.Z)*-1),row.tt,row.ErrMag]
		except Exception as e:
			print e
			# import pdb;pdb.set_trace()
			continue

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
				fsources.write('{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],elem[5]))
				print '{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],elem[5])
				fsources.write('%s\n' % "1")
				print '%s\n' % "1"
				mystr = "1	1	pick"+str(key[0])+".p.C"
				print mystr
				fsources.write('%s\n' % mystr)
				counter += 1
			openfileobject.write('{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(elem[0],elem[1],str(elem[2]),str(elem[6].total_seconds()),str(elem[7])))
			# import pdb;pdb.set_trace()
			key_lstC.append(key[0])
	elif float(elem[2]) > 67:
		with open('./data/pick'+key[0]+'.p.M','a') as openfileobject:
			# import pdb;pdb.set_trace()
			if key[0] not in key_lstM:
				fsources.write('{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],elem[5]))
				print '{:<15}{:<15}{:<15}\n'.format(elem[3],elem[4],elem[5])
				fsources.write('%s\n' % "1")
				print '%s\n' % "1"
				mystr = "2	1	pick"+str(key[0])+".p.M"
				print mystr
				fsources.write('%s\n' % mystr)
				counter += 1
			openfileobject.write('{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(elem[0],elem[1],str(elem[2]),str(elem[6].total_seconds()),str(elem[7])))
			# import pdb;pdb.set_trace()
			key_lstM.append(key[0])
	else:
		pass

print counter
fsources.close()
addFirstLine('./sources/sourceswa.in',str(counter))


template_file = []
dir_path = os.path.dirname('./data/')
template_file = []
for f in os.listdir(dir_path):
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
print "END", datetime.datetime.now().time(), datetime.datetime.now().date()