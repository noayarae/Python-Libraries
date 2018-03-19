# Created by:  Efrain Noa
'''
Description: This code separate one shapefile in multiple ones by one specific attribute
File:        "split.py"
How to use:
Input: 1) provide a shapefile to separate
       2) Shapefile MUST have a field name "cota" with cota values   <-------------
       3) provide a empty folder where multiple files should be stored
Output: Multiple files as rows the input file has
'''
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy, os, shutil, arcgisscripting, re, ntpath
from arcpy.sa import *
#Import functions
import add_field_way1
import add_field_wiht_seq_values as afs

# Script created to separate one shapefile in multiple ones by one specific attribute
# Example for a Inputfile called "my_shapefile" and a field called "my_attribute"

def setup_inputs():
    #Set Input Output variables
    #<-------> CHANGE. provide input file which will be splitted
    #input_file = u"D:\\hidro\\M_J_Python\\python_class\\Mod_1\\codes\\split\\data\\dissolv.shp"  #u"E:\\LowerWabash\\Indna_wtlnd\\outlet2.shp" #<-- CHANGE. provide input file which will be splitted
    '''              
    input_file = u"D:\\08_hidro\\M_J_Python\\python_class\\Mod_1\\codes\\split_shapefile\\data\\dissolv.shp"                  
    print "Input file: ", input_file
    outDir = u"D:\\08_hidro\\M_J_Python\\python_class\\Mod_1\\codes\\split_shapefile\\" #<-- CHANGE. provide folder name where it will be splitted
    print "Output folder: ", outDir; print
    '''
    
    current_path = sys.argv[0] ## It gets current full filename, where ever it is located
    #print "current_path:  ",current_path; print
    # it gets the grand parent path
    grand_parent_folder = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_path, os.pardir)), os.pardir))
    # it gets the parent path
    parent_folder = os.path.join(os.path.abspath(os.path.join(current_path, os.pardir)))
    #print "grand parent folder:  ",grand_parent_folder; print
    #print "parent folder:  ",parent_folder; print
    
    input_file = parent_folder + "\\data\\d2.shp" # <--------  INPUT
    print "Input file: ", input_file
    outDir = parent_folder
    #print "Output folder: ", outDir; print


    list_shpfiles = split_folder(input_file, outDir) # <------------------  call function
    return list_shpfiles

#def split_folder(input_file, fieldname, outDir):
def split_folder(input_file, outDir):
    gp = arcgisscripting.create(9.3)
    gp.OverWriteOutput = 1

    afs.add_field(input_file) #        <---------------  call function
    
    fieldname = "FID2"
    
    # Create a folder to store split files
    # Check if "...\\output" folder does exist
    output_folder = outDir + "\\output"
    if not os.path.exists(outDir + "\\output"):
        os.makedirs(outDir + "\\output") # it creates a ordinary directory
    else:
        shutil.rmtree(outDir + "\\output") # delete files from "..\GAP_pre_process\output" folder
        os.makedirs(outDir + "\\output") # create again "..\GAP_pre_process\output" folder
        print "Line 63: The given name for the NEW directory already exist"

    # Create new field named such as "cota_str"
    new_fieldname = add_field_way1.add_field(input_file, fieldname) #        <---------------  call function
    ###print "new_fieldname:  ",new_fieldname
    #print 'new field "'+ new_fieldname +'" was created...';
    print
    
    # Reads My_shapefile for different values in the attribute
    rows = gp.searchcursor(input_file)
    ###print "line 54: ", rows 
    row = rows.next()

    attributes = []
    while row:
        #Example: attributes.append(row.cota_str) #
        #attributes.append(row.cota_str) #<--------------- CHANGE "my_attribute" to the name of your attribute
        attributes.append(row.FID2_str) 
        row = rows.next() # jump into the next row
        #print "attributes : ",attribute_types

    #print "rows: ",attributes # Output a Shapefile for each different attribute
    
    list_shpfiles = []
    #for each_at in attribute_types:
    for i,each_at in enumerate (attributes,1):
        #print (each_at, type(each_at)) #each attribute
        each_at_string = str(i)
        int_val = int(re.search(r'\d+',each_at_string).group()) #it gets integer value from a string (string variable is each_at)

        just_filename = ntpath.basename(input_file) # Extract file name from path, no matter what the os/path format
        f_name = os.path.splitext(just_filename)[0] # Extract the file_name without extension
        
        ###print int_val
        #outSHP = outDir + "u" + str(each_at) + ".shp"
        #outSHP = split_folder + "\\s" + str(int_val).zfill(4) + ".shp" # Prefix name for splitted file "u"
        outSHP = output_folder + "\\"+ f_name +"_"+ str(int_val).zfill(4) + ".shp" # Prefix name for splitted file "u"
        print "Line 98: ", outSHP
        list_shpfiles.append(outSHP)
        ###print "each_at : ", each_at
        #gp.Select_analysis (input_file, outSHP, "\"cota\" = '" + (each_at) + "'") #<-- CHANGE my_attribute to the name of your attribute
        #gp.Select_analysis (input_file, outSHP, "\"cota_str\" = '" + (each_at) + "'") #<-- CHANGE my_attribute to the name of your attribute
        gp.Select_analysis (input_file, outSHP, "\"FID2_str\" = '" + (each_at) + "'") #<-- CHANGE my_attribute to the name of your attribute
    
    del rows, row, attributes, gp
    print ("Split into " + str(len(list_shpfiles)) + " files is done...")
    return list_shpfiles # return a list called "list_shpfiles" containing all splitted files

if __name__ == "__main__":
    print "This code separate one shapefile into multiple ones by a specific attribute"
    list_shpfiles = setup_inputs()
    
'''
# Original
# Script created to separate one shapefile in multiple ones by one specific
# attribute

# Example for a Inputfile called "my_shapefile" and a field called "my_attribute"
import arcgisscripting

# Starts Geoprocessing
gp = arcgisscripting.create(9.3)
gp.OverWriteOutput = 1

#Set Input Output variables
inputFile = u"C:\\GISTemp\\My_Shapefile.shp" #<-- CHANGE
outDir = u"C:\\GISTemp\\" #<-- CHANGE

# Reads My_shapefile for different values in the attribute
rows = gp.searchcursor(inputFile)
row = rows.next()
attribute_types = set([])

while row:
    attribute_types.add(row.my_attribute) #<-- CHANGE my_attribute to the name of your attribute
    row = rows.next()

# Output a Shapefile for each different attribute
for each_attribute in attribute_types:
    outSHP = outDir + each_attribute + u".shp"
    print outSHP
    gp.Select_analysis (inputFile, outSHP, "\"my_attribute\" = '" + each_attribute + "'") #<-- CHANGE my_attribute to the name of your attribute

del rows, row, attribute_types, gp

#END
'''
