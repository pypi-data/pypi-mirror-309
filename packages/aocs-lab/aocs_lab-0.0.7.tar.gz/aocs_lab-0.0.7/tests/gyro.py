from math import sqrt, asin, sin, cos, pi
import numpy as np
from utils import lib

def calc_local_rot_rate():
    # 上海厂房坐标 31.021018°N 121.393126°E
    omega_north, omega_up = lib.latitude_to_angular_velocity(np.deg2rad(31.021018))

    # 厂房偏转角度
    theta = asin(24/80)
    n = omega_north * cos(theta)
    e = omega_north * sin(theta)

    print(f"当地北向角速度: {np.rad2deg(omega_north):6f} deg/s")
    print(f"当地天向角速度: {np.rad2deg(omega_up):6f} deg/s")
    print(f"厂房北向角速度: {np.rad2deg(n):6f} deg/s")
    print(f"厂房东向角速度: {np.rad2deg(e):6f} deg/s")

if __name__ == "__main__":
    calc_local_rot_rate()
