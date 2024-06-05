import numpy as np
import matplotlib.pyplot as plt


class Ship:
    def __init__(self, id, position, velocity, last_update_time, safezone_radius=100):
        self.id = id
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.last_update_time =  last_update_time
        self.safezone_radius = safezone_radius

    def update(self, position, velocity, timestamp):
        self.position = position
        self.velocity = velocity
        self.last_update = timestamp

    def is_colliding(self, other_ship):
        selfzone_radius = self.safezone_radius + other_ship.safezone_radius
        distance = np.linalg.norm(self.position - other_ship.position) 
        #linalg --> Calculates the Euclidian norm of two velocity vectors 
        #which means straight line difference between two vectors.

        return distance <= selfzone_radius

