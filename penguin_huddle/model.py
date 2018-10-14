from agent import *
from mesa import Model
from mesa.time import RandomActivation
import random
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class Arctic(Model):
    def __init__(self, N, width, height, temperature, ground_loss_rate, die_temperature):
        self.num_agents = N

        # false means he grid is not toroidal
        self.grid = MultiGrid(width, height, False)

        self.schedule = RandomActivation(self)
        self.temperature = temperature
        self.running = True

        self.ground_loss_rate = ground_loss_rate
        self.die_temperature = die_temperature

        # Create the GridCell agents for each cell
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                c = GridCell(unique_id=(x, y), model=self, heat=self.temperature)
                self.schedule.add(c)
                self.grid.place_agent(c, (x, y))

        # Place the penguins in random grid locations
        # Penguins should not overlap
        # Create a list of locations where the penguins are already assigned
        occupied = []
        for i in range(self.num_agents):
            p = Penguin(unique_id=i, model=self, heat=40.0, loss_rate=0.0, open_sides=4)
            self.schedule.add(p)
            if len(occupied) >= (self.grid.width * self.grid.height):
                break
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            while (x, y) in occupied:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
            occupied.append((x,y))
            self.grid.place_agent(p, (x, y))
            grid_cellmate = self.grid.get_cell_list_contents((x,y))
            for j in grid_cellmate:
                if type(j) is GridCell:
                    j.occupancy()

        self.data_collector = DataCollector(
            model_reporters={"Average Heat of Penguins": average_heat}
        )

    def remove_ghosts(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                for agent in self.grid.get_cell_list_contents([(x, y)]):
                    if type(agent) is Penguin and agent.kill:
                        self.grid.remove_agent(agent)

    def kill_penguin(self, agent):
        self.grid.remove_agent(agent)

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()
        self.remove_ghosts()


def average_heat(model):
    agent_heats = []
    for agent in model.schedule.agents:
        if type(agent) is Penguin:
            agent_heats.append(agent.heat)
    return round(sum(agent_heats)/len(agent_heats), 2)
