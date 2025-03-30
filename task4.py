import rasterio
from rasterio.fill import fillnodata
import numpy as np
import matplotlib.pyplot as plt


raster_file = rasterio.open('LVIS2009/GeoTIFF/Merged2009.tif')
out_fp = "/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/Merged2009FILL.tif"

raster = raster_file.read(1)

mask_boolean = (raster !=-999)

filled_raster = fillnodata(raster, mask = mask_boolean, max_search_distance = 100)


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



