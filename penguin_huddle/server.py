from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import *
from agent import *
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    if type(agent) is Penguin:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "r": 0.5}
        if agent.kill is False:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 1
        else:
            portrayal["Color"] = "red"
            portrayal["r"] = "0.25"
            portrayal["Layer"] = 1
        return portrayal


die_slider = UserSettableParameter('slider', "Temperature at which penguins die", 20, 0, 40, 1)
loss_rate_slider = UserSettableParameter('slider', "Heat Loss rate to ground", 0.1, 0, 1.0, 0.1)
n_slider = UserSettableParameter('slider', "Number of Penguins", 20, 1, 200, 1)

# lets show the average heat of the penguins
chart = ChartModule([{"Label": "Average Heat of Penguins",
                      "Color": "Black"}],
                    data_collector_name='data_collector')

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(Arctic,
                       [grid, chart],
                       "Arctic Landscape",
                       {"N": n_slider,
                        "width": 20,
                        "height": 20,
                        "temperature": 0,
                        "ground_loss_rate": loss_rate_slider,
                        "die_temperature": die_slider}
                       )

