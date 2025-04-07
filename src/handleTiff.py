from osgeo import gdal, osr
import numpy as np

class TiffHandle:
    '''
    Class to handle GeoTIFF file writing with a flexible pixel size based on X and Y extent.
    '''

    def writeTiff(self, data, filename="output.tif", epsg=3031, transform=None):
        '''
        Write a GeoTIFF with a specified geotransform.
        '''
        if transform is None or len(transform) != 6:
            raise ValueError("Transform must be a six-element sequence")

        nY, nX = data.shape
        print(f"Original data shape: {nY} x {nX}")

        # Create an output array filled with NoData value
        output_data = np.full((nY, nX), -999, dtype=np.float32)

        # Copy input data into the output array
        output_data[:nY, :nX] = data

        print(f"Output data shape: {nY} x {nX}")

        # Define the geotransform from the provided transform
        geotransform = transform
        print(f"Geotransform: {geotransform}")

        # Create the GeoTIFF file
        dst_ds = gdal.GetDriverByName('GTiff').Create(filename, nX, nY, 1, gdal.GDT_Float32)
        dst_ds.SetGeoTransform(geotransform)

        # Set spatial reference
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)
        dst_ds.SetProjection(srs.ExportToWkt())

        # Write the data to the file
        dst_ds.GetRasterBand(1).WriteArray(output_data)
        dst_ds.GetRasterBand(1).SetNoDataValue(-999)
        dst_ds.FlushCache()

        dst_ds = None  # Close file
        print(f"Image written to {filename}")

