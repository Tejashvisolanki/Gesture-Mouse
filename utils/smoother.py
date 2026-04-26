import numpy as np
from filterpy.kalman import KalmanFilter

def create_kalman(r=10, q=0.1):
    kf = KalmanFilter(dim_x=4, dim_z=2)
    kf.F = np.array([[1,0,1,0],
                     [0,1,0,1],
                     [0,0,1,0],
                     [0,0,0,1]], dtype=float)
    kf.H = np.array([[1,0,0,0],
                     [0,1,0,0]], dtype=float)
    kf.R *= r
    kf.P *= 1000
    kf.Q *= q
    kf.x = np.array([[0],[0],[0],[0]], dtype=float)
    return kf

class CursorSmoother:
    def __init__(self, r=10, q=0.1, dead_zone=8):
        self.kf = create_kalman(r, q)
        self.dead_zone = dead_zone
        self.prev_x = 0
        self.prev_y = 0

    def smooth(self, x, y):
        self.kf.predict()
        self.kf.update(np.array([[x], [y]]))
        sx = int(self.kf.x[0].item())
        sy = int(self.kf.x[1].item())

        if abs(sx - self.prev_x) < self.dead_zone and abs(sy - self.prev_y) < self.dead_zone:
            return self.prev_x, self.prev_y

        self.prev_x, self.prev_y = sx, sy
        return sx, sy