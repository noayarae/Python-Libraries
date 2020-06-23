# Created by Efrain Noa
# Description: This code computes the Composite Topographic Index
#              
# How to use:
# Input: 1) dem in raster format
#        2) output folder
#
# Output: 1) Two files: cti float and integer typr, both in raster format
# ----------------------------------------------------------------------------------------
import arcpy, sys, os #, re , arcgisscripting, arcinfo
from arcpy import env
from arcpy.sa import *

env.overwriteOutput = True
import numpy, math

def setup_inputs_manual():
    # Set up input file
    path = "X:\\noayarae\\project\\dem" #"E:\\hidro\\M_J_Python\\test1\\cartografia_base\\28_\\dem" # CHANGE path
    filename = "sloperad3" # CHANGE filename
    inputfile = os.path.join(path,filename)

    inputfile = "D:\\08_hidro\\piura\\only_piura_bs\\dem"
    
    # set up the output folder
    output_folder = "D:\\08_hidro\\piura\\only_piura_bs\\output"
    print "Input files...   done!!!"
    
    ### Call function to call other functions
    set_inputs_and_call_functions (inputfile,output_folder)
    

def setup_inputs_toolbox():
    dem_file = arcpy.GetParameterAsText(0)
    out_folder = arcpy.GetParameterAsText(1)
    
    arcpy.AddMessage ("Input file:    "+dem_file)
    arcpy.AddMessage ("Output folder: "+out_folder+'\n')
    #arcpy.AddMessage ('\n')
    #arcpy.AddMessage ('Building...')

    ### Call function to call other functions
    set_inputs_and_call_functions (dem_file,out_folder)
    
    arcpy.AddMessage("done...")
    return

def set_inputs_and_call_functions(dem,output_folder):
    '''
    fill = os.path.join(output_folder,"fill")
    fd = os.path.join(output_folder,"fd")
    dropfd = os.path.join(output_folder,"dropfd")
    sca = os.path.join(output_folder,"sca")
    slope = os.path.join(output_folder,"slope")
    slopeR = os.path.join(output_folder,"slopeR")
    tanslp = os.path.join(output_folder,"tanslp")
    corrsca = os.path.join(output_folder,"corrsca")
    #'''

    
    fill = os.path.join("in_memory","fill_c")
    fd = os.path.join("in_memory","fd_c")
    dropfd = os.path.join("in_memory","dropfd_c")
    sca = os.path.join("in_memory","sca_c")
    slope = os.path.join("in_memory","slope_c")
    slopeR = os.path.join("in_memory","slopeR_c")
    tanslp = os.path.join("in_memory","tanslp_c")
    corrsca = os.path.join("in_memory","corrsca_c")
    #'''
    
    cti = os.path.join(output_folder,"cti")
    cti_int = os.path.join(output_folder,"cti_int")

    # Call functions
    fill_tool(dem, fill)
    fd_tool(fill,fd,dropfd)     # Step 1
    fac_tool(fd,sca)            # Step 2
    get_slope(fill,slope)
    get_slopeRad(slope,slopeR)  # Step 3
    get_tan_slope(slopeR,tanslp) # Step 4
    get_correc_flowaccum(sca,corrsca)# Step 5
    calc_cti(corrsca, tanslp, cti)   # Step 6
    calc_cti_int(cti, cti_int)


### ------------------------------------------------------------------ 
def fill_tool(demfile, fill): # 
    arcpy.CheckOutExtension("Spatial")
    arcpy.gp.Fill_sa(demfile, fill, "")
    print "Fill tool...     done!!!"
    return

def fd_tool(fill, fd, dropfd): # Step 1
    arcpy.CheckOutExtension("Spatial")
    arcpy.gp.FlowDirection_sa(fill, fd, "NORMAL", dropfd)
    print "Fd tool...       done!!!"
    return

def fac_tool(fd, sca): # Step 2
    arcpy.CheckOutExtension("Spatial")
    arcpy.gp.FlowAccumulation_sa(fd, sca, "", "FLOAT")
    print "Fac tool...      done!!!"
    arcpy.AddMessage ("Flow accumulation...  done!")
    return

def get_slope(fill, slope): # 
    arcpy.CheckOutExtension("Spatial")
    zFactor = 1 # If x,y and z are in same units, z-factor=1. This is by default
    outSlope = Slope(fill, "DEGREE", zFactor)
    # Save the output 
    outSlope.save(slope)
    #print outfile
    print "Slope tool...    done!!!"
    return outSlope

def get_slopeRad(slope,slopeR): # Step 3
    arcpy.CheckOutExtension("Spatial")
    outPlus2 = (Raster(slope)* 1.570796)/90
    outPlus2.save(slopeR)
    print "slopeRad tool... done!!!"
    return slopeR

def get_tan_slope(slopeR,tanslp): # Step 4 (raster_cal3)
    arcpy.CheckOutExtension("Spatial")

    #print "Raster_calculator_3: tanslp. Outfule: ", outfile3
    outPlus3 = Con(Raster(slopeR)> 0,Tan(Raster(slopeR)),0.001)
    outPlus3.save(tanslp)

    #Con("%sloperad%" > 0,Tan("%sloperad%"),0.001)
    print "tanslope tool... done!!!"
    arcpy.AddMessage ("tanslope...  done!")
    return outPlus3

def get_correc_flowaccum(inputfile,outfile): # Step 5
    arcpy.CheckOutExtension("Spatial")

    description = arcpy.Describe(inputfile)  
    cellsize = description.children[0].meanCellHeight  
    #print cellsize 

    ### RAster calculator: step 5
    outPlus = (Raster(inputfile) + 1)*cellsize
    outPlus.save(outfile)
    print "corr_fac tool... done!!!"
    return outfile

def calc_cti(corrsca, tanslp, cti): #(raster_cal4)
    arcpy.CheckOutExtension("Spatial")
    outPlus4 = Ln(Raster(corrsca)/ Raster(tanslp))
    outPlus4.save(cti)
    print "cti tool...      done!!!"
    arcpy.AddMessage ("cti...  done!")
    return cti

def calc_cti_int(cti, cti_int):
    arcpy.CheckOutExtension("Spatial")
    outPlus5 = Int(Raster(cti) + 0.5)
    outPlus5.save(cti_int)
    print "cti_int tool...  done!!!"
    return cti_int
    
if __name__ == "__main__":
    print "CTI calculator is running ..."
    #setup_inputs_manual()
    setup_inputs_toolbox()
    print "Done  ... !!!  "
