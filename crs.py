import rasterio
import numpy as np
from rasterio.windows import from_bounds

def crop_and_fill_to_bounds(input_raster, output_raster, common_bounds):
    with rasterio.open('LVIS2009/GeoTIFF/Merged2009.tif') as src:
        # Create a window based on the given common bounds
        window = from_bounds(*common_bounds, transform=src.transform)
        transform = src.window_transform(window)
        
        # Calculate the output size
        width = window.width
        height = window.height
        
        # Create a new array with no-data value
        nodata = src.nodata if src.nodata is not None else -9999
        data = np.full((int(height), int(width)), nodata, dtype=src.dtypes[0])
        
        # Read and place the data within the common bounds
        window_data = src.read(1, window=window, boundless=True, fill_value=nodata)
        data[:window_data.shape[0], :window_data.shape[1]] = window_data
        
        # Write the data to the output raster
        with rasterio.open(
            output_raster,
            'w',
            driver='GTiff',
            height=data.shape[0],
            width=data.shape[1],
            count=1,
            dtype=data.dtype,
            crs=src.crs,
            transform=transform,
            nodata=nodata
        ) as dst:
            dst.write(data, 1)

# Provided bounds
common_bounds = (-1602026.6020989993, -287230.75200707925, -1587559.2355732368, -252337.0128109111)

# Example Usage
raster1 = 'raster1.tif'
raster2 = 'raster2.tif'
output_raster1 = 'aligned_raster3.tif'
output_raster2 = 'aligned_raster4.tif'

# Crop and fill empty areas with no-data value using the provided bounds
crop_and_fill_to_bounds(raster1, output_raster1, common_bounds)
crop_and_fill_to_bounds(raster2, output_raster2, common_bounds)
