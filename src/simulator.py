from typing import List, Tuple
from distribution import Distribution
from queue import Queue
import heapq
import streamlit
import matplotlib.pyplot as plt
import numpy
from service import Service
from scipy.stats import gaussian_kde
class Serial_Servers_Sim:
    def __init__(self, arrivals_distribution : Distribution, service_time_distributions : List[Distribution]):
        self.n_of_servers = len(service_time_distributions)
        self.n_of_clients = 1
        self.arrivals_distribution = arrivals_distribution
        self.service_time_distributions = service_time_distributions
        self.timeline = []
        self.services : List[Service] = []
        for i in range(self.n_of_servers):
            self.services.append(Service(i, self.service_time_distributions[i]))
        self.table = []
        self.post_processing_data = {}
    
    def simulate(self, time_to_simulate):
        self.time_simulated = time_to_simulate
        self.get_arrivals(time_to_simulate)
        self.initialize_table_and_lines()
        while len(self.timeline):
            time, operation, person_id, service_id = heapq.heappop(self.timeline)
            #print(str(round(time, 2)) + ' ' + operation + ' ' + str(person_id) + ' ' + str(service_id))
            match operation:
                case 'ARRIVAL':
                    self.table[person_id][service_id][0] = time
                    if self.services[service_id].available:
                        heapq.heappush(self.timeline, (time, 'BEGIN_SERVICE', person_id, service_id))
                    else:
                        self.services[service_id].lineup(person_id, time)
                case 'BEGIN_SERVICE':
                    self.table[person_id][service_id][1] = time
                    end_event = self.services[service_id].serve(person_id, time)
                    heapq.heappush(self.timeline, end_event)
                case 'END_SERVICE':
                    self.table[person_id][service_id][2] = time
                    if service_id + 1 < self.n_of_servers:
                        heapq.heappush(self.timeline, (time, 'ARRIVAL', person_id, service_id + 1))
                    next_event = self.services[service_id].end_service(person_id, time)
                    if next_event:
                        heapq.heappush(self.timeline, next_event)

    def get_arrivals(self, time_to_simulate):
        self.timeline.append((0, 'ARRIVAL', 0, 0)) #la primera persona entra en el segundo 0
        time = 0
        while time < time_to_simulate:
            time = time + self.arrivals_distribution.random()
            if time < time_to_simulate:
                self.timeline.append((time, 'ARRIVAL', self.n_of_clients, 0))
                self.n_of_clients = self.n_of_clients + 1
        heapq.heapify(self.timeline)
    
    def initialize_table_and_lines(self):
        for i in range(self.n_of_clients):
            self.table.append([])
        for i in range(self.n_of_clients):
            for j in range(self.n_of_servers):
                self.table[i].append([0, 0, 0])
    
    def post_processing(self):
        self.get_clients_info()
        self.get_servers_info()
    
    def get_servers_info(self):
        servers_info = []
        max_line_length = (0, 0)
        sum_avg_line_length = 0
        sum_max_line_length = 0
        max_waiting_time = 0
        max_working_time = 0
        sum_waiting_time = 0
        sum_working_time = 0
        for i in range(self.n_of_servers):
            server_info = self.services[i].post_processate(self.time_simulated)
            max_line_length = max(max_line_length, (server_info['max_line_length'], i))
            max_waiting_time = max(max_waiting_time, server_info['waiting_time'])
            max_working_time = max(max_working_time, server_info['working_time'])
            sum_waiting_time = sum_waiting_time + server_info['waiting_time']
            sum_working_time = sum_working_time + server_info['working_time']
            sum_avg_line_length = sum_avg_line_length + server_info['avg_line_length']
            sum_max_line_length = sum_max_line_length + server_info['max_line_length']
            servers_info.append((server_info['waiting_time'], server_info['working_time'], server_info['max_line_length'], server_info['avg_line_length']))
        self.post_processing_data['max_server_waiting_time'] = max_waiting_time
        self.post_processing_data['max_server_working_time'] = max_working_time
        self.post_processing_data['max_line_length'] = max_line_length
        self.post_processing_data['avg_line_length'] = sum_avg_line_length/self.n_of_servers
        self.post_processing_data['avg_max_line_length'] = sum_max_line_length/self.n_of_servers
        self.post_processing_data['avg_server_waiting_time'] = sum_waiting_time/self.n_of_servers
        self.post_processing_data['avg_server_working_time'] = sum_working_time/self.n_of_servers

        self.post_processing_data['servers_waiting_times'], self.post_processing_data['servers_working_times'], self.post_processing_data['servers_max_line_length'], self.post_processing_data['servers_avg_line_length'] = [list(x) for x in zip(*servers_info)]
    
    def get_clients_info(self):
        clients_info = []
        for i in range(self.n_of_clients):
            clients_info.append([0, 0, 0]) #waiting_time, service_time, n_of_lines
            for j in range(self.n_of_servers):
                waiting_time = self.table[i][j][1] - self.table[i][j][0]
                if waiting_time > 0:
                    clients_info[i][0] = clients_info[i][0] + waiting_time
                    clients_info[i][2] = clients_info[i][2] + 1
                clients_info[i][1] = clients_info[i][1] + (self.table[i][j][2] - self.table[i][j][1])
        max_client_waiting_time = 0
        max_client_service_time = 0
        max_client_lines_done = 0
        sum_client_waiting_time = 0
        sum_client_service_time = 0
        sum_client_lines_done = 0
        for i in range(self.n_of_clients):
            max_client_waiting_time = max(max_client_waiting_time, clients_info[i][0])
            max_client_service_time = max(max_client_service_time, clients_info[i][1])
            max_client_lines_done = max(max_client_lines_done, clients_info[i][2])
            sum_client_waiting_time = sum_client_waiting_time + clients_info[i][0]
            sum_client_service_time = sum_client_service_time + clients_info[i][1]
            sum_client_lines_done = sum_client_lines_done + clients_info[i][2]
        self.post_processing_data['max_client_waiting_time'] = max_client_waiting_time
        self.post_processing_data['max_client_service_time'] = max_client_service_time
        self.post_processing_data['max_client_lines_done'] = max_client_lines_done
        self.post_processing_data['avg_client_waiting_time'] = sum_client_waiting_time/self.n_of_clients
        self.post_processing_data['avg_client_service_time'] = sum_client_service_time/self.n_of_clients
        self.post_processing_data['avg_client_lines_done'] = sum_client_lines_done/self.n_of_clients
        self.post_processing_data['clients_waiting_times'], self.post_processing_data['clients_service_time'], self.post_processing_data['clients_lines_done'] = [list(x) for x in zip(*clients_info)]

    def show(self):
        aux_str = "En la simulacion se acepto solo entrada de clientes durante los primeros " + str(self.time_simulated) + " segundos"
        streamlit.write(aux_str)
        aux_str = "Se usaron 100 servidores, tales que la distribucion de tiempo con que brindan servicios fue seleccionada al azar de entre las provistas en random_vars"
        streamlit.write(aux_str)
        aux_str = "Entraron " + str(self.n_of_clients) + " clientes"
        streamlit.write(aux_str)
        aux_str = "El ultimo cliente en dejar el servicio lo hizo a los " + str(round(self.table[self.n_of_clients - 1][self.n_of_servers - 1][2], 2)) + " segundos"
        streamlit.write(aux_str)
        aux_str = "El mayor tiempo de espera en colas de algun cliente fue " + str(round(self.post_processing_data['max_client_waiting_time'], 2)) + " segundos"
        streamlit.write(aux_str)
        aux_str = "El tiempo de espera en colas promedio para los clientes fue " + str(round(self.post_processing_data['avg_client_waiting_time'], 2)) + " segundos"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['clients_waiting_times'])
        ax.set_xlabel('segundos esperando en cola')
        ax.set_ylabel('n_of_clients')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "El mayor tiempo de servicio para algun cliente fue " + str(round(self.post_processing_data['max_client_service_time'], 2)) + " segundos"
        streamlit.write(aux_str)
        aux_str = "El tiempo de servicio promedio para los clientes fue " + str(round(self.post_processing_data['avg_client_service_time'], 2)) + " segundos"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['clients_service_time'])
        ax.set_xlabel('segundos recibiendo servicio')
        ax.set_ylabel('n_of_clients')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "La mayor cantidad de colas hechas por algun cliente fue " + str(round(self.post_processing_data['max_client_lines_done'], 2))
        streamlit.write(aux_str)
        aux_str = "Cada cliente hizo en promedio " + str(round(self.post_processing_data['avg_client_lines_done'], 2)) + " colas"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['clients_lines_done'])
        ax.set_xlabel('n_de_colas_hechas')
        ax.set_ylabel('n_of_clients')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "El maximo tiempo que un servidor estuvo inactivo fue " + str(round(self.post_processing_data["max_server_waiting_time"], 2)) + " segundos"
        streamlit.write(aux_str)
        aux_str = "En promedio, los servidores estuvieron inactivos " + str(round(self.post_processing_data['avg_server_waiting_time'], 2)) + " segundos"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['servers_waiting_times'])
        ax.set_xlabel('segundos inactivo')
        ax.set_ylabel('n_of_servers')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "El maximo tiempo que un servidor estuvo trabajando fue " + str(round(self.post_processing_data["max_server_working_time"], 2)) + " segundos"
        streamlit.write(aux_str)
        aux_str = "En promedio, los servidores estuvieron trabajando " + str(round(self.post_processing_data['avg_server_working_time'], 2)) + " segundos"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['servers_working_times'])
        ax.set_xlabel('segundos activo')
        ax.set_ylabel('n_of_servers')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "La cola mas larga que tuvo cualquier servidor fue de " + str(self.post_processing_data["max_line_length"][0]) + " clientes y ocurrio en el servidor numero " + str(self.post_processing_data["max_line_length"][1] + 1)
        streamlit.write(aux_str)
        aux_str = "La cola mas larga que cada servidor tuvo en promedio fue de " + str(self.post_processing_data['avg_max_line_length']) + " clientes"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['servers_max_line_length'])
        ax.set_xlabel('maximo tamanho de la cola')
        ax.set_ylabel('n_of_servers')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "La cola promedio para los servidores fue de " + str(round(self.post_processing_data["avg_line_length"], 2)) + " clientes"
        streamlit.write(aux_str)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['servers_avg_line_length'])
        ax.set_xlabel('tamanho promedio de la cola')
        ax.set_ylabel('n_of_servers')
        streamlit.pyplot(fig)
        streamlit.markdown('<br><br><br>', unsafe_allow_html=True)
        aux_str = "Pero podemos apreciar que generalmente, con este arreglo de distribuciones seleccionadas de manera aleatoria que tenemos como placeholder, el cuello de botella el sistema aparece en el primer o segundo servidor"
        streamlit.write(aux_str)
        aux_str = "Por ese motivo mostremos como lucen los graficos de tamanho maximo y promedio de cola cuando obviamos a los dos primeros servidores"
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['servers_max_line_length'][2:])
        ax.set_xlabel('maximo tamanho de la cola')
        ax.set_ylabel('n_of_servers')
        streamlit.pyplot(fig)
        fig, ax = plt.subplots()
        ax.hist(self.post_processing_data['servers_avg_line_length'][2:])
        ax.set_xlabel('tamanho promedio de la cola')
        ax.set_ylabel('n_of_servers')
        streamlit.pyplot(fig)