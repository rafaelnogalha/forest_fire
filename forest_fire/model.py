from turtle import width
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.batchrunner import BatchRunner

from .agent import TreeCell


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, air_humidity=0.5, wind_force=0.1):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "About to Fire": lambda m: self.count_type(m, "About to Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                # variavel dependente da acidez do solo
                "Acid": lambda m: self.count_soil_type(m, "Acid"),
                "Good": lambda m: self.count_soil_type(m, "Good"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                random = self.random.random()
                if x == 0:
                    new_tree.condition = "On Fire"
                    new_tree.soil_condition = "Acid"
                elif random < air_humidity:
                    new_tree.condition = "Humidity Tree"
                    new_tree.soil_condition = "Good"
                elif random < wind_force:
                    new_tree.condition = "About to Fire"
                    new_tree.soil_condition = "Acid"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        
        self.running = True
        self.datacollector.collect(self)
        self.air_humidity = air_humidity
        self.wind_force = wind_force
        self.density = density

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False
            
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

    @staticmethod
    def count_soil_type(model, soil_condition):
        """
        Helper method to count soil in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.soil_condition == soil_condition:
                count += 1
        return count
    
    
def density(model):
    return model.density

def air_humidity(model):
    return model.air_humidity

def wind_force(model):
    return model.wind_force
    
def batchRun():
    """
    run my model in a certain time
    """
    ni = 2
    stepsPerSimulation = 2
    airH = 0.1
    windF = 0.25
    fixedParams = {
        "height": 100,
        "width": 100,
        "air_humidity": airH,
        "wind_force": windF,
    }
    variableParams = {
        "density": [0.65, 0.75, 0.85, 0.95],
    }
    br = BatchRunner(
        ForestFire, 
        variableParams, 
        fixedParams, 
        iterations=ni, 
        max_steps=stepsPerSimulation, 
        model_reporters={
            "Densidade": density,
            "Umidade do Ar": air_humidity,
            "Intensidade do Vento": wind_force,
        },
        agent_reporters={
            "Posição": "pos",
        }
    )
    br.run_all()
    runModelData = br.get_model_vars_dataframe()
    runAgentData = br.get_agent_vars_dataframe()
    file_name_suffix = "fire_model_data" + str(airH) + "_" + str(windF)
    runModelData.to_csv("results/model_data" + file_name_suffix + ".csv")
    runAgentData.to_csv("results/agent_data" + file_name_suffix + ".csv")

batchRun()
    

