# Extract precipitation values from Raster to 29 sites

import arcpy, os, sys, string, csv
from datetime import datetime

start_time = datetime.now()

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

from datetime import date, timedelta
print "running ..."
# Create a temporal directory
tmp_path_dir = os.path.join('D:/research/ML_model/data_from_pc', 'tmp') # Temporal directory
#os.mkdir(path)
if not os.path.exists(tmp_path_dir):
    os.makedirs(tmp_path_dir)


start_date = date(1999, 6, 1) # date(year, month, day)
end_date = date(1999, 9, 30) # This is included
delta = timedelta(days=1)
cc1 = 0
vals_table = []
while start_date <= end_date:
    print "----- Interation ",cc1+1
    #print(start_date.strftime("%Y-%m-%d"))
    yr = start_date.strftime("%Y")
    mo = start_date.strftime("%m")
    dy = start_date.strftime("%d")
    #print mo,dy,yr

    ### Here, set raster files downloaded from PRISM
    # For pp
    #ras_name = 'PRISM_ppt_stable_4kmD2_'+yr+mo+dy+'_bil.bil' # For pp
    #ras_file = 'D:/research/ML_model/data_from_pc/pp_1999/'+ras_name

    # For tmax
    #ras_name = 'PRISM_tmax_stable_4kmD2_'+yr+mo+dy+'_bil.bil' # For tmax
    #ras_file = 'D:/research/ML_model/data_from_pc/tmax_1999/'+ras_name

    # For tmean
    #ras_name = 'PRISM_tmean_stable_4kmD2_'+yr+mo+dy+'_bil.bil' # For tmax
    #ras_file = 'D:/research/ML_model/data_from_pc/tmean_1999/'+ras_name

    # For tmin
    #PRISM_tmin_stable_4kmD2_19990101_bil.bil
    ras_name = 'PRISM_tmin_stable_4kmD2_'+yr+mo+dy+'_bil.bil' # For tmax
    ras_file = 'D:/research/ML_model/data_from_pc/tmin_1999/'+ras_name
    #D:\research\ML_model\data_from_pc\tmin_1999
    
    #print ras_file

    out_file = tmp_path_dir+"/tmp_"+yr+mo+dy+".shp" # temporal file
    print out_file
    
    a1 = "D:/research/ML_model/arcmap_data/sites_29utm.shp" # Shape file
    a2 = ras_file #"D:/research/ML_model/data_from_pc/pp_1999/PRISM_ppt_stable_4kmD2_19990101_bil.bil" # Raster file
    a3 = out_file #"D:/research/ML_model/data_from_pc/pp_19990101.shp" # ouput shapefile

    ### Extract values from raster to points and create and shp file
    arcpy.gp.ExtractValuesToPoints_sa(a1, a2, a3,"INTERPOLATE","VALUE_ONLY")

    
    ### Read field values
    sites_val_f = a3 # "D:/research/ML_model/data_from_pc/"+"pp_19990101.shp" #"testdata.shp"    # The zip code shapefile
    lyr = "test_layer"     # The name of the Make Feature Layer output
    # Processes to make feature layer...
    arcpy.MakeFeatureLayer_management(sites_val_f, lyr)
    # Build search cursor for all 10.x...
    sbs, vals = [],[]
    search_1 = arcpy.SearchCursor(lyr, "", "", "OBSPRED_ID")
    for fcRow in search_1:
        sb = fcRow.getValue("OBSPRED_ID")
        sbs.append(sb)
        #print sb
    search_2 = arcpy.SearchCursor(lyr, "", "", "RASTERVALU")
    for fcRow in search_2:
        val = fcRow.getValue("RASTERVALU")
        vals.append(val) 
        #print val

    #print sbs
    print vals
    vals_table.append(vals)

    start_date += delta
    cc1 += 1

#out_csv = "D:/research/ML_model/data_from_pc/output1.csv" # For pp      <--- SET
#out_csv = "D:/research/ML_model/data_from_pc/tmax_all.csv" # For tmax   <--- SET
#out_csv = "D:/research/ML_model/data_from_pc/tmean_all.csv" # For tmean  <--- SET
out_csv = "D:/research/ML_model/data_from_pc/tmin_all.csv" # For tmean  <--- SET

with open(out_csv, "wb") as f1:
    writer = csv.writer(f1)
    #writer.writerows([["sb1","sb2"]])
    writer.writerows([sbs])
    writer.writerows(vals_table)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

### Extras
'''
### Cliping a raster by a shapefile
f1 = "D:/research/ML_model/data_from_pc/pp_1999/PRISM_ppt_stable_4kmD2_19990101_bil.bil" # Raster file
f2 = "D:/research/ML_model/data_from_pc/clip2" # Output shp file
f3 = "D:/research/ML_model/data_from_pc/square.shp" # mosaic/shep clip

arcpy.Clip_management(in_raster = f1,
                      rectangle="-123.316435970241 45.4831972927906 -122.903361539629 45.8182254024116",
                      out_raster = f2,
                      in_template_dataset= f3,
                      nodata_value="0", clipping_geometry="ClippingGeometry",
                      maintain_clipping_extent="NO_MAINTAIN_EXTENT")

### Convert raster to point
arcpy.RasterToPoint_conversion(in_raster="D:/research/ML_model/data_from_pc/clip1",
                               out_point_features="D:/research/ML_model/data_from_pc/dd1.shp",
                               raster_field="Value")
'''




