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

if os.path.exists('picks'):
	shutil.rmtree('picks')
	os.makedirs('picks')
else:
	os.makedirs('picks')




dir_path = os.path.dirname(os.path.realpath(__file__))
mypath = dir_path+"/data/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
	for file in filenames:
		print file
		removeFirstLine(mypath+file)
		try:
			noPicks = file_len(mypath+file)
			if noPicks < 5: #or noPicks == 1:
				copyfile('./data/'+file, './picks/'+file)
				continue
		except Exception as e:
			print e
			print "No picks found!"
			import pdb;pdb.set_trace()
			copyfile('./data/'+file, './picks/'+file)		
		with open(mypath+file,'r+') as fread:
			myfeatures = []
			myreal = []
			for line in fread:
				# print line
				sline = line.split()
				# lat = float(sline[0])
				# lon = float(sline[1])
				# depth = float(sline[2])
				lat = float(sline[0])
				long = float(sline[1])
				alt = float(sline[2])
				tt = float(sline[3])

				# x1 = alt * np.cos(lat) * np.sin(long)
				# y1 = alt * np.sin(lat)
				# z1 = alt * np.cos(lat) * np.cos(long)

				myfeatures.append([lat,long,alt])
				myreal.append([lat,long,alt,tt])


			farr = np.array(myfeatures)
			
			realdepth = (6371-farr[:,2])/6371
			
			lat, long, tempdepth = farr.T * np.pi / 180

			# alt = farr[:,2]
			x1 = np.cos(lat) * np.cos(long) * realdepth
			y1 = np.cos(lat) * np.sin(long) * realdepth
			z1 = np.sin(lat) * realdepth

			
			# import pdb;pdb.set_trace()
			realtt = np.array(myreal)[:,3]
			scaler = StandardScaler().fit_transform(realtt)
			X = np.array(zip(x1,y1,z1,scaler))



			try:
				# nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)
				# distances, indices = nbrs.kneighbors(X)
				# mean = np.mean(distances)
				# print "Mean distance= ",mean


				# db = DBSCAN(eps=mean*0.3, min_samples=2).fit(X)
				# import pdb;pdb.set_trace()
				db = DBSCAN(eps=0.00580001, min_samples=2).fit(X)
				labels = db.labels_
				mylabels = []
				

				fread.seek(0)
				labelSeen = []
				lineRemoved = []
				for ml,[lineNo,line] in zip(labels,enumerate(fread)):
					if ml == -1:
						continue
					else:
						if ml in labelSeen:
							lineRemoved.append(lineNo+1)
							print line
						else:
							labelSeen.append(ml)


				n_clusters_ = len(set(labels))  - (1 if -1 in labels else 0)
				print "Number of Clusters: " , n_clusters_

				# kmeans_model = KMeans(n_clusters=n_clusters_, random_state=1).fit(X)
				# labelsk = kmeans_model.labels_
				# print "Metrics Silhouette score: ", metrics.silhouette_score(X, labels, metric='euclidean')

				# import pdb;pdb.set_trace()
				print Counter(labels)
				# X_embedded = TSNE(n_components=2).fit_transform(X)
				X_embedded = PCA(n_components=2).fit_transform(X)
				mylabels = []
				for ml in labels:
					if ml == -1:
						ml = 1.5
					elif ml == 0:
						ml = 2.5
					mylabels.append(ml)
				mylabels = np.array(mylabels)
				

				fig = plt.figure()
				ax = fig.add_subplot(1, 1, 1)


				plt.scatter(X_embedded[:,0],X_embedded[:,1],c=mylabels,norm=colors.LogNorm(vmin=mylabels.min(), vmax=mylabels.max()), cmap='jet')
			
				
				# ax = fig.add_subplot(1, 2, 2,projection='3d')
				f = mlab.figure(1, bgcolor=(0.48, 0.48, 0.48), fgcolor=(0, 0, 0),
							 size=(400, 400))
				f = mlab.clf()
				world = []
				with open('world100.txt','rb') as csvfile:
					for line in csvfile:
						if line !="\n":
							lon, lat = line.split()	
							lat = float(lat)
							lon = float(lon)
							
							if lon > 60 and lon < 180 and lat > -45 and lat < 45:
								world.append([lat,lon])
						else:
							import numpy as np
							if world:
								world = np.array(world)
								lat, long = world.T * np.pi / 180



								x = np.cos(lat) * np.cos(long) 
								y = np.cos(lat) * np.sin(long)
								z = np.sin(lat) 


								mlab.plot3d(x, y, z, color=(0,0,0),tube_radius=None,opacity=1)
								world = []
				# ax = Axes3D(fig)
				# amyfeatures = np.array(myfeatures)
				points = mlab.points3d(X[:,0],X[:,1],X[:,2],mylabels,
										colormap="jet",
										 scale_mode='none',scale_factor=0.01)
				# ax.scatter(,c=mylabels,norm=colors.LogNorm(vmin=mylabels.min(), vmax=mylabels.max()), cmap='jet')
				# plt.show()
				plt.close()
				mlab.show()

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
						if np.isinf(weight):
							pass
						else:
							import pdb;pdb.set_trace()
					else:
						weight = 1.3

					lbStd[elem[0]] = weight

				
				with open('./picks/'+file,'w') as fw:
					for myl,myi in zip(labels,myreal):
						uncertainty = round(lbStd[myl],2)
						if uncertainty < 0.1:
							uncertainty = 0.1
						if np.isinf(uncertainty):
							uncertainty = 1.3
						uncertainty = str(uncertainty)

					# uncertainty = '0.1'		
						print '{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(myi[0],myi[1],str(myi[2]),str(myi[3]),uncertainty)
						fw.write('{:<15}{:<15}{:<15}{:<15}{:<15}\n'.format(myi[0],myi[1],str(myi[2]),str(myi[3]),uncertainty)) 



				for ii,rmL in enumerate(lineRemoved):
					if ii == 0:
						lineNo = rmL
						# print lineNo
						linesRemoved = 0
						# file = 'pickASAR.p.M'
						removeLineFromFile("./picks/"+file,lineNo,actualLine=None)
					else:
						
						linesRemoved += 1
						lineNo = rmL - linesRemoved
						# file = 'pickASAR.p.M'
						removeLineFromFile("./picks/"+file,lineNo,actualLine=None)
						# print lineNo
			except Exception as e:
				print e
				copyfile('./data/'+file, './picks/'+file)
				# import pdb;pdb.set_trace()


dir_path = os.path.dirname('./picks/')
template_file = []
for f in listdir(dir_path):
	# print f
	template_file.append(f)

for i in range(len(template_file)):
	with open('./picks/'+template_file[i], 'r') as myfile:
		# print './data/'+template_file[i]
		noPicks = file_len('./picks/'+template_file[i])
		# import pdb;pdb.set_trace()
		addFirstLine('./picks/'+template_file[i],str(noPicks))


dir_path = os.path.dirname('./data/')
template_file = []
for f in listdir(dir_path):
	# print f
	template_file.append(f)

for i in range(len(template_file)):
	with open('./data/'+template_file[i], 'r') as myfile:
		# print './data/'+template_file[i]
		noPicks = file_len('./data/'+template_file[i])
		# import pdb;pdb.set_trace()
		addFirstLine('./data/'+template_file[i],str(noPicks))
# import pdb;pdb.set_trace()


print "Done removing close events. S/N Improved!"