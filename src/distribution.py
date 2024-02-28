import random
class Distribution:
    def __init__(self, distribution = random.random) -> None:
        self.distribution = distribution
    def random(self):
        return self.distribution()