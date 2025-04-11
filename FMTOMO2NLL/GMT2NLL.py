fread = open('azFMTOMOVel.p','r')

fwrite = open('./AZNLLVel1.p','w')
velDict ={}
for line in fread:
	sline = line.strip().split()
	fwrite.write(sline[3]+'\n')

	# import pdb;pdb.set_trace()

fwrite.close()