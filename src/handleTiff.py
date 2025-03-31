from osgeo import gdal, osr
import numpy as np

class TiffHandle():
    '''
    Class to handle GeoTIFF file writing
    '''

    def __init__(self):
        '''
        Class initializer (No need for complex properties)
        '''
        pass

    def writeTiff(self, data, filename="output.tif", epsg=30321, res=None, minX=None, maxY=None):
        '''
        Write a GeoTIFF from a raster layer
        '''
        # Ensure essential parameters are provided
        if res is None or minX is None or maxY is None:
            raise ValueError("Resolution, minX, and maxY must be provided")

        # Get the shape of the data (mosaic)
        nY, nX = data.shape  # Check shape of data
        print(f"Data shape: {nY} x {nX}")

        # Adjust for the projection (flip X and Y based on EPSG:30321)
        # In EPSG:30321, it seems minX is the maximum X and maxY is the minimum Y
        geotransform = (minX, res, 0, maxY, 0, -res)
        print(f"Geotransform: {geotransform}")

        # Create the GeoTIFF file
        dst_ds = gdal.GetDriverByName('GTiff').Create(filename, nX, nY, 1, gdal.GDT_Float32)
        dst_ds.SetGeoTransform(geotransform)

        # Set the spatial reference (projection)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)
        dst_ds.SetProjection(srs.ExportToWkt())

        # Write the data to the GeoTIFF
        dst_ds.GetRasterBand(1).WriteArray(data)
        dst_ds.GetRasterBand(1).SetNoDataValue(-999)
        dst_ds.FlushCache()  # Save to disk

        dst_ds = None  # Close the file
        print(f"Image written to {filename}")
