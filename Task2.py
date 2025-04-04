
'''
Plotting a singular plot
'''

import tracemalloc
from src.tiffExample import writeTiff # Import function to write GeoTIFF files
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
from glob import glob #Import to help with multiple files and folders
import os #Import for file and directory handling
from src.Commands import getCmdArgs, norm_lon



tracemalloc.start()

##########################################S

class plotLVIS(lvisGround):
  """
  A class inheriting from lvisGround and adding additional methods 
  for reprojecting geolocation data and writing DEM files.
  """

  def writeDEM(self,res,outName):
    '''Write LVIS ground elevation data to a geotiff'''
    writeTiff(self.zG,self.long,self.lat,res,filename=outName,epsg=3031)
    return

if __name__=="__main__":
  '''Main block'''

  # read the command line
  args = getCmdArgs()
  filename = args.filename #Store input filename
  res = args.res #Store spatial resolution
  year = args.year #Store the year


  x0 = norm_lon(-102.00) # set min x coord
  y0 = -75.4 # set min y coord
  x1 = norm_lon(-99.00) #set max x coord
  y1 = -74.6 #set max y coord
 
  file_count = 1 #Make the file count 1 at the start

  step_x = (x1 - x0) / 5 # Divide the x-range into 6 tiles
  step_y = (y1 - y0) / 5 # Divide the y-range into 6 tiles

  for tile_x0 in np.arange(x0,x1, step_x):
    tile_x1=tile_x0+step_x
    for tile_y0 in np.arange(y0, y1, step_y):
      tile_y1=tile_y0+step_y
      
      try:
          #read in all data within our spatial subset
        lvis=plotLVIS(filename,minX=tile_x0,minY=tile_y0,maxX=tile_x1,maxY=tile_y1,setElev=True)


        lvis.reprojectLVIS(3031) # Reproject the data to the Antarctic Polar Stereographic projection (EPSG 3031)
        lvis.estimateGround() #Call the estimate ground function
        outName = f"LVIS{year}/Datasets/T2_DEM_{file_count}.tif"  # Estimate ground elevation from LVIS data
        file_count +=1 #Increase the file size by one each time
        lvis.writeDEM(res, outName) # Write the DEM data to a GeoTIFF file with the specified resolution
      
      except AttributeError as e:
        print(f"{filename} Skipped") #Print the files which have been skipped
  
# Call the merge fuction
# Use the current working directory for the input files and output file
current_dir = os.getcwd()
dirpath = glob(f"{current_dir}/LVIS{year}/Datasets/T2*tif")
#Outpaths for all of the Merged files
out_fp = f"{current_dir}/LVIS{year}/GeoTIFF/T2_Merged{year}.tif"
lvis.mergeDEM(year, dirpath, out_fp) 
plt.title(f"PIG Elevation for the {year}")
# Save the figure as a PNG with the specified DPI and tight bounding box
plt.savefig(f"Output_Images/PIG_Single_{year}.png", dpi=75, bbox_inches='tight')




# Call Memory Function to get the currnet and peak memory in bytes
current, peak = tracemalloc.get_traced_memory()
# Convert bytes to GB
current_mb = current / 10**9
peak_mb = peak / 10**9
# Print memory usage details
print(f"Current memory usage: {current_mb:.2f} GB")
print(f"Peak memory usage: {peak_mb:.2f} GB")
# Stop tracing memory
tracemalloc.stop()