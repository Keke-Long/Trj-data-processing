# calculate speed
import pandas as pd
import numpy as np
from tqdm import tqdm

def cal_distance(x1,x2,y1,y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

df = pd.read_csv("/media/ubuntu/ANL/Data1_lane_xynew.csv")
df["v"] = np.nan
df["a"] = np.nan

veh_list = df['id'].unique()

new_d = []
new_d = pd.DataFrame(new_d)

for veh in tqdm(veh_list, desc='Processing vehicles'):
    d = df[df['id'] == veh]
    """
    Cal v
    """
    for i, row in d.iterrows():
        veh_id = row['id']
        t = row['t_sec']
        x_t = row['x_utm']
        y_t = row['y_utm']
        pos2 = np.flatnonzero( (d['t_sec'] == t+0.1) )
        if len(pos2) == 1:
            x_t_next = d.iloc[pos2[0]]['x_utm']
            y_t_next = d.iloc[pos2[0]]['y_utm']
            v = cal_distance(x_t, x_t_next, y_t, y_t_next) / 0.1
            d.loc[i, "v"] = round(v,3)

    """
    Cal a
    """
    for i, row in d.iterrows():
        veh_id = row['id']
        t = row['t_sec']
        v = row['v']
        pos2 = np.flatnonzero( (d['t_sec'] == t+0.1) )
        if len(pos2) == 1:
            v_t_next = d.iloc[pos2[0]]['v']
            a = (v_t_next - v) / 0.1
            d.loc[i, "a"] = round(a,3)
    new_d = pd.concat([new_d, d], axis=0)

new_d.to_csv(path_or_buf="/media/ubuntu/ANL/Data1_lane_xy_va.csv", index=False)