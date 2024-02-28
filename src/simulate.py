import streamlit
from distribution import Distribution
from simulator import Serial_Servers_Sim
from random_vars import get_n_random_distributions

servidores = get_n_random_distributions(100)
sss = Serial_Servers_Sim(Distribution(), servidores)
sss.simulate(1000)
sss.post_processing()
print(sss.post_processing_data['max_client_waiting_time'])
sss.show()

