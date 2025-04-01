from osgeo import gdal, osr
import numpy as np

class TiffHandle():
    '''
    Class to handle GeoTIFF file writing with a fixed output size
    '''
    
    def __init__(self, fixed_shape=(256, 256)):  # Default output size
        self.fixed_shape = fixed_shape

    def writeTiff(self, data, filename="output.tif", epsg=30321, res=None, minX=None, maxY=None):
        '''
        Write a GeoTIFF with a fixed output size.
        '''
        if res is None or minX is None or maxY is None:
            raise ValueError("Resolution, minX, and maxY must be provided")

        nY, nX = data.shape
        print(f"Original data shape: {nY} x {nX}")

        # Ensure output data has the fixed size
        fixed_nY, fixed_nX = self.fixed_shape
        fixed_data = np.full((fixed_nY, fixed_nX), -999, dtype=np.float32)  # Fill with NoData value

        # Crop or pad data to match the fixed shape
        min_nY = min(nY, fixed_nY)
        min_nX = min(nX, fixed_nX)
        fixed_data[:min_nY, :min_nX] = data[:min_nY, :min_nX]  # Copy valid data

        print(f"Output data shape: {fixed_nY} x {fixed_nX}")

        # Adjust geotransform based on fixed size
        geotransform = (minX, res, 0, maxY, 0, -res)
        print(f"Geotransform: {geotransform}")

        # Create the GeoTIFF file
        dst_ds = gdal.GetDriverByName('GTiff').Create(filename, fixed_nX, fixed_nY, 1, gdal.GDT_Float32)
        dst_ds.SetGeoTransform(geotransform)

        # Set spatial reference
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)
        dst_ds.SetProjection(srs.ExportToWkt())

        # Write fixed-size data
        dst_ds.GetRasterBand(1).WriteArray(fixed_data)
        dst_ds.GetRasterBand(1).SetNoDataValue(-999)
        dst_ds.FlushCache()  # Save to disk

        dst_ds = None  # Close file
        print(f"Image written to {filename}")
