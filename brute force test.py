import numpy as np

# define the objective function
# define gripper load and minimum distance
WL = 5
D = 1
# define density values
a1 = 4
a2 = 2
a3 = 1

# define bounds for link lengths
l_min = 0.1
l_max = 2

# initialize best value of T and corresponding link lengths
T_best = np.inf
l1_best, l2_best, l3_best = None, None, None

# loop over all possible combinations of link lengths
for l1 in np.linspace(l_min, l_max, 50):
    for l2 in np.linspace(l_min, l_max, 50):
        for l3 in np.linspace(l_min, l_max, 50):
            
            # calculate torques for each position
            x1, y1, q3_1 = 0.75, 0.1, -60
            x2, y2, q3_2 = 0.5, 0.5, 0
            x3, y3, q3_3 = 0.2, 0.6, 45
            T1 = a3*l3*(np.cos(np.radians(q3_1)) + np.sin(np.radians(q3_1))*(l2/l3 + l1/l3)) + a2*l2*(np.sin(np.radians(q3_1))*(l1/l3) - np.cos(np.radians(q3_1))) + a1*l1*np.sin(np.radians(q3_1))
            T2 = a3*l3*(np.cos(np.radians(q3_2)) + np.sin(np.radians(q3_2))*(l2/l3 + l1/l3)) + a2*l2*(np.sin(np.radians(q3_2))*(l1/l3) - np.cos(np.radians(q3_2))) + a1*l1*np.sin(np.radians(q3_2))
            T3 = a3*l3*(np.cos(np.radians(q3_3)) + np.sin(np.radians(q3_3))*(l2/l3 + l1/l3)) + a2*l2*(np.sin(np.radians(q3_3))*(l1/l3) - np.cos(np.radians(q3_3))) + a1*l1*np.sin(np.radians(q3_3))
            
            # check if the constraints are satisfied
            if (l1 + l2 + l3) <= D and a3*l3*9.81 <= WL and y1 >= 0 and y2 >= 0 and y3 >= 0:
                
                # calculate total torque parameter T
                T = np.sqrt(T1**2 + T2**2 + T3**2)
                
                # update best value of T and corresponding link lengths
                if T < T_best:
                    T_best = T
                    l1_best, l2_best, l3_best = l1, l2, l3

# print results
print("Link lengths: ", l1_best, l2_best, l3_best)
print("Minimum torque parameter T: ", T_best)
