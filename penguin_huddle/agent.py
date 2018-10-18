from mesa import Agent
from model import *
from math import sqrt, pow, inf


class Penguin(Agent):
    def __init__(self, unique_id, model, heat, loss_rate):
        super().__init__(unique_id, model)
        self.heat = heat
        self.loss_rate = loss_rate
        # self.open_sides = open_sides
        self.kill = False
        self.waddle_id = 0
        self.open_sides = []
        self.open_positions = []
        self.last_position = None

    def lose(self):
        losing = self.heat * ((self.loss_rate * self.open_sides) + self.model.ground_loss_rate)
        self.heat = self.heat - losing
        # cell_contains = self.model.grid.get_cell_list_contents([self.pos])
        # for gridcell in cell_contains:
        #     if type(gridcell) is GridCell:
        #         gridcell.heat += (0.9 * losing)  # 90 % of what the penguin looses is given to the grid

    def live_or_die(self):
        if self.heat <= self.model.die_temperature:
            self.kill = True

    def set_waddle_id(self, w):
        self.waddle_id = w

    def check_openness(self):
        # Check if the penguin is open in four directions: East (E), North (N), West (W), South (S)
        neighborhood = self.model.grid.get_neighborhood(self.pos)
        self.open_sides = 0
        self.open_positions = []
        for n in neighborhood:
            if self.model.grid.is_cell_empty(n):
                self.open_positions.append(n)
                self.open_sides += 1

    # looks around and finds the grid that the penguin wants to go to
    def find_lighthouse(self):
        self.check_openness()
        walk_length = inf
        lighthouse = self.pos
        neighbors = self.model.grid.get_neighbors(self.pos)
        for x in range(self.model.grid.width):
            for y in range(self.model.grid.height):
                for hot_penguin in self.model.grid.get_cell_list_contents([(x, y)]):
                    if (x, y) != self.pos and hot_penguin.heat >= self.heat and hot_penguin not in neighbors:
                        dist = euclidean(self.pos, hot_penguin.pos)
                        if dist < walk_length:
                            walk_length = dist
                            lighthouse = hot_penguin.pos
        return lighthouse

    def next_pos(self):
        next_pos = self.pos
        lighthouse = self.find_lighthouse()
        self.check_openness()
        if lighthouse == self.pos:
            neighbor_count = len(self.model.grid.get_neighbors(self.pos))
            new_neighbor_count = neighbor_count
            for op in self.open_positions:
                if len(self.model.grid.get_neighbors(op))-1 > new_neighbor_count and op != self.last_position:
                    new_neighbor_count = len(self.model.grid.get_neighbors(op))-1
                    next_pos = op
        else:
            best_distance = inf
            for np in self.open_positions:
                if euclidean(np, lighthouse) < best_distance and np != self.last_position:
                    best_distance = euclidean(np, lighthouse)
                    next_pos = np
        return next_pos

    # def make_waddle(self):
    #     for p in self.model.grid.get_neighbors(self):
    #         if p.waddle_id < self.waddle_id:
    #             self.waddle_id = p.waddle_id

    def step(self):
        if type(self) is Penguin and self.pos is not None:
            new_position = self.next_pos()
            self.last_position = self.pos
            self.model.grid.move_agent(self, new_position)
            # self.make_waddle()
            self.lose()
            self.live_or_die()


# class GridCell(Agent):
#     def __init__(self, unique_id, model, heat, loss_rate):
#         super().__init__(unique_id, model)
#         self.heat = heat
#         self.occupied = False
#         self.loss_rate = loss_rate
#
#     def occupancy(self):
#         cellmates = self.model.grid.get_cell_list_contents([self.pos])
#         if len(cellmates) > 1:
#             self.occupied = True
#         else:
#             self.occupied = False
#
#     def is_occupied(self):
#         return self.occupied
#
#     def lose(self):
#         self.heat = max(self.heat - (self.heat * self.loss_rate), 0)
#
#     def step(self):
#         self.occupancy()
#         self.lose()
#         # if self.occupied:
#         #     print(self.pos, " occupado")


# simply define the euclidean distance between point a and b
def euclidean(a, b):
    return sqrt(pow(a[0]-b[0], 2) + pow(a[1]-b[1], 2))
