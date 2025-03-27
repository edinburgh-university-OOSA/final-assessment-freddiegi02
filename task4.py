import rasterio
from rasterio.fill import fillnodata
import numpy as np
import matplotlib.pyplot as plt


raster_file = rasterio.open('/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/Merged2009.tif')
out_fp = "/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/Merged2009FILL.tif"

raster = raster_file.read(1)
print(raster)

plt.imshow(raster, cmap='BrBG')
#plt.show()

mask_boolean = (raster !=-999)
print(mask_boolean)


# print(mask_numbers)

filled_raster = fillnodata(raster, mask = mask_boolean, max_search_distance = 100)

plt.imshow(raster, cmap='BrBG')
plt.colorbar(label="Elevation") 
plt.show()


out_meta = raster_file.meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": filled_raster.shape[0],
    "width": filled_raster.shape[1],
    "transform": raster_file.transform,
    "dtype": filled_raster.dtype,
        # Ensure correct data typea
})

with rasterio.open(out_fp, "w", **out_meta) as dest:
     dest.write(filled_raster, 1)



