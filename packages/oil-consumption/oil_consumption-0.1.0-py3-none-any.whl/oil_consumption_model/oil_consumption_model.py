



import numpy as np
from scipy.interpolate import UnivariateSpline
import numpy as np
from scipy.interpolate import UnivariateSpline
def oil_consumption_physical_model(speed, wind_speed, swh):
    """读取数据"""
    v = speed
    v_a = wind_speed
    h_a = swh
    U = v * 1.852 / 3.6  # m/s

    return Fuel_consum_ten_minutes