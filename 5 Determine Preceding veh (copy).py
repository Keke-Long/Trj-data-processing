import pandas as pd
import numpy as np
from tqdm import tqdm

df = pd.read_csv("/media/ubuntu/ANL/Data1_lane_xy_va.csv")
df['PreVeh_id'] = np.nan
df['PreVeh_v'] = np.nan
df['delta_d'] = np.nan #距离差

# 写一个所有edge (一个edge内lane的方向一样) 应该用什么排序的方案，包括x/y，升序降序
sort_info = {}
sort_info['1_0'] = ['x_pix', True]
sort_info['2_1'] = ['x_pix', True]
sort_info['3_2'] = ['x_pix', True]
sort_info['4_3'] = ['x_pix', True]

sort_info['0_1'] = ['x_pix', False]
sort_info['1_2'] = ['x_pix', False]
sort_info['2_3'] = ['x_pix', False]
sort_info['3_4'] = ['x_pix', False]

sort_info['9_2'] = ['y_pix', True]
sort_info['2_6'] = ['y_pix', True]
sort_info['10_3'] = ['y_pix', True]
sort_info['3_7'] = ['y_pix', True]

sort_info['5_1'] = ['y_pix', False]
sort_info['1_8'] = ['y_pix', False]
sort_info['7_3'] = ['y_pix', False]
sort_info['3_10'] = ['y_pix', False]

net = np.load('net.npy', allow_pickle=True).item()

edge_list = list(net.keys())
edge_list.remove('node1')
edge_list.remove('node2')
edge_list.remove('node3')

def cal_distance(x1,x2,y1,y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Iterate through the times
for t in tqdm(df['t_sec'].unique()):
    df_t = df[df['t_sec']==t]
    # Group the data frame by edge and lane
    grouped = df_t.groupby(['edge', 'lane'])
    # Iterate through the groups
    for name, group in grouped:
        edge, lane = name
        group = group.sort_values(sort_info[edge][0], ascending=sort_info[edge][1])
        c = 0
        ids = group['id'].values
        vs = group['v'].values
        x = group['x_utm'].values
        y = group['y_utm'].values
        delta_d = np.diff(np.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2))
        for i in range(1, len(group)):
            df.iloc[group.index[i], df.columns.get_loc('PreVeh_id')] = ids[c]
            df.iloc[group.index[i], df.columns.get_loc('PreVeh_v')] = vs[c]
            df.iloc[group.index[i], df.columns.get_loc('delta_d')] = delta_d[i-1]
            c = i

df.to_csv(path_or_buf="/media/ubuntu/ANL/Data1_forCalibration.csv", index=False)
