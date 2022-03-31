from mesa import Agent


class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", "Burned Out", "Wet"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.soil_condition = "Good"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        # if self.soil_condition == "Acid":
        #     self.condition = "On Fire"
        if self.condition == "About to Fire" and self.soil_condition == "Acid":
            self.condition = "On Fire"
        elif self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"
            self.soil_condition = "Acid"
        elif self.condition == "Humidity Tree":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fire":
                    neighbor.condition = "Humidity Tree"
            self.condition = "Humidity Tree"
            self.soil_condition = "Good"

# class SoilCell(Agent):
#     """
#     A tree cell.

#     Attributes:
#         x, y: Grid coordinates
#         condition: Can be "Fine", "acid"
#         unique_id: (x,y) tuple.

#     unique_id isn't strictly necessary here, but it's good
#     practice to give one to each agent anyway.
#     """

#     def __init__(self, pos, model):
#         """
#         Create a new soil.
#         Args:
#             pos: The soil's coordinates on the grid.
#             model: standard model reference for agent.
#         """
#         super().__init__(pos, model)
#         self.pos = pos
#         self.condition = "Fine"

#     def step(self):
#         """
#         If the soil is on fire, spread it to fine soils nearby.
#         """
#         if self.condition == "On Fire":
#             for neighbor in self.model.grid.neighbor_iter(self.pos):
#                 if neighbor.condition == "Fine":
#                     neighbor.condition = "On Fire"
#             self.condition = "Burned Out"
#         elif self.condition == "Wet":
#             for neighbor in self.model.grid.neighbor_iter(self.pos):
#                 if neighbor.condition == "Fire":
#                     neighbor.condition = "Wet"
#             self.condition = "Wet"
