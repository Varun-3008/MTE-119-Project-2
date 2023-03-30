import numpy as np
from scipy.optimize import minimize
import numba
import random as rd

#@numba.njit(nogil = True, parallel=True)
def forward_kinematics(l1, l2, l3, q1, q2, q3):
    x = l1 * np.cos(q1) + l2 * np.cos(q2) + l3 * np.cos(q3)
    y = l1 * np.sin(q1) + l2 * np.sin(q2) + l3 * np.sin(q3)
    return x, y

#@numba.njit(nogil = True, parallel=True)
def torques(x, l1, l2, l3, q1, q2, q3, a1, a2, a3, WL):
    W1 = a1 * l1
    W2 = a2 * l2
    W3 = a3 * l3

    return (l1 / 2) * W1 * np.cos(q1) +  W2 * (l1*np.cos(q1) + l2/2 * np.cos(q2)) + W3 * (l1*np.cos(q1) + l2 * np.cos(q2) + l3/2 * np.cos(q3)) + WL * x

#@numba.njit(nogil = True, parallel=True)
def objective_function(l, *args):
    l1, l2, l3 = l
    positions, density = args

    total_T = 0
    for pos in positions:
        x, y, q3 = pos
        q1, q2 = inverse_kinematics(l1, l2, l3, x, y, q3)
        total_T += torques(x, WL, l1, l2, l3, q1, q2, q3, *density)**2

    return total_T

#@numba.njit(nogil = True, parallel=True)
def inverse_kinematics(l1, l2, l3, x, y, q3):
    # Calculate q1 and q2 using inverse kinematics

    # Calculate the position of the second joint (intermediate point)
    x_int = x - l3 * np.cos(q3)
    y_int = y - l3 * np.sin(q3)

    # Distance between the base and the second joint (intermediate point)
    d = np.sqrt(x_int ** 2 + y_int ** 2)

    # Calculate q2 using the cosine law
    cos_q2 = ()
    cos_q2 = (d ** 2 + l2 ** 2 - l1 ** 2) / (2 * d * l2)
    q2 = np.pi- np.arccos(cos_q2)

    # Calculate q1 using the tangent law
    numerator = l2 * np.sin(q2)
    denominator = l1 + l2 * cos_q2
    q1 = np.arctan2(y_int, x_int) - np.arctan2(numerator, denominator)

    return q1, q2

# Given positions and densities
positions = [
    (0.75, 0.1, np.deg2rad(-60)),
    (0.5, 0.5, np.deg2rad(0)),
    (0.2, 0.6, np.deg2rad(45))
]

density = (4*9.81, 2*9.81, 1*9.81)  # a1, a2, a3
WL = 5 * 9.81  # Rated loading in Newtons

# Initial guess for link lengths
min = 1000000
min_res = None
for i in range(10000), :
    l0 = [rd.random(), rd.random(), rd.random()] # random.randn

    # Constraints
    constraints = [
        {"type": "ineq", "fun": lambda l: l[0] + l[1] + l[2] - 1},  # l1 + l2 + l3 >= 1
        {"type": "ineq", "fun": lambda l: l[0]},  # l1 >= 0
        {"type": "ineq", "fun": lambda l: l[1]},  # l2 >= 0
        {"type": "ineq", "fun": lambda l: l[2]},  # l3 >= 0
        {"type": "ineq", "fun": lambda l: 0.84852814 - l[2]} # l[3] <= 0.84852814
    ]

    # Perform optimization
    result = minimize(objective_function, l0, args=(positions, density), constraints=constraints)
    if abs(round(result.fun,2)) < min:
    # Print results
        print("Optimal link lengths:", result.x)
        print("Minimum T value:", round(result.fun, 2))
        min = round(result.fun,2)
