# Created by Efrain Noa
# Description: This code add a new field into a existing shapefile
# File:     add_field_way1.py

# How to use:
# Input: 1) provide the folder address "path"
#        2) provide the filename "filename"
#        3) SHAPEFILE must have a field named "cota", otherwise setup the new field name in Line 42, for "Example 3"

# Output: The same input file having a new field populated
# ----------------------------------------------------------------------------------------
import arcpy, sys, os, re
from arcpy import env  # import env from arcpy module

def setup_inputs():
    # Set up path and filename
    # "D:\\hidro\\Z_JMA\\CCHHCCHH\\geographic_data\\procesos2"  # "E:\\thesis\\GAP_mobile3\\GAP_Copy\\GAP_analysis\\Output"
    
    #path = "D:\\hidro\\M_J_Python\\python_class\\Mod_1\\codes\\add_field_way1\\data"  # CHANGE path
    path = "D:\\08_hidro\\M_J_Python\\python_class\\Mod_1\\codes\\split_shapefile\\data"  # CHANGE path    
    filename = "dissolv.shp" # CHANGE filename
    inputfile = os.path.join(path,filename)
    print "shapefile: ",inputfile

    field_name = "cota"

    add_field(inputfile, field_name)                # <--------------  call function

def add_field(inputfile, field_name):

    ### Example 1: Add a blank field
    '''
    # New field called "subbasin", is created
    arcpy.AddField_management(inputfile, "subbasin", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")
    '''
    ### Example 2: Add a field, and populate with a constant value
    '''
    # New field called "subbasin", is created
    arcpy.AddField_management(inputfile, "subbasin", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")

    # "subbasin" is populated with a constant value
    arcpy.CalculateField_management(inputfile, "subbasin", "101", "VB", "#") #make sure about the constant value
    '''
    #### Example 3: Add a field, and fill it with a value from another existing field
    
    # New field called "code", is created
    # EXAMPLE: arcpy.AddField_management("file_name", "new_field_name", "type", "#digits", "#decimals","field_length","field_alias", "NULLABLE", "REQUIRED")
    new_fieldname = field_name + "_str"
    #arcpy.AddField_management(inputfile, "cota_str", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(inputfile, new_fieldname, "TEXT", "", "", "", "", "NULLABLE", "REQUIRED")

    # "Field_Name" is populated with a value from another existing field
    # EXAMPLE: arcpy.CalculateField_management("FileName", "Field_Name", "expression", "expression_type", "code_block") # example of expression = [MARKET_VAL]/[SHAPE_Area] for division
    #Parcel_2 = arcpy.CalculateField_management(inputfile, "cota_str", "[cota]", "VB", "#") #[MARKET_VAL]/[SHAPE_Area] for division
    Parcel_2 = arcpy.CalculateField_management(inputfile, new_fieldname, "["+ field_name + "]", "VB", "#") #[MARKET_VAL]/[SHAPE_Area] for division
    print (new_fieldname + " new field name: ")
    return new_fieldname

    #### Example 4: Add a field, and fill with a value related to its name
    '''
    # integer value from its name is gotten
    fill_value = int(re.search(r'\d+',inputfile).group()) #it gets integer value from a string (string variable is each_at)
    print fill_value
    
    # New field called "subbasin", is created
    arcpy.AddField_management(inputfile, "sbbn_2", "SHORT", "", "", "", "", "NULLABLE", "REQUIRED")

    # "code" is populated with a value from another existing field
    Parcel_2 = arcpy.CalculateField_management(inputfile, "subbasin", fill_value, "VB", "#") #populate with "fill_value"
    '''

    print "End add_field function"
    
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
