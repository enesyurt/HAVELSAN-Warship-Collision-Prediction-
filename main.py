import numpy as np

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

import time
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import threading

class Radar:
    def __init__(self, ships, update_interval=1, prediction_interval=1):
        self.ships = ships
        self.update_interval = update_interval
        self.prediction_interval = prediction_interval
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter([], [], s=100)
        self.safezones = [Circle((0, 0), ship.safezone_radius, edgecolor='r', facecolor='none', linestyle='dotted') for ship in ships]
        for safezone in self.safezones:
            self.ax.add_patch(safezone)
        self.stop_event = threading.Event()
        self.start_time = time.time()

    def update_ship_data(self):
        while not self.stop_event.is_set():
            current_time = time.time()
            for ship in self.ships:
                if ship.last_update is not None:
                    new_position = predict_position(ship, current_time)
                    ship.update(new_position, ship.velocity, current_time)
            time.sleep(self.update_interval)

    def simulate_radar_updates(self):
        while not self.stop_event.is_set():
            current_time = time.time()
            for ship in self.ships:
                if ship.last_update is not None:
                    new_position = predict_position(ship, current_time)
                    ship.update(new_position, ship.velocity, current_time)
            time.sleep(self.update_interval)

    def check_collisions(self):
        current_time = time.time()
        for i, ship1 in enumerate(self.ships):
            for j, ship2 in enumerate(self.ships):
                if i < j and is_collision(ship1, ship2):
                    threat_level = calculate_threat_level(ship1, ship2)
                    collision_time = current_time - self.start_time
                    print(f"Collision detected between {ship1.ship_id} and {ship2.ship_id} at t= {collision_time:.2f} seconds. Threat level: {threat_level}")

    def check_future_collisions(self):
        collision_pairs = []
        for i, ship1 in enumerate(self.ships):
            for j, ship2 in enumerate(self.ships):
                if i < j:
                    future_time = max(ship1.last_update, ship2.last_update) + self.prediction_interval
                    future_position1 = predict_position(ship1, future_time)
                    future_position2 = predict_position(ship2, future_time)
                    if distance(future_position1, future_position2) < 2 * ship1.safezone_radius:
                        collision_pairs.append((ship1.ship_id, ship2.ship_id, future_time))
        for ship1_id, ship2_id, collision_time in collision_pairs:
            ship1 = next(ship for ship in self.ships if ship.ship_id == ship1_id)
            ship2 = next(ship for ship in self.ships if ship.ship_id == ship2_id)
            threat_level = calculate_threat_level(ship1, ship2)
            future_collision_time = collision_time - self.start_time
            print(f"Potential future collision between {ship1_id} and {ship2_id} at t= {future_collision_time:.2f} seconds. Threat level: {threat_level}")

    def update_plot(self, frame):
        positions = np.array([ship.position for ship in self.ships])
        self.scat.set_offsets(positions)
        for ship, safezone in zip(self.ships, self.safezones):
            safezone.center = ship.position
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        return self.scat,

    def simulate(self, duration=10):
        while not self.stop_event.is_set() and time.time() - self.start_time < duration:
            self.check_collisions()
            self.check_future_collisions()
            time.sleep(self.update_interval)
        self.stop_event.set()

    def run(self, duration=10):
        ani = FuncAnimation(self.fig, self.update_plot, interval=1000, cache_frame_data=False)
        update_thread = threading.Thread(target=self.update_ship_data)
        sim_thread = threading.Thread(target=self.simulate, args=(duration,))
        radar_update_thread = threading.Thread(target=self.simulate_radar_updates)
        
        update_thread.start()
        sim_thread.start()
        radar_update_thread.start()
        
        plt.show()
        
        update_thread.join()
        sim_thread.join()
        radar_update_thread.join()

# Initialize ships
ships = [
    Ship("0001", [-50, -50, 0], [0, 10, 0]),
    Ship("0002", [100, 100, 0], [-10, -10, 0])
]

for ship in ships:
    ship.last_update = time.time()


radar = Radar(ships, update_interval=1, prediction_interval=1)

radar.run(duration=15)
