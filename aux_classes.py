import queue
class Service:
    def __init__(self, id, service_time_distribution):
        self.id = id
        self.service_time_distribution = service_time_distribution
        self.line = queue.Queue()
        self.available = True
        self.time = 0
        self.time_available = 0
        self.time_working = 0
        self.clients_served = 0
    
    def update_time(self, time):
        delta = time - self.time
        if self.available:
            self.time_available = self.time_available + delta
        else:
            self.time_working = self.time_working + delta
        self.time = time

    def lineup(self, person_id, time):
        self.update_time(time)
        self.line.put(person_id)
    
    def serve(self, person_id, time):
        self.update_time(time)
        self.available = False
        service_time = self.service_time_distribution.random()
        return (self.time + service_time, 'FINISHED_SERVICE', person_id, self.id)
    
    def finish_service_to(self, person_id, time):
        self.update_time(time)
        self.available = True
        self.clients_served = self.clients_served + 1
    
    def move_line(self, time):
        self.update_time(time)
        if not self.line.empty():
            return self.line.get()
        return None


class Person:
    def __init__(self, id, time):
        self.id = id
        self.time = time
        self.time_waiting = 0
        self.time_being_served = 0
        self.services_visited = 0
        self.waiting = True
    
    def time_update(self, time):
        delta = time - self.time
        if self.waiting:
            self.time_waiting = self.time_waiting + delta
        else:
            self.time_being_served = self.time_being_served + delta
        self.time = time

    def lineup(self, service_id, time):
        self.time_update(time)
        self.waiting = True
    
    def be_served(self, service_id, time):
        self.time_update(time)
        self.waiting = False

    def finish_service_from(self, service_id, time):
        self.time_update(time)
        self.waiting = True