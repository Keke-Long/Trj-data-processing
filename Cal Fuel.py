# 确定5min的开始时间，结束时间戳，每个交叉口node要包含的车道集，
# 每个5min，遍历时间，每个时间，所有满足车道集需求的时刻就加进来，
import pandas as pd
import datetime
import math
import numpy as np


df = pd.read_csv("/media/ubuntu/ANL/Data1_lane_xy_va.csv")

i = df[(df['edge'] == 'node') & (df['lane'] == 1)].index
df.loc[i,'edge'] = 'node1'
i = df[(df['edge'] == 'node') & (df['lane'] == 2)].index
df.loc[i,'edge'] = 'node2'
i = df[(df['edge'] == 'node') & (df['lane'] == 3)].index
df.loc[i,'edge'] = 'node3'

import numpy as np
def Cal_fuel_VTMicro(v,a):
    PE = np.matrix([[-8.27978, 0.36696, -0.04112, 0.00139],
                    [0.06229, -0.02143, 0.00245, 3.71 * 10 ** (-6)],
                    [-0.00124, 0.000518, 6.77 * 10 ** (-6), -7.4 * 10 ** (-6)],
                    [7.72 * 10 ** (-6), -2.3 * 10 ** (-6), -5 * 10 ** (-7), 1.05 * 10 ** (-7)]])

    NE = np.matrix([[-8.27978, -0.27907, -0.05888, -0.00477],
                    [0.06496, 0.03282, 0.00705, 0.000434],
                    [-0.00131, -0.00066, -0.00013, -7.6 * 10 ** (-6)],
                    [8.23 * 10 ** (-6), 3.54 * 10 ** (-6), 6.48 * 10 ** (-7), 3.98 * 10 ** (-8)]])

    PE2 = np.matrix([[-0.679439, 0.135273, 0.015946, -0.001189],
                     [0.029665, 0.004808, -0.000020635, 5.5409285 * 10 ** (-8)],
                     [-0.000276, 0.000083329, 0.000000937, -2.479644 * 10 ** (-8)],
                     [0.000001487, -0.000061321, 0.000000304, -4.467234 * 10 ** (-9)]])
    a = a * 3.6 # m/s to km/h
    v = v * 3.6
    if a >= 0:
        fuel = np.power(math.e, np.matrix([1, v, np.power(v,2), np.power(v,3)]) * PE * np.transpose(np.matrix([1, a, np.power(a,2), np.power(a,3)])) )
    else:
        fuel = np.power(math.e, np.matrix([1, v, np.power(v,2), np.power(v,3)]) * NE * np.transpose(np.matrix([1, a, np.power(a,2), np.power(a,3)])) )
    #fuel2 = math.pow(math.e, np.matrix([1, v, pow(v,2), pow(v,3)]) * PE2 * np.transpose(np.matrix([1, a, pow(a,2), pow(a,3)])))
    #print(fuel[:,])
    return fuel[0,0]


start_t = '20221111160315.1'
start_t_sec = 0.1 + (datetime.datetime.strptime('20221111160315', "%Y%m%d%H%M%S") - datetime.datetime(2022, 11, 11, 16)).total_seconds()

node_list = {'fuel_node1': ['node1', '0_1', '5_1', '2_1'],
             'fuel_node2': ['node2', '1_2', '9_2', '3_2'],
             'fuel_node3': ['node3', '2_3', '10_3', '4_3', '7_3']}

time_step = 0.1

energy_record = pd.DataFrame(columns=['fuel_node1', 'fuel_node2', 'fuel_node3'])
for node in node_list.keys():
    for i in range(5): # 算2个5min
        t1 = start_t_sec + 5*60*i
        t2 = start_t_sec + 5*60*(i+1)
        L = df[(df['t_sec'] >= t1) & (df['t_sec'] < t2) & (df['edge'].isin(node_list[node]))].index
        fuel = 0
        veh_list = []
        trip_length = 0
        for j in L:
            v = max(0, max(round(df.loc[j, 'v'], 3), 15 ))
            a = max(-2, max(round(df.loc[j, 'a'], 3), 2 ))
            if not np.isnan(a):
                fuel += Cal_fuel_VTMicro(v, a) * time_step
                veh_list.append(df.loc[j, 'id'])
                trip_length += v * time_step
        num_veh = len(set(veh_list))
        fuel = fuel/(trip_length/100000) #百公里油耗
        print(i, fuel)
        energy_record.loc[i, node] = fuel

print(energy_record)


#   fuel_node1 fuel_node2 fuel_node3
# 0  41.915435  40.556843        inf
# 1  63.991563  63.942819  63.832079
# 2  58.177332  58.972872  60.074755
# 3  34.612112  34.470403  35.599354
# 4  34.414683  34.608833        inf
