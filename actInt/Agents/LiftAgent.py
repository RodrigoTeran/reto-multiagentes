import agentpy as ap
from random import choice


class LiftAgent(ap.Agent):
    def setup(self):
        pass

    def step(self):
        a = [-1, 1]
        dx = choice(a)
        dy = choice(a)

        self.model.warehouse.move_by(self, (dx, dy))
