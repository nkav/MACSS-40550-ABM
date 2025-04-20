from mesa import Agent

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type, min_desired_share_alike, max_desired_share_alike):
        super().__init__(model)
        ## Set agent type
        self.type = agent_type
        self.desired_share_alike = self.random.uniform(min_desired_share_alike, max_desired_share_alike)
    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(pos = self.pos, moore=True, radius=self.model.radius  )
        ## Count neighbors of same type as self
        similar_neighbors = len([n for n in neighbors if n.type == self.type])
        # live_neighbors = sum(neighbor.state for neighbor in self.model.grid.iter_neighbors((self.x, self.y), True))
        ## If an agent has any neighbors (to avoid division by zero), calculate share of neighbors of same type
        if len(neighbors) > 0:
            share_alike = similar_neighbors / len(neighbors)
        else:
            share_alike = 0
        ## If unhappy with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if share_alike < self.desired_share_alike:
            self.model.grid.move_to_empty(self)
        else: 
            self.model.happy += 1
            ## Mimicry effect - 20% chance of adjusting desired_share_alike towards average desired_share_alike of same-type neighbors
            if len([n for n in neighbors if n.type == self.type]) > 0:
                ## Calculate average desired_share_alike of same-type neighbors
                avg_desired_share_alike = sum(n.desired_share_alike for n in neighbors if n.type == self.type) / len([n for n in neighbors if n.type == self.type])
                if self.random.random() < 0.2:
                    if avg_desired_share_alike > self.desired_share_alike:
                        self.desired_share_alike += self.model.mimicry_effect
                    elif avg_desired_share_alike < self.desired_share_alike:
                        self.desired_share_alike -= self.model.mimicry_effect
                    ## Ensure desired_share_alike stays within bounds [0, 1]
                    self.desired_share_alike = max(0, min(1, self.desired_share_alike))
            ## Depolarization effect - 20% chance of moderating desired_share_alike if any neighbor is of a different type
            if any(n.type != self.type for n in neighbors):
                if self.random.random() < 0.2:
                    self.desired_share_alike -= self.model.depolarization_effect
                    self.desired_share_alike = max(0, self.desired_share_alike)  # Ensure bounds

