from math import sqrt

import numpy as np

G = 6.6743e-11


class Body:
    def __init__(self, position=np.array([0, 0, 0], dtype=float), velocity=np.array([0, 0, 0], dtype=float), mass=0,
                 id=0):
        self.id = id
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.acceleration = np.array([0, 0, 0], dtype=float)
        self.prev_position = position
        self.prev_velocity = velocity
        self.prev_acceleration = np.array([0, 0, 0], dtype=float)
        self.prev_jerk = np.array([0, 0, 0], dtype=float)
        self.jerk = np.array([0, 0, 0], dtype=float)
        self.color = (1.0, 0, 0)

    def constrain(self, value, low, high):
        return min(max(value, low), high)

    '''
    Adds to the acceleration vector the force applied by one body on this body.
    After all other bodies applied force on this body, we can update the position and velocity
    '''

    def compute_force(self, other):
        rij = other.position - self.position
        r = np.linalg.norm(rij)
        # r = self.constrain(r, 1, 10)
        f = (G * other.mass * rij) / (r ** 3)
        self.acceleration = self.acceleration + f
        velocity_diff = other.velocity - self.velocity
        self.jerk += G * other.mass * (velocity_diff / r ** 3 - (3 * np.dot(velocity_diff, rij) * rij) / (r ** 5))

    '''
    Euler integration
    '''

    def euler_integrator(self, dt):
        self.position += self.velocity * dt
        self.velocity += self.acceleration * dt

        self.acceleration = np.array([0, 0, 0])

    '''
    semi-implicit Euler method, also called symplectic Euler, 
    semi-explicit Euler, Euler–Cromer, and Newton–Størmer–Verlet
    '''

    def symplectic_euler_integrator(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        self.acceleration = np.array([0, 0, 0])

    def hermite_integrator(self, dt):
        self.position = self.position + self.velocity * dt + 1 / 2 * self.acceleration * dt ** 2 + 1 / 6 * self.jerk * dt ** 3
        self.velocity = self.velocity + self.acceleration * dt + 1 / 2 * self.jerk * dt ** 2

        # hermite correction step
        self.position += 1 / 2 * (self.prev_velocity + self.velocity) * dt - 1 / 10 * (
                self.acceleration - self.prev_acceleration) * dt ** 2 + 1 / 120 * (
                                 self.prev_jerk + self.jerk) * dt ** 3
        self.velocity += 1 / 2 * (self.prev_acceleration + self.acceleration) * dt - 1 / 12 * (
                self.jerk - self.prev_jerk) * dt ** 2

        self.prev_velocity = self.velocity
        self.prev_acceleration = self.acceleration
        self.prev_jerk = self.jerk

        self.acceleration = np.array([0, 0, 0])

    def verlet_integrator(self, dt):
        velocity = self.position - self.prev_position
        self.prev_position = self.position
        self.position += velocity + self.acceleration * dt ** 2
        self.acceleration = np.array([0, 0, 0])
