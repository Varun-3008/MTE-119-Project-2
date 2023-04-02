import numpy as np
import time
import numba
import concurrent.futures as conc
from tqdm import tqdm


W1 = 4 * 9.81
W2 = 2 * 9.81
W3 = 1 * 9.81
WL = 5 * 9.81

            
@numba.njit(nogil=True)
def check_lengths(l1, l2, l3):
    
    positions = np.array([
        [0.75, 0.1, np.deg2rad(-60), 1000000, 0, 0, 0],
        [0.5, 0.5, np.deg2rad(0), 1000000, 0, 0, 0],
        [0.2, 0.6, np.deg2rad(45), 1000000, 0, 0, 0]
    ])


    for pos in positions:
        x,y,q3 = pos[0], pos[1], pos[2]
        x2,y2 = x - l3 * np.cos(q3), y - l3 * np.sin(q3)
        if y2 >= 0:
            l12 = np.sqrt(x2**2 + y2**2)
            angle = np.tan(y2/x2)
            a1 = np.arccos((l1**2 + l12**2 - l2**2)/(2*l1*l12))
            q1 = [angle + a1, angle - a1]
            x1, y1 = [l1 * np.cos(q1[0]), l1 * np.cos(q1[1])], [l1 * np.sin(q1[0]), l1 * np.sin(q1[1])]
            q2 = [np.tan((y2-y1[0])/(x2-x1[0])), np.tan((y2-y1[1])/(x2-x1[1]))]
            
            for i in range(0,2):
                T = (l1 / 2) * W1 * np.cos(q1[i]) + W2 * (l1*np.cos(q1[i]) + l2/2 * np.cos(q2[i])) + W3 * (l1*np.cos(q1[i]) + l2 * np.cos(q2[i]) + l3/2 * np.cos(q3)) + WL * x
                if T < pos[3] and y1[i] >= 0: 
                    pos[3] = T
                    pos[4] = q1[i]
                    pos[5] = q2[i]
                    pos[-1] = y1[i]
    T_Total = np.sqrt(positions[0][3]**2 + positions[1][3]**2 + positions[2][3]**2)
    T1, T2, T3 = positions[0][3], positions[1][3], positions[2][3]
    pos1a1, pos2a1, pos3a1 = positions[0][4], positions[1][4], positions[2][4]
    pos1a2, pos2a2, pos3a2 = positions[0][5], positions[1][5], positions[2][5]
    pos1a3, pos2a3, pos3a3 = positions[0][2], positions[1][2], positions[2][2]   
    return[l1, l2, l3, T_Total, T1, T2, T3, pos1a1, pos1a2, pos1a3, pos2a1, pos2a2, pos2a3, pos3a1, pos3a2, pos3a3, positions[0][-1], positions[1][-1], positions[2][-1]]
            


if __name__ == "__main__":
    startTime = time.perf_counter()
    #data = pd.DataFrame()
    min_res = [0,0,0,1000000,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with conc.ThreadPoolExecutor() as executor:
        futures = []
        for l1 in np.linspace(0.005, 5, num=100):#reduce num for less brute force at first
            for l2 in np.linspace(0.005, 5, num=100):
                for l3 in np.linspace(0.005, 0.84852813742, num=100): #0.0848... is max length of l3
                    futures.append(executor.submit(check_lengths, l1, l2, l3))

        for future in tqdm(conc.as_completed(futures)): #using tqdm to track progress
            if future.result() is not None:
                if future.result()[3] < min_res[3]:
                    min_res = future.result()
                #data = pd.concat([data, pd.DataFrame(future.result()).T], axis=0, ignore_index=True) #added in pd.DataFrame(future.result()) because was throwing error trying to concat float w/ dataframe
   # data = data.set_axis(["L1", "L2", "L3", "T", "T1", "T2", "T3", "pos1a1", "pos1a2", "pos1a3", "pos2a1", "pos2a2", "pos2a3", "pos3a1", "pos3a2", "pos3a3"], axis=1, inplace=False)
    #data.to_csv("data.csv")
    print (min_res)