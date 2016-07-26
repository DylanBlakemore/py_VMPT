# Class define a 'track', which contains a location history for a single tracer.
# All tracks for a given location set will have the same length, being equal to
# the number of unique time steps. Where a location does not exist at a time t_i,
# the location x_i is set to [nan, nan, nan] 
import numpy as np

class Track:
    def __init__(self, initial_point=None, track_length):
        self.n_skips = 0
        self.length = track_length
        if initial_point is None:
            self.x_0 = np.array([0.0, 0.0, 0.0])
            self.t_0 = 0
        else:
            self.x_0 = initial_point[0:3]
            self.t_0 = initial_point[3]
      
    # Adds an entry to the end of the track history.
    # new_location is a numpy array with format [x,y,z,t]
    def appendLocation(self, new_location):
        return None
    
    # Used when no new location is found for the new time step.
    def appendNone(self, new_time):
        return None
      
    # Returns the theoretical next position based on the most recent locations.
    # t_ext is the time for which the extrapolated position is calculated.
    def getExtrapolatedPosition(self, t_ext):
        return None
    
    # Private method to update the history (positions, velocities etc.)
    def _updateHistory(self):
        return None
        
    
            
        

