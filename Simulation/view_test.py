#===== Standard Library
#===== 3rd party
#===== Reader
from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper as Helper
from experiment import Experiment
#===== 
experiment = Experiment(acc_type='sub1')
resp = experiment.get_beta('1INCH-PERP')
print(resp)