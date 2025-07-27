from datetime import datetime
from jason_ssh.data import filter_date, filter_period, filter_region, group_mean_by_track, load_data, mask_sea, read_dir_data, save_data
from jason_ssh.grid import kriging_interpolation
from jason_ssh.plot import plot_grid, plot_map, plot_time_series

data_dir = "D:\\Data\\datasets\\ssh\\"
data_path = "data/ssh_data.npz"

lon_range = (100, 130)
lat_range = (0, 43)

# 东海
lon_range = (120, 130)
lat_range = (25, 35)


data = read_dir_data(data_dir)
# # 持久化保存结果

save_data(data_path, data)

# 加载数据
data = load_data(data_path)

# plot_map(data.lon, data.lat, data.ssha, data.time, fig_name="jason3_global_track_downsample_10x.png")

# exit(0)

start_time = datetime(2025, 2, 1)
end_time = datetime(2025, 2, 11)

# data = filter_date(data, start_time, end_time)

data = filter_region(data, lon_range, lat_range)

data = group_mean_by_track(data)

# plot_time_series(data, fig_name="jason3_china_track_timeseries.png")

# plot_map(data.lon, data.lat, data.ssha, data.time, fig_name="jason3_china_track_downsample_10x.png")

# exit(0)

# 按perriod_id分类

# for period_id in set(data.period_id):
#     period_data = filter_period(data, period_id)

#     ssh = period_data.mss + period_data.ssha

#     # plot_map(period_data.lon, period_data.lat, period_data.ssha, period_data.time)

#     z_kriged, grid_lon, grid_lat = kriging_interpolation(period_data.lon, period_data.lat, period_data.ssha)

#     # masked_ssha = mask_sea(z_kriged, grid_lon, grid_lat)

#     # print(f"Period mean time: {period_data.time[0]}")
#     # print(f"Period ID: {period_id}, mean: {masked_ssha.mean().values}")

#     plot_grid(z_kriged, grid_lon, grid_lat, pic_name=f"jason3_ssha_kriging_east_{period_id}.png")