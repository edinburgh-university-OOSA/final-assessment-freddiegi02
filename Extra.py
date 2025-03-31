import rasterio
from rasterio.merge import merge
from glob import glob
import matplotlib.pyplot as plt
from src.handleTiff import tiffHandle  # Import the tiffHandle class

# Your coordinates
x0 = -102.00  # Set min x coordinate
y0 = -75.4    # Set min y coordinate
x1 = -99.00   # Set max x coordinate
y1 = -74.6    # Set max y coordinate

# Define resolution (for example, 0.01 degrees per pixel)
resolution = 0.01

# Get list of GeoTIFF file paths to merge
dirpath = glob("LVIS2015/Datasets/*tif")
out_fp = "/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/MergedAB.tif"

# Open each file and add it to the list
mosaic_files = []
for file in dirpath:
    src = rasterio.open(file)
    mosaic_files.append(src)

# Merge the files using rasterio.merge
mosaic, out_trans = merge(mosaic_files)
print(f"Merged mosaic shape: {mosaic.shape}")

# Display the mosaic (first band)
plt.imshow(mosaic[0], cmap='terrain')
plt.title("Merged Mosaic")
plt.show()

# Create an instance of the tiffHandle class
tiff = tiffHandle()

# Create and write the GeoTIFF with a fixed size
tiff.createFixedSizeTiff(x0, y0, x1, y1, resolution, out_fp, mosaic[0])

# Optionally, close the opened rasterio datasets
for src in mosaic_files:
    src.close()
