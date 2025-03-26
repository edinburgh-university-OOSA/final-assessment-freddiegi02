import rasterio
from rasterio.merge import merge
#from rasterio.plot import show
import glob
import os
from matplotlib import pyplot as plt
import numpy as np


dirpath = "/home/s2758252/OOSE/Summative/"
out_fp = "/home/s2758252/OOSE/Summative/OutputRaster/Merged2015.tif"

search_criteria = "lvisDEM2015*.tif"

q = os.path.join(dirpath, search_criteria)
print(q)

dem_fps = glob.glob(q)

print(dem_fps)

src_files_to_mosaic = []

for fp in dem_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)


print(src_files_to_mosaic)

mosaic, out_trans = merge(src_files_to_mosaic)

plt.imshow(mosaic[0], cmap='terrain')
#SSplt.show()

out_meta = src.meta.copy()

out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "count": mosaic.shape[0],
    "dtype": mosaic.dtype,
        # Ensure correct data typea
})

with rasterio.open(out_fp, "w", **out_meta) as dest:
     dest.write(mosaic)


