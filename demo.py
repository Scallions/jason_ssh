from datetime import datetime
from jason_ssh.data import filter_date, filter_period, filter_region, load_data, read_dir_data, save_data
from jason_ssh.grid import kriging_interpolation
from jason_ssh.plot import plot_grid, plot_map

data_dir = "D:\\Data\\datasets\\ssh\\"
data_path = "data/ssh_data.npz"

lon_range = (100, 130)
lat_range = (0, 43)


# data = read_dir_data(data_dir)
# # 持久化保存结果

# save_data(data_path, data)

# 加载数据
data = load_data(data_path)



start_time = datetime(2025, 2, 1)
end_time = datetime(2025, 2, 11)

# data = filter_date(data, start_time, end_time)

data = filter_region(data, lon_range, lat_range)

# 按perriod_id分类

for period_id in set(data.period_id):
    period_data = filter_period(data, period_id)

    ssh = period_data.mss + period_data.ssha

    # plot_map(period_data.lon, period_data.lat, period_data.ssha, period_data.time)

    z_kriged, grid_lon, grid_lat = kriging_interpolation(period_data.lon, period_data.lat, period_data.ssha)

    plot_grid(z_kriged, grid_lon, grid_lat, pic_name=f"jason3_ssha_kriging_{period_id}.png")