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

    def __init__(self, width=100, height=100, density=0.65, fireman=0.5):
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
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Wet": lambda m: self.count_type(m, "Wet"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                elif self.random.random() < fireman:
                    new_tree.condition = "Wet"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        
        self.running = True
        self.datacollector.collect(self)
        self.fireman = fireman
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
    
    
def density(model):
    return model.density

def fireman(model):
    print(model.fireman)
    return model.fireman
    
def batchRun():
    """
    run my model in a certain time
    """
    ni = 2
    stepsPerSimulation = 2
    fireM = 0.95
    fixedParams = {
        "height": 100,
        "width": 100,
        "fireman": fireM,
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
            "Bombeiro": fireman,
        },
        agent_reporters={
            "Posição": "pos",
        }
    )
    br.run_all()
    runModelData = br.get_model_vars_dataframe()
    runAgentData = br.get_agent_vars_dataframe()
    file_name_suffix = "fire_model_data" + str(fireM)
    runModelData.to_csv("results/model_data" + file_name_suffix + ".csv")
    runAgentData.to_csv("results/agent_data" + file_name_suffix + ".csv")

batchRun()
    

