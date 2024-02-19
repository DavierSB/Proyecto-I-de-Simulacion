import random
import sim
class Distribution_Example:
    def __init__(self) -> None:
        pass
    def random(self):
        return random.random()

simulation = sim.Serial_Servers_Sim(Distribution_Example(), [Distribution_Example()])
simulation.simulate(10)

for person in simulation.persons:
    print(str(person.id) + " " + str(person.time_waiting))
