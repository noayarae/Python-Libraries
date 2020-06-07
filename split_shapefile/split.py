# Created by:  Efrain Noa
# "D:\\research\\water_rights\\wr\\code\\split.py"
'''
Description: This code separate one shapefile into multiple ones based on 'idx' attribute
File:        "split.py"
How to use:
Input: 1) provide a shapefile to separate
       2) The field name 'idx' is reserved for this code
          (i.e. the input file MUST-NOT have a field named 'idx')
       3) provide one folder where multiple files should be stored (it is preferred a empty folder)
Output: Multiple files as rows the input file has
'''
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy, os, shutil, arcgisscripting, re
from arcpy.sa import *
#Import functions
#import add_field_way1
#import add_field_way2b as af

# Script created to separate one shapefile in multiple ones by one specific attribute
# Example for a Inputfile called "my_shapefile" and a field called "my_attribute"

def setup_inputs():
    #Set Input Output variables
    path = "D:\\research\\water_rights\\wr\\code\\input" # CHANGE path
    filename = "qq.shp" # CHANGE filename
    inputfile = os.path.join(path,filename)
    print "Input file: ", inputfile
    
    outDir = "D:\\research\\water_rights\\wr\\code\\output"
    print "Output folder: ", outDir; print

    ### 'idx' is a reserved name for this code
    field_name = "idx"
    
    add_field = add_populate_based_on_FID_field(inputfile, "idx") # ----> call function
    list_shpfiles = split_folder(inputfile, outDir) # -------> call function
    
    return

def setup_inputs_toolbox():
    in_file = arcpy.GetParameterAsText(0)
    out_folder = arcpy.GetParameterAsText(1)
    
    arcpy.AddMessage (in_file)
    arcpy.AddMessage (out_folder)
    arcpy.AddMessage ('\n')
    arcpy.AddMessage ('Building...')

    add_field = add_populate_based_on_FID_field(in_file, "idx") # ----> call function
    list_shpfiles = split_folder(in_file, out_folder) # -------> call function
    
    arcpy.AddMessage("done...")
    return

def add_populate_based_on_FID_field (inputfile, fieldname):
    
    ### Add field named "idx"
    '''arcpy.AddField_management(in_table=inputfile, field_name=fieldname,
                              field_type="LONG", field_precision="", field_scale="",
                              field_length="",field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="") #'''
    arcpy.AddField_management(in_table=inputfile, field_name=fieldname,
                              field_type="TEXT", field_precision="", field_scale="",
                              field_length="10", field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")
    
    ### Populate the "idx" field based on the "FID" field
    '''arcpy.CalculateField_management(in_table=inputfile, field=fieldname,
                                expression="[FID]+1", expression_type="VB", code_block="")#'''
    
    arcpy.CalculateField_management(in_table=inputfile, field=fieldname, expression="!FID! +1",
                                    expression_type="PYTHON_9.3", code_block="")
   

def split_folder(input_file, outDir):
    gp = arcgisscripting.create(9.3)
    gp.OverWriteOutput = 1
    
    ### Reads My_shapefile for attribute value
    rows = gp.searchcursor(input_file)
    #print "line 48: ", rows 
    row = rows.next()

    attributes = []
    while row:
        ### 'idx' is a reserved name for this code
        attributes.append(row.idx) #<-------- CHANGE "my_attribute" to the name of your attribute
        row = rows.next() # jump into the next row
        #print "attributes : ",attribute_types

    print "rows: ",attributes # Output a Shapefile for each different attribute
    
    list_shpfiles = []
    #for each_at in attribute_types:
    for each_at in attributes:
        ###print type(each_at) each attribute
        each_at_string = str(int(each_at))
        int_val = int(re.search(r'\d+',each_at_string).group()) #it gets integer value from a string (string variable is each_at)
        
        ###print int_val
        #outSHP = outDir + "u" + str(each_at) + ".shp"
        outSHP = outDir + "\\s" + str(int_val).zfill(4) + ".shp" # Prefix name for splitted file "u"
        print "Line 95: ", outSHP
        list_shpfiles.append(outSHP)
        ###print "each_at : ", each_at
        gp.Select_analysis (input_file, outSHP, "\"idx\" = '" + (each_at) + "'") #<-- CHANGE my_attribute to the name of your attribute

        arcpy.AddMessage("File: " + outSHP)
    
    del rows, row, attributes, gp
    print ("Splited into " + str(len(list_shpfiles)) + " files")
    
    return list_shpfiles # return a list called "list_shpfiles" containing all splitted files


if __name__ == "__main__":
    print "This code separates one shapefile into multiple ones"
    #list_shpfiles = setup_inputs()
    list_shpfiles = setup_inputs_toolbox()

    print "done ... "

'''
Ref:
https://www.youtube.com/watch?v=GiqPfqjNvxU
'''

