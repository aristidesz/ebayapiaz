from __future__ import division
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
from pyrocko import crust2x2
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from collections import defaultdict
from os import walk
from os import listdir
from os.path import isfile, join
from os import listdir
from mpl_toolkits.mplot3d import axes3d, Axes3D
import os 
from shutil import copyfile
import numpy as np
from mayavi import mlab
# import pytest
from tvtk.api import tvtk
import time
import  moviepy.editor as mpy
import scipy.ndimage as ndimage
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame, read_csv, Series
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn import preprocessing

pd.set_option('display.max_columns', None)

def cluster(d):
	clusters = defaultdict(list)
	for key, val in d.iteritems():
		clusters[val].append(key)
	return clusters


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

dir_path = os.path.dirname(os.path.realpath(__file__))
def addFirstLine(azfile,NotoAdd):
	# import pdb;pdb.set_trace()
	with open(azfile, 'r') as original: data = original.read()
	with open(azfile, 'w') as modified: modified.write("{:<12}\n".format(int(NotoAdd)) + data)

def removeFirstLine(file):
	removeLineFromFile(file,1,None)


def removeLineFromFile(file,lineNo,actualLine):
	f = open(file,"r+")
	d = f.readlines()
	f.seek(0)
	for ii,i in enumerate(d):
		line = ii + 1
		# import pdb;pdb.set_trace()
		if actualLine == None:
			if line != lineNo:
				f.write(i)
		else:
			if i != actualLine:
				f.write(i)
	f.truncate()
	f.close()

print "START", datetime.now().time(), datetime.now().date()


if os.path.exists('csvFiles'):
	shutil.rmtree('csvFiles')
	os.makedirs('csvFiles')
else:
	os.makedirs('csvFiles')

df = pd.DataFrame(columns=["eventid","reporter","station","phase",
                  "yearorigin","monthorigin","dayorigin",
                  "hourorigin","minuteorigin","secondorigin",
                  "yeararrival","montharrival","dayarrival","hourarrival"
                  ,"minutearrival","secondarrival","distance","stalat","stalong",
                  "staelev","latitude","longitude","depth","magnitude","residual","channel",
                  "clusterLabel","uncertaintyTT"])

events = pd.read_csv("AZF-P-SAllSta.dat", 
                  names = ["eventid","reporter","station","phase",
                  "yearorigin","monthorigin","dayorigin",
                  "hourorigin","minuteorigin","secondorigin",
                  "yeararrival","montharrival","dayarrival","hourarrival"
                  ,"minutearrival","secondarrival","distance","stalat","stalong",
                  "staelev","latitude","longitude","depth","magnitude","residual","channel"])


for sta in events['station'].unique():
	staevents = events[(events.station == sta)]
	
	# fread = open('AZF-P-SAllSta','r')
	myfeatures = []
	myreal = []
	
	# print line
	lat = staevents['latitude']
	long = staevents['longitude']
	alt = staevents['depth']
	phase =  staevents['phase']

	le = preprocessing.LabelEncoder()
	phaseEncoded = le.fit(phase).transform(phase)

	oarrival_datetime = pd.to_datetime(dict(year = staevents.yearorigin,
		month=staevents.monthorigin,day=staevents.dayorigin,
		hour=staevents.hourorigin,minute=staevents.minuteorigin,
		second=staevents.secondorigin))


	arrival_datetime = pd.to_datetime(dict(year = staevents.yeararrival,
		month=staevents.montharrival,day=staevents.dayarrival,
		hour=staevents.hourarrival,minute=staevents.minutearrival,
		second=staevents.secondarrival))

	arrdiff = arrival_datetime - oarrival_datetime
	tt = arrdiff.dt.total_seconds()


	myfeatures = zip(lat,long,alt)
	myreal = zip(lat,long,alt,tt)


	farr = np.array(myfeatures)

	realdepth = (6371-farr[:,2])/6371

	lat, long, tempdepth = farr.T * np.pi / 180


	x1 = np.cos(lat) * np.cos(long) * realdepth
	y1 = np.cos(lat) * np.sin(long) * realdepth
	z1 = np.sin(lat) * realdepth


	realtt = np.array(myreal)[:,3]
	scaler = StandardScaler().fit_transform(realtt)
	X = np.array(zip(x1,y1,z1,scaler))
	db = DBSCAN(eps=0.00580001, min_samples=2).fit(X)
	labels = db.labels_
	mylabels = []





	n_clusters_ = len(set(labels))  - (1 if -1 in labels else 0)

	#Print station No. of clusters and the labels
	print sta
	print "Number of Clusters: " , n_clusters_
	print Counter(labels)

	##
	labdict = dict()
	for ll,mf in zip(labels,myreal):
		if ll in labdict:
			labdict[ll].append(mf)
		else:
			labdict[ll] = [mf]

	lbStd = {}
	for elem in labdict.items():
		labelTT = []
		for items in elem[1]: 
			# print elem[0],items[3]
			labelTT.append(float(items[3]))
		# print np.std(labelTT)	
		
		# numerator = [np.square(np.mean(labelTT)-lt) for lt in labelTT]
		# wi = np.sqrt(np.sum(numerator)/len(labelTT))
		if elem[0] != -1:
			weight = np.divide(1,np.sqrt(np.var(labelTT)))
			# import pdb;pdb.set_trace()
		else:
			weight = 1.3

		lbStd[elem[0]] = weight

	unc_lst = []
	for myl,myi in zip(labels,myreal):
		if myl == -1:
			uncertainty = '1.3'
		else:
			#Round the uncertainty of each label
			uncertainty = round(lbStd[myl],2)

			if np.isinf(uncertainty):
				uncertainty = 0.1
			#Check for too small uncertainties
			if uncertainty < 0.1:
				uncertainty = 0.1
			uncertainty = str(uncertainty)
	
		unc_lst.append(uncertainty)	
	

	#Attach cluster label and uncertainty of traveltime on data
	staevents['clusterLabel'] = Series(labels, index=staevents.index)
	staevents['uncertaintyTT'] = Series(unc_lst, index=staevents.index)

	#Longitude Correction for -180 and 180
	staevents['stalong'] = staevents['stalong'].apply(lambda x: np.mod((float(x)+180),360)-180)

	#Loop over unique labels and output only one event for each cluster except when event belongs to no cluster
	for lf in labdict.keys():
		if lf != -1:
			# print staevents.loc[staevents['clusterLabel'] == lf].iloc[0]
			df = df.append(staevents.loc[staevents['clusterLabel'] == lf].iloc[0])

	df =  df.append(staevents.loc[staevents['clusterLabel'] == -1])
	# import pdb;pdb.set_trace()
	df.to_csv('./csvFiles/'+str(sta)+'.csv', sep=',',index=False)
	df = pd.DataFrame(columns=["eventid","reporter","station","phase",
	                  "yearorigin","monthorigin","dayorigin",
	                  "hourorigin","minuteorigin","secondorigin",
	                  "yeararrival","montharrival","dayarrival","hourarrival"
	                  ,"minutearrival","secondarrival","distance","stalat","stalong",
	                  "staelev","latitude","longitude","depth","magnitude","residual","channel",
	                  "clusterLabel","uncertaintyTT"])

azpcDir = './csvFiles/'
dir_path = os.path.dirname(azpcDir)
template_file = []
for f in os.listdir(dir_path):
	if f.endswith(('.csv')):
		template_file.append(f)

station_arrivals = {}
for i in range(len(template_file)):
	with open(dir_path+"/"+template_file[i], 'r') as myfile:
		df =  df.append(pd.read_csv(myfile))


# import pdb;pdb.set_trace()
df.sort_values(by=['eventid'])
df.to_csv('cleanDataPSISCEHBv2.csv', sep=',',index=False)

print "Done removing close events. S/N Improved!"