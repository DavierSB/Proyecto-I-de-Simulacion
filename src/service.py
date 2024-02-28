from queue import Queue
class Service:
    def __init__(self, id, service_time_distribution):
        self.id = id
        self.service_time_distribution = service_time_distribution
        self.line = Queue()
        self.available = True
        self.time = 0
        self.time_available = 0
        self.time_working = 0
        self.lines_info = {} #contiene tuplas de la forma (n_of_people_in_line, time)
    
    def update_time(self, time):
        delta = time - self.time
        if self.available:
            self.time_available = self.time_available + delta
        else:
            self.time_working = self.time_working + delta
        if not (self.line.qsize() in self.lines_info):
            self.lines_info[self.line.qsize()] = 0
        self.lines_info[self.line.qsize()] = self.lines_info[self.line.qsize()] + delta
        self.time = time

    def lineup(self, person_id, time):
        self.update_time(time)
        self.line.put(person_id)
    
    def serve(self, person_id, time):
        self.update_time(time)
        self.available = False
        service_time = self.service_time_distribution.random()
        return (self.time + service_time, 'END_SERVICE', person_id, self.id)
    
    def end_service(self, person_id, time):
        self.update_time(time)
        if self.line.qsize() > 0:
            return (time, 'BEGIN_SERVICE', self.line.get(), self.id)
        self.available = True
    
    def post_processate(self, total_sim_time):
        post_processing_info = {}
        post_processing_info['waiting_time'] = self.time_available
        post_processing_info['working_time'] = self.time_working
        sum_of_lines_lengths = 0
        max_lenght = 0
        for key in self.lines_info:
            sum_of_lines_lengths = sum_of_lines_lengths + key
            max_line_length = key
        post_processing_info['max_line_length'] = max_line_length
        post_processing_info['avg_line_length'] = sum_of_lines_lengths/total_sim_time
        return post_processing_info