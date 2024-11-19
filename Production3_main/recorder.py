#===== Standard Library
import os
import pathlib
import pickle
#===== 3rd party
#===== Reader
#=====
class Recorder:
    def __init__(self):
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'record.txt')
        pass
    
    def record(self, key, value):
        with open(self.path, 'rb') as fp:
            record_dict = pickle.load(fp)
        record_dict[key] = value
        with open(self.path, 'wb') as fp:
            pickle.dump(record_dict, fp)
    
    def read(self, key):
        with open(self.path, 'rb') as fp:
            record_dict = pickle.load(fp)
        if key is None:
            return record_dict
        return record_dict[key]
    
    def delete(self, key):
        with open(self.path, 'rb') as fp:
            record_dict = pickle.load(fp)
        record_dict.pop(key, None)
        with open(self.path, 'wb') as fp:
            pickle.dump(record_dict, fp)