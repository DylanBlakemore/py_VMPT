# built-in libraries
import numpy as np
import os
import glob

from sklearn.cluster import DBSCAN
# custom classes
from lib import dataset
from lib import frame
from lib import plotter
from lib import lofpy
from lib import outlierremoval as orem

## Constants used throughout the algorithm ##
LINES_PER_TRACER = 100 # number of LOR's used per tracer
EPS = 5.0              # search distance used in both LOF and DBSCAN. Also separation distance
K   = 4                # number of points used in LOF and DBSCAN
########################

# get user input
input_folder = raw_input('Enter the path of the folder containing the input files: ')
output_folder = raw_input('Enter the name of the folder to which the output will be written: ')
num_tracers = int(raw_input('Enter the number of tracers expected: '))

# search the input folder for all files with the correct filetype (.dat)
print('Searching for .dat files in ' + input_folder)
search_path = os.path.join(input_folder,'*.dat')
input_files = glob.glob(search_path)

# define which files to triangulate
num_files = len(input_files)
start_file = 0
end_file = num_files
if end_file > num_files:
    end_file = num_files
    
# calculate the size (number of lines) of each frame
frame_size = LINES_PER_TRACER * num_tracers
    
for file_num in range(start_file, 1):#end_file

    file_path = input_files[file_num]
    print('Loading data from file ' + file_path)
    data_file = dataset.DataSet(file_path, frame_size)
    print('Data loaded')
    
    num_frames = data_file.getNumFrames()
    
    for frame_num in range(0, 1):#num_frames
        frame_data = data_file.getFrameAt(frame_num)
        poi = frame_data.getPointsOfInterest(EPS)
        
        all_points = frame_data.getPointsAt(poi['ind'])
        all_vols = poi['vol']
        
        lof = lofpy.getLOF(K, all_points)
        low_lof = orem.getLowFraction(lof, 0.5)
        
        lof_smoothed = all_points[low_lof,:]
        lof_smoothed_vols = np.array(all_vols)[low_lof]
        
        low_vol = orem.getLowFraction(lof_smoothed_vols, 0.6)
        
        # Actual points used in clustering
        remainders = lof_smoothed[low_vol,:]
        
        db = DBSCAN(eps=EPS, min_samples=K).fit(remainders)
        labels = db.labels_
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        print(n_clusters)
        
        locations = np.zeros((n_clusters,3))
        
        # Loop over clusters using 'where'
        for cluster in range(0, n_clusters):
            j = 1
         
        # Loop over all points individually
        #for i in range(0, len(low_vol)):
            
        
        
             
        
        