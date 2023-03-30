import pandas as pd
import numpy as np
import time
import numba
import concurrent.futures as conc
from tqdm import tqdm
from math import pi

W1 = 4 * 9.81
W2 = 2 * 9.81
W3 = 1 * 9.81
WL = 5 * 9.81

            
@numba.njit(nogil=True)
def check_lengths(l1, l2, l3):
    positions = [
        {'x': 0.75, 'y': 0.1, 'min': 1000000, 'q1': 0, 'q2': 0, 'q3': np.deg2rad(-60)},
        {'x': 0.5, 'y': 0.5, 'min': 1000000, 'q1': 0, 'q2': 0, 'q3': np.deg2rad(0)},
        {'x': 0.2, 'y': 0.6,  'min': 1000000, 'q1': 0, 'q2': 0, 'q3': np.deg2rad(45)}
    ]
    for q1 in range(0,180):
        q1 = np.deg2rad(q1)
        if l1*np.sin(q1) >= l2:
            a,b = 0,360
        else:
            a,b = np.ceil(180-np.arcsin(l1*np.sin(q1)/l2)),np.ceil(np.arcsin(l1*np.sin(q1)/l2)) #setting range of possible q2 so doesn't go below x-axis
        for q2 in range(a,b):
            q2 = np.deg2rad(q2)
            for pos in positions:
                q3 = pos['q3']
                x = l1 * np.cos(q1) + l2 * np.cos(q2) + l3 * np.cos(q3)
                y = l1 * np.sin(q1) + l2 * np.sin(q2) + l3 * np.sin(q3)

                if np.sqrt((x - pos['x'])**2 + (y - pos['y'])**2) < 0.005: #threshold of 0.005
                    T = (l1 / 2) * W1 * np.cos(q1) + W2 * (l1*np.cos(q1) + l2/2 * np.cos(q2)) + W3 * (l1*np.cos(q1) + l2 * np.cos(q2) + l3/2 * np.cos(q3)) + WL * x
                    
                    if T < pos['min']: 
                        pos['min'] = T
                        pos['q1'] = q1
                        pos['q2'] = q2

    T_Total = np.sqrt(positions[0]['min']**2 + positions[1]['min']**2 + positions[2]['min']**2)
    T1, T2, T3 = positions[0]['min'], positions[1]['min'], positions[2]['min']
    pos1a1, pos2a1, pos3a1 = np.rad2deg(positions[0]['q1']), np.rad2deg(positions[1]['q1']), np.rad2deg(positions[2]['q1'])
    pos1a2, pos2a2, pos3a2 = np.rad2deg(positions[0]['q2']), np.rad2deg(positions[1]['q2']), np.rad2deg(positions[2]['q2'])
    pos1a3, pos2a3, pos3a3 = np.rad2deg(positions[0]['q3']), np.rad2deg(positions[1]['q3']), np.rad2deg(positions[2]['q3'])   
    return[l1, l2, l3, T_Total, T1, T2, T3, pos1a1, pos1a2, pos1a3, pos2a1, pos2a2, pos2a3, pos3a1, pos3a2, pos3a3]

if __name__ == "__main__":
    startTime = time.perf_counter()
    data = pd.DataFrame()
    with conc.ThreadPoolExecutor() as executor:
        futures = []
        for l1 in np.linspace(0.005, 5, num=100):#reduce num for less brute force at first
            for l2 in np.linspace(0.005, 5, num=100):
                for l3 in np.linspace(0.005, 0.84852813742, num=25): #0.0848... is max length of l3
                    futures.append(executor.submit(check_lengths, l1, l2, l3))

        for future in tqdm(conc.as_completed(futures)): #using tqdm to track progress
            if future.result() is not None:
                data = pd.concat([data, pd.DataFrame(future.result()).T], axis=0, ignore_index=True) #added in pd.DataFrame(future.result()) because was throwing error trying to concat float w/ dataframe
    data = data.set_axis(["L1", "L2", "L3", "T", "T1", "T2", "T3", "pos1a1", "pos1a2", "pos1a3", "pos2a1", "pos2a2", "pos2a3", "pos3a1", "pos3a2", "pos3a3"], axis=1, inplace=False)
    data.to_csv("c:/Users/varun/OneDrive/Desktop/MTE 119/Project 2/data.csv")