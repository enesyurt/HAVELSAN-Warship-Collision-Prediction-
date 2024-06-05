import numpy as np
import time

class Ship:
    def __init__(self, ship_id, position, velocity, safezone_radius=40):
        self.ship_id = ship_id
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.safezone_radius = safezone_radius
        self.last_update = None

    def update(self, position, velocity, update_time):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.last_update = update_time

def distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def predict_position(ship, future_time):
    time_diff = future_time - ship.last_update
    return ship.position + ship.velocity * time_diff

def is_collision(ship1, ship2):
    return distance(ship1.position, ship2.position) < 2 * ship1.safezone_radius

def calculate_threat_level(ship1, ship2):
    dist = distance(ship1.position, ship2.position)
    if dist < 2 * ship1.safezone_radius:
        return 'High'
    elif dist < 4 * ship1.safezone_radius:
        return 'Medium'
    else:
        return 'Low'



ships = [
    Ship("0001", [0, 0, 0], [10, 10, 0]),
    Ship("0002", [100, 100, 0], [-10, -10, 0])
]

# Set initial last update time
for ship in ships:
    ship.last_update = time.time()
