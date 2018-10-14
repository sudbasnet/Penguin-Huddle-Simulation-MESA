from mesa import Agent
from model import *
HEAT_LOSS_GROUND = 0.01
WHEN_DO_PENGUINS_DIE = 5.0


class Penguin(Agent):
    def __init__(self, unique_id, model, heat, loss_rate, open_sides):
        super().__init__(unique_id, model)
        self.heat = heat
        self.loss_rate = loss_rate
        self.open_sides = open_sides
        self.kill = False

    def lose(self):
        global HEAT_LOSS_GROUND
        self.heat = self.heat - (self.heat * ((self.loss_rate * self.open_sides) + self.model.ground_loss_rate))

    def live_or_die(self):
        if self.heat <= self.model.die_temperature:
            self.kill = True

    def step(self):
        self.lose()
        self.live_or_die()
        # print("unique_id and heat level: ", self.unique_id, self.heat)


class GridCell(Agent):
    def __init__(self, unique_id, model, heat):
        super().__init__(unique_id, model)
        self.heat = heat
        self.occupied = False

    def occupancy(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            self.occupied = True
        else:
            self.occupied = False

    def step(self):
        self.occupancy()
        # if self.occupied:
        #     print(self.pos, " occupado")
