
from processLVIS import lvisGround #Importing lvisGround class from processLVIS
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments



##########################################

def getCmdArgs():
  # function description for use within python
  '''
  Get commandline arguments
  '''
  # Create an argparse object with a description
  ap = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  # Add a positional argument for the input filename (string)
  ap.add_argument("filename",type=str,help=("Input filename"))
  # Add a positional argument for the waveform index (integer)
  ap.add_argument("waveform",type=int,help=("Input Number"))
  # Parse the command-line arguments
  args = ap.parse_args()
  # return that object from this function
  return args

class plotLVIS(lvisGround):
  '''A class, ineriting from lvisData
     and add a plotting method'''

  def reprojectLVIS(self, outEPSG):
    '''Reprojects the geolocation data to a specified ESPG'''
    inProj=Proj("epsg:4326") #Input projection (WGS84)
    outProj=Proj("epsg:"+str(outEPSG)) #Output projection based on ESPG code
    self.long, self.lat=transform(inProj, outProj,self.lat,self.lon) #Transform projection 


  def plotWave(self, i):
    """Plots the wavefrom for the given index"""

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
    plt.plot(self.waves[i], self.z[i]) #plot waveform return vs elevation 
    plt.xlabel("Waveform return") # X-axis label
    plt.ylabel("Elevation (m)") # Y-axis label
    plt.show() #Dispaly the plot



##########################################


if __name__=="__main__":
  '''Main block'''
  
args = getCmdArgs() #Get the command line arguments
filename = args.filename   # Store the input filename 
waveform = args.waveform   #Store the waveform index

# create instance of class with "onlyBounds" flag
b=plotLVIS(filename,onlyBounds=True)

# Define spatial boundaries 
x0=b.bounds[0]
y0=b.bounds[1]
x1=(b.bounds[2]-b.bounds[0])/1+b.bounds[0]
y1=(b.bounds[3]-b.bounds[1])/1+b.bounds[1]

# read in all data within our spatial subset
lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1,setElev=True)

#Plot the choosen waveform
lvis.plotWave(waveform)

