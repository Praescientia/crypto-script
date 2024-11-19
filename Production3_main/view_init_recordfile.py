#===== Standard Library
#===== 3rd party
import pickle
import os
import pathlib
#===== Reader
from recorder import Recorder
#=====
record_dict = {'main_hwm':0}
path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'record.txt')
with open(path, 'wb') as fp:
    pickle.dump(record_dict, fp)