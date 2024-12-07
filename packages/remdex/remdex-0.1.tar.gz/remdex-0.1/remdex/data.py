import numpy as np
import os 

__data_path__:str = None
__available_numpy_names__ = []

class AccessDeniedError(Exception):
    def __init__(self, message:str = 'Data Access Denied') -> None:
        self.message = message
        super().__init__(self.message)

def get_numpy(name:str):
    if name not in __available_numpy_names__:
        raise AccessDeniedError()
    path = os.path.join(__data_path__, name)
    return np.load(path)
