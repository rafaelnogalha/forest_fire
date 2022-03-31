from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire

COLORS = {"Fine": "#00AA00","About to Fire": "#00AA00" ,"On Fire": "#880000", "Burned Out": "#000000", "Humidity Tree": "#00AA00"}
COLORS_SOIL = {"Good": "#964B00", "Acid": "#FFFF00"}

def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    portrayal["Color2"] = COLORS_SOIL[tree.soil_condition]
    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

soil_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_SOIL.items()]
)
soil_pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_SOIL.items()]
)

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    # variavel independente de controle de umidade
    "air_humidity": UserSettableParameter("slider", "air humidity", 0.5, 0, 0.95, 0.01),
    # variavel independente de controle do ar
    "wind_force": UserSettableParameter("slider", "wind force", 0.5, 0, 0.25, 0.01),
    # "temperature": UserSettableParameter("slider", "wind force", 0.5, 0, 0.45, 0.01),
}
server = ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart, soil_chart, soil_pie_chart], "Forest Fire", model_params
)
