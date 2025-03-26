
from processLVIS import lvisGround
from pyproj import Proj, transform
from matplotlib import pyplot as plt
import numpy as np
from tiffExample import writeTiff


##########################################S

class plotLVIS(lvisGround):
  '''A class, ineriting from lvisData
     and add a plotting method'''

  def reprojectLVIS(self, outEPSG):
    '''Reprojects the geolocation data to a specified ESPG'''
    inProj=Proj("epsg:4326")
    outProj=Proj("epsg:"+str(outEPSG))
    self.long, self.lat=transform(inProj, outProj,self.lat,self.lon)


  def plotWave(self, i):

    # # Extract the waveform data
    # wave_data = self.waves[i]
    
    # # Find the first occurrence of zero and plot up to that point
    # cutoff_index = len(wave_data)
    # for j, value in enumerate(wave_data):
    #     if value == 0:
    #         cutoff_index = j
    #         break

    # Plot only up to the first zero
    #plt.plot(wave_data[:cutoff_index], self.z[i][:cutoff_index])
    plt.plot(self.waves[i], self.z[i])
    plt.xlabel("Waveform return")
    plt.ylabel("Elevation (m)")
    plt.show()



##########################################


if __name__=="__main__":
  '''Main block'''

filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_068453.h5'

  # create instance of class with "onlyBounds" flag
b=plotLVIS(filename,onlyBounds=True)


x0=b.bounds[0]
y0=b.bounds[1]
x1=(b.bounds[2]-b.bounds[0])/10+b.bounds[0]
y1=(b.bounds[3]-b.bounds[1])/10+b.bounds[1]

# read in all data within our spatial subset
lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1,setElev=True)
lvis.plotWave(0)

