

from jason_ssh.data import filter_region, load_data
from jason_ssh.trend import trend_by_track


data_path = "data/ssh_data.npz"
data = load_data(data_path)

# 东海
lon_range = (120, 130)
lat_range = (25, 35)

data = filter_region(data, lon_range, lat_range)

trend_data = trend_by_track(data)