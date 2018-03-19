# Created by Efrain Noa
# Description: This code add a new field into a existing shapefile
# File:     add_field_way1.py

# How to use:
# Input: 1) provide the folder address "path"
#        2) provide the filename "filename"
#        3) SHAPEFILE must have a field named "cota", otherwise setup the new field name in Line 42, for "Example 3"

# Output: The same input file having a new field populated
# ----------------------------------------------------------------------------------------
import arcpy, sys, os, re, arcgisscripting
from arcpy.sa import *
from arcpy import env  # import env from arcpy module

def setup_inputs():
    # Set up path and filename
    '''
    # "D:\\hidro\\Z_JMA\\CCHHCCHH\\geographic_data\\procesos2"  # "E:\\thesis\\GAP_mobile3\\GAP_Copy\\GAP_analysis\\Output"
    path = "D:\\hidro\\M_J_Python\\python_class\\Mod_1\\codes\\add_field_way1\\data"  # CHANGE path
    filename = "dissolv.shp" # CHANGE filename
    inputfile = os.path.join(path,filename)
    print "shapefile: ",inputfile
    #'''

    current_path = sys.argv[0] ## Get current full filename, where ever it is located
    #print "current_path:  ",current_path; print
    # Get the grand parent path
    grand_parent_folder = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_path, os.pardir)), os.pardir))
    # Get the parent path
    parent_folder = os.path.join(os.path.abspath(os.path.join(current_path, os.pardir)))
    #print "grand parent folder:  ",grand_parent_folder; print
    #print "parent folder:  ",parent_folder; print

    input_file = parent_folder + "\\data\\d1.shp" # <--------  INPUT
    print "Input file: ", input_file
    #sys.exit()
        
    add_field(input_file)                # <--------------  call function


def add_field(inputfile):
#### Example 5: Add a field, and fill it with sequential values from 0 to n
    
    field_names = [f.name for f in arcpy.ListFields(inputfile)] # Extract the field_names from the input shapefile
    #print (field_names[0])
    
    # New field called "FID2", is created
    # EXAMPLE: arcpy.AddField_management("file_name", "new_field_name", "type", "#digits", "#decimals","field_length","field_alias", "NULLABLE", "REQUIRED")
    new_fieldname = "FID" + "2"
    #arcpy.AddField_management(inputfile, "cota_str", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(inputfile, new_fieldname, "TEXT", "", "", "", "", "NULLABLE", "REQUIRED")

    # "Field_Name" is populated with a value from another existing field (from main FID)
    # EXAMPLE: arcpy.CalculateField_management("FileName", "Field_Name", "expression", "expression_type", "code_block") # example of expression = [MARKET_VAL]/[SHAPE_Area] for division
    #Parcel_2 = arcpy.CalculateField_management(inputfile, "cota_str", "[cota]", "VB", "#") #[MARKET_VAL]/[SHAPE_Area] for division
    #Parcel_2 = arcpy.CalculateField_management(inputfile, new_fieldname, "["+ field_name + "]", "VB", "#") #[MARKET_VAL]/[SHAPE_Area] for division
    Parcel_2 = arcpy.CalculateField_management(inputfile, new_fieldname, "["+ field_names[0] + "]", "VB", "#") #[MARKET_VAL]/[SHAPE_Area] for division

    print (new_fieldname + "  field was added...")
    #'''

if __name__ == "__main__":
    print "This code add a new field into a existing shapefile"
    setup_inputs()

'''
name1 = arcpy.ListFields("Parcel.shp")
for a in name1:
    n = a.name
    print n

print "field 1: ",name1[0]
print "name n ", n
'''
