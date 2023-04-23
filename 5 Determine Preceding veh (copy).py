#确定前车信息，包括前车的id，速度，距离
import pandas as pd
import numpy as np
from tqdm import tqdm

df = pd.read_csv("/media/ubuntu/ANL/Data1_lane_xy_va.csv")
veh_info = pd.read_csv("/media/ubuntu/ANL/Veh_info.csv")
df['Pre_id'] = np.nan
df['Pre_v'] = np.nan
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


for t in tqdm(df['t_sec'].unique()):
    df_t = df[df['t_sec']==t]
    grouped = df_t.groupby(['edge', 'lane'])
    for name, group in grouped:
        edge, lane = name
        if len(group) < 2 or edge in ['node1', 'node2', 'node3']:
            continue
        # 开始根据x/y的大小排序，
        group = group.sort_values(sort_info[edge][0], ascending=sort_info[edge][1])
        df.loc[group.index[0], 'PreVeh_id'] = -1

        c = 1
        for i in group.index[1:]: # i 是按y排序后的行数
            veh_id = df.loc[i, 'id']
            pre_veh_id = df.loc[c, 'id']

            df.loc[i, 'PreVeh_id'] = pre_veh_id
            df.loc[i, 'PreVeh_v'] = df.loc[c, 'v']

            pre_veh_len = float(veh_info.loc[veh_info['id'] == pre_veh_id]['length'])
            veh_len = float(veh_info.loc[veh_info['id'] == veh_id]['length'])

            x1 = df.loc[i, 'x_utm']
            x2 = df.loc[c, 'x_utm']
            y1 = df.loc[i, 'y_utm']
            y2 = df.loc[c, 'y_utm']
            df.loc[i, 'delta_d'] = cal_distance(x1, x2, y1, y2) - 0.5*(pre_veh_len + veh_len)
            c = i

df.to_csv(path_or_buf="/media/ubuntu/ANL/Data1_lane_xy_va_pre.csv", index=False)
