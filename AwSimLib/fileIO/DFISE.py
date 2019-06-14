####################################################################
####################################################################
#### 	The Awesome Simulator, DF-ISE FileIO Module		####
####    						    	####
####	Author: Abhejit Rajagopal,  abhejit@ucla.edu	    	####
####    		   				    	####
####    (DFISE.py) is part of the AwSimLib software package   	####
####	module DFISE.py: /fileIO/DFISE.py		    	####
####    		    				    	####
####    This software is free to use, subjct to terms and   	####
####    	conditions in the AwSimLib license (LGPLv3).	####
####    AwSimLib license: ../_LICENSE.TXT		    	####
####################################################################
####################################################################

####################################################################
####	 Version History					####
####################################################################
####  0.1	09/01/2013 - classes, combine by line		####
####  0.2	12/12/2013 - combine v2.py			####
####  0.3	04/10/2014 - read.py, unified			####
####  0.4	05/20/2014 - lumeric, csv, 			####
####  0.5	09/02/2014 - AwSimLib initial release		####
####  								####
####  Part of the AwSimLib software package.			####
####  Copyright (C) 2014 Abhejit Rajagopal			####
####################################################################
####################################################################

####################################################################
####	Helper Functions: --> Debug				####
####################################################################
## system libs
import sys
orig_stdout = sys.stdout

def printHEADER(string):
	pass
	#string = string
	#print (string)
def printINFO(string):
	pass	
	#string = string	
	#print (string)
def printDATA(string):
	pass
	#string = string	
	#print (string)
def printADD(string):
	pass
	#string = string
	#print (string)
####################################################################
####################################################################

####################################################################
####	Class Definitions:--> Make a DFISE_File object		####
####################################################################
class DFISE_DATfile:
## DF-ISE Data ('.dat') File handler
	def __init__(self, *filenames):
		self.filename = 'FilenameNotSpecified.noext'
		self.INFO = Info()
		self.DATA = Data()

		# optional filename options to pre-load data
		if len(filenames)==0:
			print ('Empty DFISE_DATFile: no filename specified.')
		elif len(filenames)==1:
			self.filename = str(filenames[0])
	#
## end DF-ISE object class

class Info:
## class to represent header in a '.dat' file
	def __init__(self):
		self.version 	= []
		self.type 	= []
		self.dimension 	= []
		self.nb_vertices= []
		self.nb_edges	= []
		self.nb_faces	= []
		self.nb_elements= []
		self.nb_regions	= []
		self.datasets	= []
		self.functions	= []

	def setField(self, field, value):
	#applies a value to a field
		if (field == "version"):
			self.version = value
		elif (field == "type"):
			self.type = value
		elif (field == "dimension"):
			self.dimension = value
		elif (field == "nb_vertices"):
			self.nb_vertices = value
		elif (field == "nb_edges"):
			self.nb_edges = value
		elif (field == "nb_faces"):
			self.nb_faces = value
		elif (field == "nb_elements"):
			self.nb_elements = value
		elif (field == "nb_regions"):
			self.nb_regions = value
		elif (field == "datasets"):
			self.datasets = value
		elif (field == "functions"):
			self.functions = value
## end Info class

class Data:
## class to represent data in a '.dat' file
	def __init__(self):
		self.numDatasets= []	# of datasets	
		self.datasets 	= []	#list of datasets

	def setNum(self, number):
	#sets numDatasets
	#makes appropriate number of Dataset variables to store in datasets
		self.numDatasets = number
		setX = []
		for i in range(number) :
			setX.append(Dataset())
		self.datasets = setX

	def setField (self, counter, field, value):
	#sets value of field in datasets[counter]
		#print "field== " + str(field.strip()) + "  value== " + str(value) + "  length== " + str(len(self.datasets))
		self.datasets[counter].setField(field.strip(),value)

	def retData(self,counter):
		return self.datasets[counter]
## end Data class

class Dataset:
## class to represent each dataset within data in a '.dat' file
	def __init__(self):
		self.dataname	= []
		self.function 	= []
		self.type 	= []
		self.dimension 	= []
		self.location 	= []
		self.validity 	= []

		self.numValues 	= []
		self.Values 	= []

	def setField(self, field, value):
	#applies a value to a field
		if (field == "dataname"):
			self.dataname = value
		elif (field == "function"):
			self.function = value
		elif (field == "type"):
			self.type = value
		elif (field == "dimension"):
			self.dimension = value
		elif (field == "location"):
			self.location = value
		elif (field == "validity"):
			self.validity = value
		elif (field == "numValues"):
			#print "NumVALUES! == " + str(value)
			self.numValues = value
		elif (field == "Values"):
			#self.Values.append(value)
			self.Values = value
## end Dataset class
####################################################################
####################################################################

####################################################################
####	Functions: --> File Ops					####
####################################################################
def readDAT(filenames):
#### File Parser for DF-ISE data ('.dat') files
####
####	In:	List of filenames, e.g.: filenames=['testgrid1.dat'(, ...)]
####
####	Out:	List of DF-ISE objects, e.g.: to_return=[dfise_object1,(, ...)]
####				
####				
	## libraries provided by system
	import numpy as np
	import sys
	import glob
	##
	
	to_return = [] #list of DFISE_DATfile
	
	print ('')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('DF-ISE readDAT')

	if type(filenames)!=list: #correct if only 1 item provided
		filenames = [filenames]
	#

	i = 0
	for filename in filenames:

		grabNull = 0
		grabHead = 1
		grabInfo = 0
		grabData = 0
		grabDataVALS = 0

		print ('~~~~~~~~~~~~~~~~~~~~')
		f = open (filename,"r")
		print ("processing:	" + str(filename))


		DFISE_obj = DFISE_DATfile(str(filename))
		j = -1	#dataset counter

		for line in f:

			if grabHead == 1: ## check file type/header on first line ##
				split_space = line.split(' ')
				#good
				if split_space[0] == "DF-ISE":
					print ("-->Header OK: DF-ISE text")
					grabHead = 0
					grabNull = 1
					continue
				#bad
				else:
					print ("~~~~")
					print (" was expecting a DF-ISE file, check file header")
					sys.exit(0)
			elif grabNull == 1:
				split_space = line.split(' ')
				
				if split_space[0] == 'Info':
					print ("-->Info section identified")
					grabInfo = 1
					grabNull = 0
					continue
				elif split_space[0] == 'Data':
					print ("-->Data section identified")
					grabData = 1
					grabNull = 0
					continue
				elif split_space[0].strip() == '':
					printHEADER( "..blankline.." )
					continue
				else:
					print ("~~~~")
					print ("ERROR SHOULD NOT BE HERE -- grabNull == 1")
					sys.exit(0)
			elif grabInfo == 1:
				split_equ = line.split('=')
				field = split_equ[0].strip()
				
				if len(split_equ) > 1:
					quantity = split_equ[1]
				elif split_equ[0].strip() == '}':	#end criteria
					print ("--end of Info section.")
					grabInfo = 0
					grabNull = 1
				else:
					print ("~~~~")
					print ("ERROR SHOULD NOT BE HERE -- grabInfo == 1")
					sys.exit(0)
				
				if field == "version":
					Info_version = float(quantity.strip()) #float
					DFISE_obj.INFO.setField(field, Info_version)
					printINFO( "version = " + str(Info_version) )
				elif field == "type":
					Info_type = quantity.strip() #string
					DFISE_obj.INFO.setField(field, Info_type)
					printINFO( "type = " + str(Info_type))
				elif field == "dimension":
					Info_dimension = int(quantity.strip()) #int
					DFISE_obj.INFO.setField(field, Info_dimension)
					printINFO( "dimension = " + str(Info_dimension) )
				elif field == "nb_vertices":
					Info_nb_vertices = int(quantity.strip()) #int
					DFISE_obj.INFO.setField(field, Info_nb_vertices)
					printINFO( "nb_vertices = " + str(Info_nb_vertices) )
				elif field == "nb_edges":
					Info_nb_edges = int(quantity.strip()) #int
					DFISE_obj.INFO.setField(field, Info_nb_edges)
					printINFO( "nb_edges = " + str(Info_nb_edges) )
				elif field == "nb_faces":
					Info_nb_faces = int(quantity.strip()) #int
					DFISE_obj.INFO.setField(field, Info_nb_faces)
					printINFO( "nb_faces = " + str(Info_nb_faces) )
				elif field == "nb_elements":
					Info_nb_elements = int(quantity.strip()) #int
					DFISE_obj.INFO.setField(field, Info_nb_elements)
					printINFO( "nb_elements = " + str(Info_nb_elements) )
				elif field == "nb_regions":
					Info_nb_regions = int(quantity.strip()) #int
					DFISE_obj.INFO.setField(field, Info_nb_regions)
					printINFO( "nb_regions = " + str(Info_nb_regions) )
				elif field == "datasets":
					Info_nb_datasets = quantity.split('[ "')[1].split('" ]')[0].split('" "')	#list of str
					Info_num_datasets = int(len(Info_nb_datasets))								#int
					DFISE_obj.INFO.setField(field, Info_nb_datasets)
					#INFO.setField("version", Info_num_datasets)
					printINFO( "nb_datasets (" + str(Info_num_datasets) + ") = " + str(Info_nb_datasets) )
				elif field == "functions":
					Info_nb_functions = quantity.split('[ ')[1].split(' ]')[0].split(' ')		#list of str
					Info_num_functions = int(len(Info_nb_functions))							#int
					DFISE_obj.INFO.setField(field, Info_nb_functions)
					#INFO.setField("version", Info_num_functions)
					printINFO( "nb_functions (" + str(Info_num_functions) + ") = " + str(Info_nb_functions) )
					if Info_num_functions == Info_num_datasets:
						print ("number of datasets matches number of functions, ok!")
						DFISE_obj.DATA.setNum(Info_num_datasets)
					else:
						print ("number of datasets does not match number of functions, check file!")
						sys.exit(0)
			elif grabData == 1:
				split_equ = line.split('=')
				split_space = line.split(' ')
				
				#print (split_space)
				#print (split_equ)
				
				field = None
				quantity = None
				
				if grabDataVALS == 0:
				
					for each in split_space:
						field = each.strip()
										
						if field == '':
							#print ("..blankspace or blankline.."),
							continue
						elif field == "Dataset":
							j = j+1
							printDATA( "**NEW DATASET, j = " + str(j) + " **" )
							Data_name = str(line.split(' ("')[1].split('") ')[0])	#str
							DFISE_obj.DATA.setField(j, "dataname", Data_name)
							printDATA( "name = " + Data_name )
						elif field == "function":
							Data_function = str(split_equ[1].strip())	#str
							DFISE_obj.DATA.setField(j, field, Data_function)
							printDATA( "function = " + Data_function )
						elif field == "type":
							Data_type = str(split_equ[1].strip())	#str
							DFISE_obj.DATA.setField(j, field, Data_type)
							printDATA( "type = " + Data_type )
						elif field == "dimension":
							Data_dimension = str(int(split_equ[1].strip()))	#int
							DFISE_obj.DATA.setField(j, field, Data_dimension)
							printDATA( "dimension = " + str(Data_dimension) )
						elif field == "location":
							Data_location = str(split_equ[1].strip())	#str
							DFISE_obj.DATA.setField(j, field, Data_location)
							printDATA( "location = " + Data_location )
						elif field == "validity":
							Data_validity = str(split_equ[1].split('[ "')[1].split('" ]')[0]) #str
							DFISE_obj.DATA.setField(j, field, Data_validity)
							printDATA( "validity = " + Data_validity )
						elif field == "Values":
							Data_num_values = int(line.split(' (')[1].split(') ')[0])	#int
							DFISE_obj.DATA.setField(j, "numValues", Data_num_values)
							printDATA( "num_values = " + str(Data_num_values) )
							grabDataVALS = 1
							datasetvals = []	# 1D list later converted to numpy array
						
				elif grabDataVALS == 1:
					## READ VALS BY LINE (DEPRICATED)###
#					if line.strip() == '}':
#						#print(datasetvals)
#						DFISE_obj.DATA.setField(j, "Values", datasetvals)
#						grabDataVALS = 0
#						continue
#					
#					quantities = line.split(' ')
#					linevals = []
#					for each in quantities:
#						if each.strip() == '':
#							continue
#						else:
#							linevals.append(float(each))
#							
#					linevals = np.array(linevals)		#each line is stored as an array
#					datasetvals.append(linevals)		#inside a list for each dataset
#					#print ("length = " + str(len(datasetvals)) + "  values = " + str(datasetvals))

					## READ VALS BY SECTION (array of dataset values)###
					if line.strip() == '}': #ending brace
						#print(datasetvals)
						datasetvals = np.array(datasetvals) #cast as numpy array (modify for alternate datatype)
						#print ("length = " + str(len(datasetvals)) )#+ "  values = " + str(datasetvals))
						DFISE_obj.DATA.setField(j, "Values", datasetvals)
						grabDataVALS = 0
						continue
					
					quantities = line.split(' ')
					linevals = []
					for each in quantities:
						if each.strip() == '':
							continue
						else:
							datasetvals.append(float(each))
						#
					#
		#	#	#		
		
		## Done collecting all the data, close file and append to data list
		f.close()
		to_return.append(DFISE_obj)

		i = i+1	#file number counter
	# end file
	print ("~~~~~~~~~~~~~~~~~~~~")
	print ('')
	
	return to_return
## END FUNCTION
def printDAT(dat):
#### Print dataset info from DF-ISE file object
####
####	In:	DF-ISE object, , e.g.: dat=DFISE.readDAT(filenames)
####
####	Out:	Prints info to consol.
####		Returns 1 if sucessful
####
	print ('')
	print ("~~~~~~~~~~~~~~~~~~~~")
	print ('DF-ISE printDAT')
	print ("~~~~~~~~~~~~~~~~~~~~")
	print ('Dataset verification:')
	i=0
	for dataset in dat.DATA.datasets:
		print ('      '+ str(i) +'      '+ dataset.dataname +'      '+ dataset.validity +'  '+ dataset.dimension)
		i = i+1
	#
	print ("~~~~~~~~~~~~~~~~~~~~")
	print ('')
####
def writeDAT(data, output_filename):
#### File Writer for DF-ISE data ('.dat') files
####
####	In:	List of DF-ISE objects, e.g.: data=[DFISE.readDAT(filenames)]
####		Output filename string, e.g.: output_filename=str('PythonDFISEdatOUTPUT.dat')
####
####	Out:	Print ',dat' with specified filename, e.g.: program should exit if not success
####		Return 1 if completed
####				
####	
	## libraries provided by system
	import numpy as np
	import sys
	##

	if type(data)!=list: #correct if only 1 item provided
		data = [data]
	#
	
	if len(data) > 1:
		print ("ERROR: You must provide only 1 valid object data=[DFISE_DATfile1(, ...)]")
		return 0
		#print ("...... using 1st item only...") #feature depricated
	
	print ('')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('DF-ISE writeDAT')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('printing file: ' + output_filename)
	
	FILE0 = data[0] # first data object
	
	orig_stdout = sys.stdout # save the pointer for standard out
	to_write = open(output_filename, 'wb')
	sys.stdout = to_write # set the standard out pointer to the to_write file

	infos = FILE0.INFO
	dats = FILE0.DATA

	#header
	print ("DF-ISE text")
	print ("")

	#info
	print ("Info {")
	print ("  " + "version = " + str(infos.version))
	print ("  " + "type    = " + str(infos.type))
	print ("  " + "dimension   = " + str(infos.dimension))
	print ("  " + "nb_vertices = " + str(infos.nb_vertices))
	print ("  " + "nb_edges    = " + str(infos.nb_edges))
	print ("  " + "nb_faces    = " + str(infos.nb_faces))
	print ("  " + "nb_elements = " + str(infos.nb_elements))
	print ("  " + "nb_regions  = " + str(infos.nb_regions))

	print ("  " + "datasets    = ["),
	for each in infos.datasets:
		print ('"'+each+'"'),
	print ("]")

	print ("  " + "functions   = ["),
	for each in infos.functions:
		print (each),
	print ("]")

	print ("}")
	print ("")

	#data
	print ("Data {")
	print ("")

	for dataset in dats.datasets:
		print ('  Dataset ("' + dataset.dataname + '") {')
		print ('    function  = ' + dataset.function)
		print ('    type      = ' + dataset.type)
		print ('    dimension = ' + dataset.dimension)
		print ('    location  = ' + dataset.location)
		print ('    validity  = [ "' + dataset.validity + '" ]')
		print ('    Values (' + str(dataset.numValues) + ') {')
		
		valNum = 0
		for val in np.nditer(dataset.Values):
			if valNum%10==0 and valNum!=0: # every ten items
				print (' ') #space+newline
			#elif valNum%10==0 and valNum==0: # every ten items
				#print (' '),
			
			print (''),
			print ('%.15e' % float(val)),
			print (''),
			
			valNum = valNum+1
			
			#
		print(' ')
		print ('    }')
		print ('  }')
		print ('')

	print ('')
	print ('}')

	sys.stdout = orig_stdout #reset sys standard out pointer
	to_write.close()
	print ('~~~~~~~~~~~~~~~~~~~~')

	return 1
	
## END FUNCTION
def combineDAT(FILEmaster, FILE0, regions0, FILE1, regions1, field_names, field_dimensions, field_location):
#### Combine DF-ISE datasets
####
####	In:	Object to store resulting DF-ISE, e.g.: Filemaster=FILE0
####		File0, e.g.: FILE0=DFISE.readDAT(filename0)
####		Regions to consider in FILE0, regions0=['regA0'(, ...)]
####		File1, e.g.: FILE1=DFISE.readDAT(filename1)
####		Regions to consider in FILE1, e.g.: regions1=['regA1'(, ...)]
####		Fields to combine, e.g.: field_names=[ "PMIUserField0"(, ...)] 
####		Dimensions of those fields, e.g.: field_dimensions=[ "1"(, ...)] 
####		Location of the points, e.g.: field_location=[ "vertex"(, ...)] 
####
####	Out:	Print ',dat' with specified filename, e.g.: program should exit if not success
####		Return 1 if completed
####				
####	Note:	# must verify numValues are the same for two datasets, obviously
####		# must verify dataname, (function, type,) location, validity
####		# ()==warning
####		
####		
	## libraries provided by system
	import numpy as np
	##

	print ('')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('DF-ISE combineDAT')
	print ('~~~~~~~~~~~~~~~~~~~~')

	if len(regions0)!=len(regions1):
		print ('Number of regions in regions0 and regions1 do not match!')
	if len(field_names)!=len(field_dimensions) or len(field_names)!=len(field_location):
		print ('Number of regions in field_<info> do not match!!')


	print('files:	'+FILE0.filename+'	'+FILE1.filename)

	#regionNUM = 0
	#for region in regions0:
	fieldNUM = 0
	for field in field_names:
		regionNUM = 0
		for region in regions0:
			print('--> looking for	'+region)
			# find dataset indices in File0
			dataset0_index = []
			indexNUM = 0
			for dataset in FILE0.DATA.datasets:
				if dataset.validity==regions0[regionNUM] and dataset.dataname==field_names[fieldNUM] and dataset.dimension==field_dimensions[fieldNUM] and dataset.location==field_location[fieldNUM]:
					dataset0_index.append(indexNUM)
					print('	'+'File0: @'+str(indexNUM)+'	found	'+dataset.dataname+'	in	'+dataset.validity)
				else:
					#print('	'+'File0: @'+str(indexNUM)+'	!!!!	'+dataset.dataname+'	in	'+dataset.validity)
					pass
			
				#
				indexNUM = indexNUM+1
			#

			# find dataset indices in File1
			dataset1_index = []
			indexNUM = 0
			for dataset in FILE0.DATA.datasets:
				if dataset.validity==regions1[regionNUM] and dataset.dataname==field_names[fieldNUM] and dataset.dimension==field_dimensions[fieldNUM] and dataset.location==field_location[fieldNUM]:
					dataset1_index.append(indexNUM)
					print('	'+'File1: @'+str(indexNUM)+'	found	'+dataset.dataname+'	in	'+dataset.validity)
				else:
					#print('	'+'File1: @'+str(indexNUM)+'	!!!!	'+dataset.dataname+'	in	'+dataset.validity)
					pass
			
				#
				indexNUM = indexNUM+1
			#

			## now we have two lists, (hopefully of same length), where each element corresponds to dataset# to compare in DATA.datasets[#] --> in this case add .Values
			if len(dataset0_index)!=len(dataset1_index):
				print (' ERROR:	data files provided have some redundancy in validity/dataname.')
			#
			if len(dataset0_index)>1:
				print (' ERROR:	more than 1 dataset found for given region/info')
				print(len(dataset0_index))
			else:
				#print(len(dataset0_index))
				pass

			indexNUM = 0
			for each in dataset0_index:
				if FILE0.DATA.datasets[dataset0_index[indexNUM]].function!=FILE1.DATA.datasets[dataset1_index[indexNUM]].function:
					print('Warning:	the sets being combined do not match in functionname')
					print('		--> file0:	'+str(FILE0.DATA.datasets[dataset0_index[indexNUM]].function))
					print('		--> file1:	'+str(FILE1.DATA.datasets[dataset1_index[indexNUM]].function))
					pass
				if FILE0.DATA.datasets[dataset0_index[indexNUM]].type!=FILE1.DATA.datasets[dataset1_index[indexNUM]].type:
					print('Warning:	the sets being combined do not match in type')
					print('		--> file0:	'+str(FILE0.DATA.datasets[dataset0_index[indexNUM]].type))
					print('		--> file1:	'+str(FILE1.DATA.datasets[dataset1_index[indexNUM]].type))
					pass
				if FILE0.DATA.datasets[dataset0_index[indexNUM]].numValues!=FILE1.DATA.datasets[dataset1_index[indexNUM]].numValues:
					print('ERROR:	the sets being combined do not match in numValues')
					print('		--> file0:	'+str(FILE0.DATA.datasets[dataset0_index[indexNUM]].numValues))
					print('		--> file1:	'+str(FILE1.DATA.datasets[dataset1_index[indexNUM]].numValues))
					continue
				#

				## identifying info
				print('	adding	@'+str(each)+'	'+FILE0.DATA.datasets[dataset1_index[indexNUM]].validity),
				print (FILE0.DATA.datasets[dataset0_index[indexNUM]].dataname +'0	'+ FILE0.DATA.datasets[dataset1_index[indexNUM]].dataname+'1'),

				## great, now just add them already!
				tmp = np.add(FILE0.DATA.datasets[dataset0_index[indexNUM]].Values, FILE1.DATA.datasets[dataset1_index[indexNUM]].Values)
				FILEmaster.DATA.setField (dataset0_index[indexNUM], 'Values', tmp)

				if all(tmp == FILEmaster.DATA.datasets[dataset0_index[indexNUM]].Values):
					print('Sucess!')
				else:
					print('hmmph	'),
					print(type(FILE0.DATA.datasets[dataset0_index[indexNUM]].Values)),
					print('	'),
					print(type(FILE1.DATA.datasets[dataset1_index[indexNUM]].Values))

					print('	'),
					print(len(FILE0.DATA.datasets[dataset0_index[indexNUM]].Values)),
					print('	'),
					print(len(FILE1.DATA.datasets[dataset1_index[indexNUM]].Values))

					print('	'),
					print((FILE0.DATA.datasets[dataset0_index[indexNUM]].Values)[0]),
					print('	'),
					print((FILE1.DATA.datasets[dataset1_index[indexNUM]].Values)[0])

					print('	'),
					print(type(FILE0.DATA.datasets[dataset0_index[indexNUM]].Values[0])),
					print('	'),
					print(type(FILE1.DATA.datasets[dataset1_index[indexNUM]].Values[0])),
					print(np.add(FILE0.DATA.datasets[dataset0_index[indexNUM]].Values[0],FILE1.DATA.datasets[dataset1_index[indexNUM]].Values[0]))


				indexNUM = indexNUM+1
			# endADD
			regionNUM = regionNUM+1
		# endField
		fieldNUM = fieldNUM+1
	#endRegion
	print ('~~~~~~~~~~~~~~~~~~~~')
	return FILEmaster
## END FUNCTION
def extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions):
#### Extract datasets from a DF-ISE object to a matrix
####
####	In:	DF-ISE file object with data, e.g.: extract_file=DFISE.readDAT(filename)
####		Regions to consider in FILE0, extract_regions=['regA0'(, ...)]
####		Datasets to extract, e.g.: extract_fields=[ "PMIUserField0"(, ...)] 
####		Dimensions of those fields, e.g.: extract_dimensions=[ "1"(, ...)] 
####
####	Out:	A list of matrices, where each matrix is data corresponding to a region
####				
####	Note:	# datasets are extracted in order, size of matrix may vary...
####			... depending on available data in file
####		
	## libraries  provided by system
	import numpy as np
	##
	
	print ('')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('DF-ISE extractDAT')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('processing: ' + extract_file.filename)	
#	print ('~~~')
	print ('')

	data = []
	for region in extract_regions:
		print ("Region:	~" + region + "~")
		coords = []
		fieldnum = 0
		for field in extract_fields:
			#print field[fieldnum]
			for dataset in extract_file.DATA.datasets:
				if dataset.dataname==field and dataset.validity==region and dataset.dimension==extract_dimensions[fieldnum]:

					## scalar quantities
					if dataset.dimension == "1":
						## GRAB BY VALUE ##
						coords.append(dataset.Values)
					
					##vector quantities
					elif dataset.dimension == "3":
						pntsX = []
						pntsY = []
						pntsZ = []
						
						## GRAB BY VALUE ##
						valNUM = 1
						for each in dataset.Values:
							if valNUM == 1:
								pntsX.append(each)
								valNUM = 2
							elif valNUM == 2:
								pntsY.append(each)
								valNUM = 3
							elif valNUM == 3:
								pntsZ.append(each)
								valNUM = 1
						#

						#important!!! for dim=3, append 3 lists
						coords.append(pntsX)
						coords.append(pntsY)
						coords.append(pntsZ)
					#endif

					print ("---> retrieved: '" + field + "' in: " + region +" as dim"+str(dataset.dimension))
				#endmatch
			#end
			
			fieldnum = fieldnum+1
		#end
		
		#now we have all the coords and datapoints
		#break
		coords = np.asarray(coords)
		coords = np.asmatrix(coords)
		coords = coords.transpose()
		data.append(coords)

#		print ("~~~")
#		print ("~~~ ~~~~~~~ ~~~")
		print ("")
	#
	
	print ("Succesfully grabbed (" + str(len(data)) + ") regions of data with (1-3)d profiles.")
	print ('~~~~~~~~~~~~~~~~~~~~')
	return data
## END FUNCTION
def write2csv(data, output_prefix, regions):
#### Print extracte data to CSV
####
####	In:	List of data matrices, e.g.: data=extract2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
####		Output file prexis, e.g.: output_prefix='_ASL_write2csv'
####		Regions to print (filenames), e.g.: regions=['Reg0'(, ...)]
####
####	Out:	Prints a CSV file for each region with all data in data
####		Returns 1 if sucessful
####		
####	Note:	# Printing will overwrite for any filename collissions
####		
	## libraries  provided by system
	import numpy as np
	##
	
	if len(data) != len(regions):
		print ("~~~~")
		print (" length of 'data' and 'regions' not equal; they should be. exiting..")
		sys.exit(0)
	
	print ("Printing output files for each region (will overwrite) ...")
	i=0
	for item in data:

		name = output_prefix+'_Reg'+str(i)+'_'+str(regions[i])+'.csv'
		print (".... " + name),
		np.savetxt( name, item, delimiter=',', fmt="%e")
		#d.tofile(name, ",")
		print ("		OK")
		
		i = i+1
	# end

	print (" ")
	print ("Job completed.")
	print (" ")
	
	return 1
	#print "Printing output files for each region (will overwrite) ..."
## END FUNCTION
def buildDAT(insert_data, info, insert_filename, insert_regions, insert_dataname, insert_function, insert_type, insert_dimension, insert_location):
#### Build a DF-ISE file object from data and info provided
####
####	In:	DF-ISE file object with data, e.g.: extract_file=DFISE.readDAT(filename)
####		Regions to consider in FILE0, extract_regions=['regA0'(, ...)]
####		Datasets to extract, e.g.: extract_fields=[ "PMIUserField0"(, ...)] 
####		Dimensions of those fields, e.g.: extract_dimensions=[ "1"(, ...)] 
####
####	Out:	A list of matrices, where each matrix is data corresponding to a region
####				
####	Note:	# Currently: (fdgi) builds DAT from data and given a DFISE.INFO() object
####		# Currently: capable of building from scalar and vector data
####		
	## libraries  provided by system
	import numpy as np
	##
	print ('')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('DF-ISE buildDAT_fdgi') #from data given info ## from info given data, from info&data given 0, from 0 given info&data
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('building file: ' + insert_filename)	
	print ('')

	#### FROM DATA ####
	newDAT = DFISE_DATfile(insert_filename)
	if len(insert_data)!=len(insert_regions):
		print ("ERROR: len of regions should match len of data (list type)")
	if len(sum(insert_dataname,[]))!=len(sum(insert_function,[])) or len(sum(insert_function,[]))!=len(sum(insert_type,[])) or len(sum(insert_type,[]))!=len(sum(insert_dimension,[])) or len(sum(insert_dimension,[]))!=len(sum(insert_location,[])):
		print ("ERROR: list of lists should have same # of elements (necessary but not sufficient condition)")

	numDatasets = len(sum(insert_dataname,[])) #count datasets
	#newDAT.DATA.setNum(numDatasets)

	numDatasets = 0
	i=0
	for region in insert_regions:
		#when manipulating, easier operate on transpose, whose shape is  (#datasets,#rows)
		tempRegionData = insert_data[i].transpose()

		print ("Region:	~" + region + "~")
		datacol = 0
		j=0
		for dataset in insert_dataname[i]:

			tempD = Dataset()	
			tempD.dataname = insert_dataname[i][j]
			tempD.function = insert_function[i][j]
			tempD.type = insert_type[i][j]
			tempD.dimension =  insert_dimension[i][j]
			tempD.location = insert_location[i][j]
			tempD.validity = region
			if int(tempD.dimension)==1:
				#values = tempRegionData[datacol:datacol+int(tempD.dimension)].transpose()
				values = tempRegionData[datacol].transpose()
				#values = []
				#for each in tempRegionData[datacol:datacol+int(tempD.dimension)].transpose():
				#	values.append(each[0,0])
				#
			elif int(tempD.dimension)==2:
				values = []
				for each in tempRegionData[datacol:datacol+int(tempD.dimension)].transpose():
					values.append(each[0,0])
					values.append(each[0,1])
				#
			elif int(tempD.dimension)==3:
				values = []
				for each in tempRegionData[datacol:datacol+int(tempD.dimension)].transpose():
					values.append(each[0,0])
					values.append(each[0,1])
					values.append(each[0,2])
				#
			else:
				print ("ERROR: DIMENSION NOT VALID")
			#
		
			tempD.Values = np.asarray(values)
			tempD.numValues = (tempD.Values).size
			newDAT.DATA.datasets.append(tempD)

	#		print tempD.dataname,
	#		print tempD.function,
	#		print tempD.type,
	#		print tempD.dimension,
	#		print tempD.location,
	#		print tempD.validity,
	#		print tempD.numValues
#			print str(datacol), str(datacol+int(tempD.dimension))

	#		print i, j,
			print numDatasets,
			print newDAT.DATA.datasets[numDatasets].dataname,
			print newDAT.DATA.datasets[numDatasets].function,
			print newDAT.DATA.datasets[numDatasets].type,
			print newDAT.DATA.datasets[numDatasets].dimension,
			print newDAT.DATA.datasets[numDatasets].location,
			print newDAT.DATA.datasets[numDatasets].validity,
			print newDAT.DATA.datasets[numDatasets].numValues
#			print newDAT.DATA.datasets[numDatasets].Values.shape


			datacol = datacol+int(insert_dimension[i][j])
			j=j+1
			numDatasets = numDatasets+1
		#
		i=i+1
	#
	newDAT.DATA.numDatasets = numDatasets #not setNum, which makes empty Dataset() objects
	print ("")
	if newDAT.DATA.numDatasets == len(newDAT.DATA.datasets):
		print ("Collected "+str(newDAT.DATA.numDatasets)+" datasets ...ok!")
	else:
		print ("ERROR: numDatasets and len(datasets) do not match!")
	print ('~~~~~~~~~~~~~~~~~~~~')

	#### GIVEN INFO ####
	#info = info
	newDAT.INFO.version 	= info.version
	newDAT.INFO.type 	= info.type
	newDAT.INFO.dimension 	= info.dimension
	newDAT.INFO.nb_vertices	= info.nb_vertices
	newDAT.INFO.nb_edges	= info.nb_edges
	newDAT.INFO.nb_faces	= info.nb_faces
	newDAT.INFO.nb_elements	= info.nb_elements
	newDAT.INFO.nb_regions	= info.nb_regions
	newDAT.INFO.setField('datasets', sum(insert_dataname,[]))
	newDAT.INFO.setField('functions', sum(insert_function,[]))

	return newDAT
## END FUNCTION
####################################################################
####################################################################
