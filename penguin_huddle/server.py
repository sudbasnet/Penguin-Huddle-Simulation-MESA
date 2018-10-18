from mesa.visualization.modules import CanvasHexGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import *
from agent import *
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Penguin:
        portrayal["Shape"] = "images/penguin.png"
        portrayal["scale"] = 1.25
        portrayal["Layer"] = 1

        # if agent.kill is False:
        #     portrayal["Color"] = "grey"
        #     portrayal["Layer"] = 1
        # else:
        #     portrayal["Color"] = "red"
        #     portrayal["r"] = "0.25"
        #     portrayal["Layer"] = 1
        return portrayal


die_slider = UserSettableParameter('slider', "Temperature at which penguins die", 5, 0, 40, 1)
loss_rate_slider = UserSettableParameter('slider', "Heat Loss rate to ground", 0.01, 0, 0.5, 0.01)
n_slider = UserSettableParameter('slider', "Number of Penguins", 25, 1, 200, 1)

# lets show the average heat of the penguins
chart = ChartModule([{"Label": "Average Heat of Penguins",
                      "Color": "Black"}],
                    data_collector_name='data_collector')

grid = CanvasHexGrid(agent_portrayal, 25, 25, 500, 500)
server = ModularServer(Arctic,
                       [grid, chart],
                       "Arctic Landscape",
                       {"N": n_slider,
                        "width": 25,
                        "height": 25,
                        "temperature": 0,
                        "ground_loss_rate": loss_rate_slider,
                        "die_temperature": die_slider}
                       )

