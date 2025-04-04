import rasterio
import numpy as np
from rasterio.windows import from_bounds

def extent(input_raster, output_raster, common_bounds):

    """
    Crops an input raster to a specified bounding box and writes the output to a new raster file.
    
    Parameters:
        input_raster (str): Path to the input raster file.
        output_raster (str): Path to save the output raster file.
        common_bounds (tuple): Bounding box (min_x, min_y, max_x, max_y) for cropping.
    """
    with rasterio.open(input_raster) as src:
        # Create a window based on the given common bounds
        window = from_bounds(*common_bounds, transform=src.transform)
        transform = src.window_transform(window)
        
        # Calculate the output size
        width = int(window.width)
        height = int(window.height)
        
        # Set no-data value to -999
        nodata = src.nodata if src.nodata is not None else -999
        data = np.full((height, width), nodata, dtype=src.dtypes[0])
        
        # Read and place the data within the common bounds
        window_data = src.read(1, window=window, boundless=True, fill_value=nodata)
        data[:window_data.shape[0], :window_data.shape[1]] = window_data
        
        # Write the data to the output raster
        with rasterio.open(
            output_raster,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=src.crs,
            transform=transform,
            nodata=nodata  # Ensure -999 is stored as nodata
        ) as dst:
            dst.write(data, 1)

