import numpy as np


class Window:
    def __init__(self, type="Hanning"):
        
        if type == "Hanning":
            self.type = "Hanning"
        else:
            raise ValueError("Not supported window type!")
    
    def window(self, data: np.ndarray):
        return {
            "Hanning": data * np.hamming(data.size)
        }[self.type]
