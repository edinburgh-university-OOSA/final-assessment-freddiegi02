import rasterio
from rasterio.merge import merge
from glob import glob
from src.handleTiff import TiffHandle  # Corrected import statement

# Get the list of tif files
dirpath = glob("LVIS2015/Datasets/*tif")
out_fp = "/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/Merged2015.tif"

mosaic_files = []

# Open each file without 'with' statement to keep the file open for merge
for file in dirpath:
    src = rasterio.open(file)
    mosaic_files.append(src)

# Merge the files
mosaic, out_trans = merge(mosaic_files)

# Get the resolution and bounding box from the merged raster
res = out_trans[0]  # Pixel resolution in X direction
minX = out_trans[2]  # X coordinate of the top-left corner
maxY = out_trans[5]  # Y coordinate of the top-left corner

# Create an instance of TiffHandle and save the mosaic
tiff_handler = TiffHandle()  # Corrected constructor
tiff_handler.writeTiff(mosaic[0], filename=out_fp, epsg=30321, res=res, minX=minX, maxY=maxY)

# Close the datasets after finishing the merge
for src in mosaic_files:
    src.close()
