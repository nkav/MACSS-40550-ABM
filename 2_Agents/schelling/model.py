from mesa import Model
from mesa.space import SingleGrid
from agents import SchellingAgent
from mesa.datacollection import DataCollector

class SchellingModel(Model):
    ## Define initiation, requiring all needed parameter inputs
    def __init__(self, width=50, height=50, density=0.7, min_desired_share_alike=0, max_desired_share_alike=1, 
                 group_one_share=0.7, radius=1, seed=None, mimicry_effect=0.01, depolarization_effect=0.01):
        ## Inherit seed trait from parent class
        super().__init__(seed=seed)
        ## Define parameter values for model instance
        self.width = width
        self.height = height
        self.density = density
        self.min_desired_share_alike = min_desired_share_alike
        self.max_desired_share_alike = max_desired_share_alike
        self.group_one_share = group_one_share
        self.radius = radius
        self.mimicry_effect = mimicry_effect
        self.depolarization_effect = depolarization_effect
        ## Create grid
        self.grid = SingleGrid(width, height, torus = True)
        ## Instantiate global happiness tracker
        self.happy = 0
        self.avg_polarization = 0  # Initialize avg_polarization
        ## Define data collector, to collect happy agents and share of agents currently happy
        self.datacollector = DataCollector(
            model_reporters = {
                "happy" : "happy",
                "share_happy" : lambda m : (m.happy / len(m.agents)) * 100
                if len(m.agents) > 0
                else 0,
                "avg_polarization": lambda m: m.avg_polarization
            }
        )
        ## Place agents randomly around the grid, randomly assigning them to agent types.
        for cont, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                if self.random.random() < self.group_one_share:
                    self.grid.place_agent(SchellingAgent(self, 1, self.min_desired_share_alike, self.max_desired_share_alike), pos)
                else:
                    self.grid.place_agent(SchellingAgent(self, 0, self.min_desired_share_alike, self.max_desired_share_alike), pos)
        ## Initialize datacollector
        self.datacollector.collect(self)

    ## Define a step: reset global happiness tracker, agents move in random order, collect data
    def step(self):
        self.happy = 0
        self.agents.shuffle_do("move")
        self.avg_polarization = self.calculate_avg_polarization()  # Update avg_polarization
        self.datacollector.collect(self)
        ## Run model until all agents are happy
        self.running = self.happy < len(self.agents)

    ## Calculate average desired_share_alike levels of all agents on the grid
    def calculate_avg_polarization(self):
        agents = [agent for agent in self.grid.agents]
        if agents:
            return sum(agent.desired_share_alike for agent in agents) / len(agents)
        return 0
