# built-in libraries
import numpy as np
import os
import glob
import shutil
from ConfigParser import SafeConfigParser

from sklearn.cluster import DBSCAN
# custom classes
from lib import dataset
from lib import frame
from lib import plotter
from lib import lofpy
from lib import vmptutils as vuti

## Constants used throughout the algorithm, imported from the config.ini file ##
config = SafeConfigParser()
config.read('lib/config.ini')

LINES_PER_TRACER = config.getint('Frame','Lines_Per_Tracer') # number of LOR's used per tracer
EPS = config.getfloat('Cluster','Eps')                       # search distance used in both LOF and DBSCAN. Also separation distance
K   = config.getint('Cluster','K')                           # number of points used in LOF and DBSCAN
MAX_OUTPUT = config.getint('LocationOutput','Max_Output')    # maximum number of entries in the output array before writing to disk
PERCENT_INC = config.getfloat('LocationOutput','Percent_Int')# progress display increment
LOF_FRAC = config.getfloat('Filter','Lof_Frac')
VOL_FRAC = config.getfloat('Filter','Vol_Frac')
########################

# get user input
input_folder = raw_input('Enter the path of the folder containing the input files: ')
# create the ouput folder (delete first if it exists)
folder_exists = 1
while folder_exists:
    output_folder = raw_input('Enter the name of the folder to which the output will be written: ')
    folder_exists = os.path.exists(output_folder)
    if folder_exists:
        delete_folder = raw_input("Folder exists, delete? (y/n) ")
        if delete_folder == "y" or delete_folder == "Y":
            shutil.rmtree(output_folder)
            os.makedirs(output_folder)
            folder_exists = 0
    else:
        os.makedirs(output_folder)
              
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
    
for file_num in range(start_file, end_file):

    file_path = input_files[file_num]
    print('==================================================')
    print('Loading data from file ' + file_path)
    data_file = dataset.DataSet(file_path, frame_size)
    print('Data loaded')
    
    num_frames = data_file.getNumFrames()
    location_output = np.zeros((MAX_OUTPUT,4))
    output_index = 0
    
    file_percent_done = 0
    file_progress = 0
    
    # Total tracers located in the frame. Used to calculate the average
    # number of tracers.
    tracers_located = 0
    
    try:
        for frame_num in range(0, num_frames):
            frame_data = data_file.getFrameAt(frame_num)
            poi = frame_data.getPointsOfInterest(EPS)
            
            all_points = frame_data.getPointsAt(poi['ind'])
            all_vols = poi['vol']
            
            lof = lofpy.getLOF(K, all_points)
            low_lof = vuti.getLowFraction(lof, LOF_FRAC)
            
            lof_smoothed = all_points[low_lof,:]
            lof_smoothed_vols = np.array(all_vols)[low_lof]
            
            low_vol = vuti.getLowFraction(lof_smoothed_vols, VOL_FRAC)
            
            # Actual points used in clustering
            remainders = lof_smoothed[low_vol,:]
            
            db = DBSCAN(eps=EPS, min_samples=K).fit(remainders)
            labels = db.labels_
            
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            #print('Number of tracers detected: ' + str(n_clusters))
            locations = np.zeros((n_clusters,4))
            tracers_located = tracers_located + n_clusters
            
            # Loop over clusters using 'where'
            for cluster in range(0, n_clusters):
                cluster_inds = np.where(labels == cluster)[0]
                location = np.sum(remainders[cluster_inds,:], axis=0)/len(cluster_inds)
                locations[cluster,0:3] = location
                locations[cluster,3] = frame_data.getFrameTime()
        
            if output_index + n_clusters >= MAX_OUTPUT:
                vuti.writeOutputToFile(output_folder, location_output)
                location_output = np.zeros((MAX_OUTPUT,4))
                output_index = 0
                location_output[output_index:output_index+n_clusters,:] = locations
                output_index += n_clusters
            else:
                location_output[output_index:output_index+n_clusters,:] = locations
                output_index += n_clusters
                
            # If the percent completed is greater than the next integer, print the progress
            file_percent_done = (float(frame_num) + 1)/float(num_frames)
            if file_percent_done >= file_progress + PERCENT_INC:
                average_num_tracers = float(tracers_located)/float(frame_num + 1)
                file_progress = file_progress + PERCENT_INC
                vuti.printProgress(file_num, file_progress, average_num_tracers)
            
        vuti.writeOutputToFile(output_folder, location_output)
    # If the user uses Cntrl+C to cancel the processing, print the location data to file
    except KeyboardInterrupt, SystemExit:
        print('\n Operation cancelled, writing data to file...')
        vuti.writeOutputToFile(output_folder, location_output)
        raise
            
                
        
# Sort the final output file according to timestamp
             
        
        