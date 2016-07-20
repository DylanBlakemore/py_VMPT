import numpy as np
    
def getLowFraction(data, fraction):
    sorted_data = list(data)
    sorted_data.sort()
    largest_valid = sorted_data[int(len(data) * fraction)]
    
    indices = np.argwhere(data <= largest_valid)
        
    return indices[:,0]
    

