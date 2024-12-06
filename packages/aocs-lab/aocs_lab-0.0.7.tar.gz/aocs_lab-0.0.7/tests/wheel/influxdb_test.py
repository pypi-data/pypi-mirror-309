import numpy as np
import wheel_data_process
import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
from aocs_lab.utils import time
from aocs_lab import influxdb2


wheel_test = {
    "start_time": '2024-09-21T09:00:00',
    "end_time": '2024-09-21T09:40:00',
    "tm_tag": ['TMKA553', 'TMKA561', 'TMKA569', 'TMKA577']
}

sat_database = {
    "C03": {
        'url': "http://172.16.111.211:8086",
        'token': "u0OGUlvv6IGGYSxpoZGZNjenBtE-1ADcdun-W-0oacL66cef5DXPmDwVzj93oP1MRBBCCUOWNFS9yMb77o5OCQ==",
        'org': "gs",
        'bucket': "piesat02_c03_database"
    }
}

data_list = influxdb2.get_field_value_from_influxdb(
    sat_database['C03'],
    time.beijing_to_utc_time_str(wheel_test['start_time']), 
    time.beijing_to_utc_time_str(wheel_test['end_time']), 
    wheel_test['tm_tag'])

data_array = np.array(data_list)


for i in range(len(wheel_test['tm_tag'])):
    dt = wheel_data_process.calc_slide_time(data_array[:,0], data_array[:,i+1], 5990, 3000)
    print(f"飞轮 {i} 惯滑时间为 {dt:.0f} s")

