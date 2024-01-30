import agentpy as ap
import matplotlib.pyplot as plt

from LiftAgent import LiftAgent
from BoxAgent import BoxAgent


class LiftModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.lifts, LiftAgent)

        self.warehouse = ap.Grid(self, (self.p.size, self.p.size), track_empty=True)

        self.warehouse.add_agents(self.agents, random=True, empty=True)
        self.curr_step = 0

    def update(self):
        self.curr_step += 1
        self.agents.step()


def run():
    def animation_func(model, ax):
        grid = model.warehouse.apply(lambda x: len([i for i in x]))
        ap.gridplot(grid, cmap="Accent", ax=ax)
        ax.set_title(f"Step: {model.curr_step}")

    parameters = {"lifts": 5, "size": 20, "steps": 100}
    model = LiftModel(parameters)
    fig, ax = plt.subplots()
    anim = ap.animate(model, fig, ax, animation_func)
    anim.save("animation.gif", fps=10)
    print(model.warehouse.grid)
    plt.show()


if __name__ == "__main__":
    run()
