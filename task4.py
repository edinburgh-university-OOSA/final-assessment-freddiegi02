import rasterio
import numpy as np


with rasterio.open('LVIS2015/GeoTIFF/Merged2015.tif') as src1, rasterio.open('LVIS2009/GeoTIFF/Merged2009.tif') as src2:
    data1 = src1.read(1)

    # extract metadata from the first raster
    meta = src1.meta.copy()
    print(meta)

    # read the window of the second raster with the same extent as the first raster
    window = src2.window(*src1.bounds)

    # read the data from the second raster with the same window as first raster
    data2 = src2.read(1, window=window, boundless=True, fill_value=-999)
    data2 = np.where(data2 == src2.nodata, 0, data2)
    print(window)
    # calculate the difference
    data = data1 - data2

    # write the result to a new raster
    with rasterio.open("output.tif", 'w', **meta) as dst:
        dst.write(data,1)