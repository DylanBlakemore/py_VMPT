import numpy as np

input_folder = raw_input("Enter the path to the fodler containing the location data: ")
input_fname = input_folder + "/locations.csv"

all_locations = np.genfromtxt(input_fname, delimiter=',')

print("Sorting location data...")
all_sorted = all_locations[np.argsort(all_locations[:,3])] # sort according to the time entry 

unique_times = np.unique(all_sorted[:,3])
num_intervals = unique_times.size





