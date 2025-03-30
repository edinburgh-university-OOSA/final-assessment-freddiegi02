import rasterio
from rasterio.merge import merge
from glob import glob
from matplotlib import pyplot as plt

dirpath = glob("/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/*tif")
out_fp = "/home/s2758252/OOSE/Summative/final-assessment-freddiegi02/MergedAB.tif"

mosacic_files = []

for files in dirpath:
    src = rasterio.open(files)
    mosacic_files.append(src)


mosaic, out_trans = merge(mosacic_files)

out_meta = src.meta.copy()

out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "count": mosaic.shape[0],
    "dtype": mosaic.dtype,
})

with rasterio.open(out_fp, "w", **out_meta) as dest:
     dest.write(mosaic)


