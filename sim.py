from aux_classes import Service, Person
import heapq
class Serial_Servers_Sim:
    def __init__(self, arrivals_distribution, service_time_distributions):
        self.n_of_servers = len(service_time_distributions)
        self.arrivals_distribution = arrivals_distribution
        self.service_time_distributions = service_time_distributions
        self.services = None
        self.timeline = []
        self.persons = []
    
    def simulate(self, time_to_simulate):
        self.services = [Service(i, self.service_time_distributions[i]) for i in range(self.n_of_servers)]
        self.compute_arrivals_until(time_to_simulate)
        heapq.heapify(self.timeline)
        while len(self.timeline):
            time, operation, person_id, service_id = heapq.heappop(self.timeline)
            match operation:
                case 'ARRIVAL':
                    self.service_solicitude(0, person_id, time)
                case 'FINISHED_SERVICE':
                    self.service_finished(service_id, person_id, time)
                    self.move_service_line(service_id, time)
                    if service_id + 1 < self.n_of_servers:
                        self.service_solicitude(service_id + 1, person_id, time)
    
    def service_solicitude(self, service_id, person_id, time):
        service = self.services[service_id]
        person = self.persons[person_id]
        if service.available:
            new_op = service.serve(person_id, time)
            heapq.heappush(self.timeline, new_op)
            person.be_served(service_id, time)
        else:
            service.lineup(person_id, time)
            person.lineup(service_id, time)
    
    def service_finished(self, service_id, person_id, time):
        service = self.services[service_id]
        person = self.persons[person_id]
        service.finish_service_to(person_id, time)
        person.finish_service_from(service_id, time)
    
    def move_service_line(self, service_id, time):
        service = self.services[service_id]
        person_id = service.move_line(time)
        if person_id:
            new_op = service.serve(person_id, time)
            heapq.heappush(self.timeline, new_op)
            person = self.persons[person_id]
            person.be_served(service_id, time)
    
    def compute_arrivals_until(self, time_to_simulate):
        time = 0
        person_id = 0
        while time < time_to_simulate:
            time = time + self.arrivals_distribution.random()
            self.timeline.append((time, 'ARRIVAL', person_id, 0))
            self.persons.append(Person(person_id, time))
            person_id = person_id + 1