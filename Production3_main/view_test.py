#===== Standard Library
#===== 3rd party
import pickle
#===== Reader
from forecast import Forecast
from recorder import Recorder
#=====
recorder = Recorder()
print(recorder.read(key='main_hwm'))