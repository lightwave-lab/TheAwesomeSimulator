####################################################################
####################################################################
#### 	The Awesome Simulator, AwSimLib DFISE.py tester		####
####    						    	####
####	Author: Abhejit Rajagopal,  abhejit@ucla.edu	    	####
####    Date: 09/02/2014				    	####
####    		   				    	####
####    (ex_DFISE.py) is part of the AwSimLib software package 	####
####	module DFISE.py: /fileIO/DFISE.py		    	####
####    		    				    	####
####    This software is free to use, subjct to terms and   	####
####    	conditions in the AwSimLib license (LGPLv3).	####
####    AwSimLib license: ../_LICENSE.TXT		    	####
####################################################################
####################################################################
import sys
sys.path.append('../../')
from AwSimLib.fileIO import DFISE as DFISE

##### READ AND WRITE DF-ISE ####
#print ('Read and write test...	'),
#I = 'input/grids/DFISE_init.dat'
#O1 = 'output/_ASL_read0_write1.dat'
#O2 = 'output/_ASL_read1_write2.dat'
#O3 = 'output/_ASL_read2_write3.dat'

#[data] = DFISE.readDAT(I) #read from Sentaurus output
#DFISE.printDAT(data)
#writeSucess1 = DFISE.writeDAT(data,O1)
#print (writeSucess1),

### check stability by reading and writing consecutively
#[data2] = DFISE.readDAT(O1) #read from DFISE.py output
#DFISE.printDAT(data2)
#writeSucess2 = DFISE.writeDAT(data2,O2)
#print (writeSucess2),

#[data3] = DFISE.readDAT(O2) #read from DFISE.py output
#DFISE.printDAT(data3)
#writeSucess3 = DFISE.writeDAT(data3,O3)
#print (writeSucess3)

## manually compare with diff or other application (gui: Meld)
## all DATs written should be identical
## spacing should be different in Sentaurus output, but logically same
########

##### EXTRACT DATA AND WRITE TO CSV ####
### read-in DATs
#files = ['input/grids/DFISE_init.dat']
#[ExtractFile] = DFISE.readDAT(files)

### extract data from DAT to matrix
##params
#extract_file = ExtractFile # given this file with data...
#extract_regions = ["substrate_bot",  "cap",  "pillar", "substrate_top"] # for these regions
#extract_fields = ["DopingConcentration", "PMIUserField0", "PMIUserField1", "PMIUserField2", "NDopantActiveConcentration"] # ... extract these datasets
#extract_dimensions = ["1", "1", "1", "1", "1"]# ... having these dimensions

##extract
#DATAfields_extract = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract, 'output/_ASL_write2csv', extract_regions)
##########

##### COMBINE DATA IN DATs ####
###read-in DATs
#files = ['input/grids/DFISE_init.dat', 'input/grids/DFISE_init.dat']
#[FILE0,FILE1] = DFISE.readDAT(files)

### params for addition
#FILEmaster = FILE0 #note that this is a reference, not an operator
##app_functions = ["+", "+", "+", "+"] #TO DO: functions=['+', '-', '.*']
#regions0 = ["substrate_bot", "substrate_top", "pillar", "cap"] #regions for file0
#regions1 = ["substrate_bot", "substrate_top", "pillar", "cap"] #regions for file1
#field_names = [ "DopingConcentration"] 
#field_dimensions = ["1"]
#field_location = ["vertex"]
#output_filename = 'output/_ASL_combineDAT.dat'

### extract data from DAT to matrix to CSV (for verification)
#extract_file = FILE0 ## WE do this before combining since FILE0 is destroyed since it is passed by reference
#extract_regions = regions0
#extract_fields = ["PMIUserField0", "PMIUserField1", "PMIUserField2", "DopingConcentration"] # ... extract these datasets
#extract_dimensions = ["1", "1", "1", "1"]# ... having these dimensions
#DATAfields_extract = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract, 'output/_ASL_combineDAT_ORIG', extract_regions)

###routine
##only performs addition at the moment
#FILEcombined = DFISE.combineDAT(FILEmaster, FILE0, regions0, FILE1, regions1, field_names, field_dimensions, field_location)
#DFISE.writeDAT(FILEcombined, output_filename)


### extract data from DAT to matrix to CSV (for verification)
#extract_file = FILEcombined
#extract_regions = regions0
#extract_fields = ["PMIUserField0", "PMIUserField1", "PMIUserField2", "DopingConcentration"] # ... extract these datasets
#extract_dimensions = ["1", "1", "1", "1"]# ... having these dimensions
#DATAfields_extract = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract, 'output/_ASL_combineDAT_ADD', extract_regions)

### manually compare to see if values changed
#########

##### EXTRACT DATA AND BUILD DAT ####
#### Read in DAT, Write DAT, Extract, Write CSV
### read-in DATs
#files = ['input/grids/DFISE_init.dat']
#[ExtractFile] = DFISE.readDAT(files)

### (for build comparison): verify datasets and order in ExtractFile
#writeSucess0 = DFISE.writeDAT(ExtractFile,'output/_ASL_buildDAT_0writeDAT.dat')
#print ('writesucess0: '+str(writeSucess0))
#DFISE.printDAT(ExtractFile)

### extract data from DAT to matrix
#extract_file = ExtractFile # given this file with data...
#extract_regions = ["substrate_bot",  "cap",  "pillar", "substrate_top"] # for these regions
#extract_fields = ["DopingConcentration", "PMIUserField0", "PMIUserField1", "PMIUserField2", "NDopantActiveConcentration"] # ... extract these datasets
#extract_dimensions = ["1", "1", "1", "1", "1"]# ... having these dimensions
#DATAfields_extract = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract, 'output/_ASL_0buildDAT_writeDAT', extract_regions)
####

#### Extract, Build DAT, Write DAT, Read DAT, Write CSV

### build a DAT from data and given info object (SCALAR EXAMPLE) 
##params
#insert_data = DATAfields_extract #note that this is a reference not an operator
#insert_filename = 'output/_ASL_buildDAT_1scalar.dat'
#insert_regions = extract_regions #validity
#insert_dataname = [extract_fields]*len(insert_regions)
#insert_function = insert_dataname
#insert_type = [["scalar"]*len(extract_fields)]*len(insert_regions)
#insert_dimension = [extract_dimensions]*len(insert_regions)
#insert_location = [["vertex"]*len(extract_fields)]*len(insert_regions)
#info = ExtractFile.INFO

##routine
#newDAT = DFISE.buildDAT(insert_data, info, insert_filename, insert_regions, insert_dataname, insert_function, insert_type, insert_dimension, insert_location)
#DFISE.printDAT(newDAT) #console verification
#writeSucess1scalar = DFISE.writeDAT(newDAT, newDAT.filename) #print verification
#print ('writeSucess1scalar: '+str(writeSucess1scalar))
#print ('')

##verify by extracting and writing to CSV
#[newDAT_scalar] = DFISE.readDAT(newDAT.filename)
#extract_file = newDAT_scalar # given this file with data...
#extract_regions = insert_regions
#extract_fields = ["DopingConcentration", "PMIUserField0", "PMIUserField1", "PMIUserField2", "NDopantActiveConcentration"] # ... extract these datasets
#extract_dimensions = ["1", "1", "1", "1", "1"]# ... having these dimensions
#DATAfields_extract_scalar = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract_scalar, 'output/_ASL_1buildDAT_SCALAR', extract_regions)
###

### build a DAT from data and given info object (VECTOR EXAMPLE) 
#insert_data = DATAfields_extract #note that this is a reference not an operator
#insert_filename = 'output/_ASL_buildDAT_2vector.dat'
#insert_regions = ["substrate_bot",  "cap",  "pillar", "substrate_top"] # for these regions #validity
#insert_dataname = [["DopingConcentration", "POSVector", "NDopantActiveConcentration"]]*len(insert_regions)
#insert_function = insert_dataname
#insert_type = [["scalar", "vector", "scalar"]]*len(insert_regions)
#insert_dimension = [["1", "3", "1"]]*len(insert_regions)
#insert_location = [["vertex", "vertex", "vertex"]]*len(insert_regions)
#info = ExtractFile.INFO

##routine
#newDAT = DFISE.buildDAT(insert_data, info, insert_filename, insert_regions, insert_dataname, insert_function, insert_type, insert_dimension, insert_location)
#DFISE.printDAT(newDAT) #console verification
#writeSucess1vector = DFISE.writeDAT(newDAT, newDAT.filename) #print verification
#print ('writeSucess1vector: '+str(writeSucess1vector))
#print ('')

##verify by extracting and writing to CSV
#[newDAT_vector] = DFISE.readDAT(newDAT.filename)
#extract_file = newDAT_vector # given this file with data...
#extract_regions = insert_regions # for these regions
#extract_fields = ["DopingConcentration", "POSVector", "NDopantActiveConcentration"] # ... extract these datasets
#extract_dimensions = ["1", "3", "1"]# ... having these dimensions
#DATAfields_extract_vector = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract_vector, 'output/_ASL_2buildDAT_VECTOR', extract_regions)
###
####

### manually load files into a view to confirm
### original and scalar DAT should match identically
### original, scalar, and vector CSV should match identically
########
