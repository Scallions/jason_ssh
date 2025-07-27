import os
from matplotlib import pyplot as plt
import pandas as pd
import xarray as xr
import pygmt

from jason_ssh.data import JasonData

def plot_map(lon, lat, ssha, time, fig_name="jason3_ssha_map.png"):
    down_sample_factor = 10
    lon = lon[::down_sample_factor]
    lat = lat[::down_sample_factor]
    ssha = ssha[::down_sample_factor]
    plt.figure(figsize=(10, 6))
    plt.scatter(lon, lat, c=ssha, cmap='viridis', marker='o', s=0.1)
    plt.colorbar(label='SSH Anomaly (m)')
    plt.title('SSH Anomaly Map')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    if not os.path.exists("figs"):
        os.makedirs("figs")
    plt.savefig(f'figs/{fig_name}')
    # plt.show()


def plot_grid(ssha, grid_lon, grid_lat, pic_name="jason3_ssha_kriging.png"):
    # 创建 xarray 数据结构
    ds = xr.Dataset(
        {
            "ssha": (["lat", "lon"], ssha)
        },
        coords={
            "lon": grid_lon,
            "lat": grid_lat
        },
    )

    # 保存为 NetCDF 文件供 PyGMT 使用
    if not os.path.exists("data"):
        os.makedirs("data")
    nc_file_path = f"data/{pic_name.replace('.png', '.nc')}"
    ds.to_netcdf(nc_file_path, mode='w')



    fig = pygmt.Figure()

    min_lon = float(ds.lon.min())
    max_lon = float(ds.lon.max())
    min_lat = float(ds.lat.min())
    max_lat = float(ds.lat.max())

    # 构建 PyGMT region 列表
    region = [min_lon, max_lon, min_lat, max_lat]

    # 读取 netCDF 网格数据绘图
    fig.grdimage(
        grid=nc_file_path,
        region=region,
        projection="M6i",  # Mercator 投影
        # projection="L121.5/20/10/40/6i",
        cmap="viridis",
        shading=True,
        frame=["a", "+tSSH from Jason-3 (Kriging)"]
    )

    # 加上海岸线
    fig.coast(
        shorelines=True, 
        resolution="auto", 
        land="gray", 
        lakes="skyblue",
    )

    # 加颜色条
    fig.colorbar(frame='af+lSSH (m)')

    # 显示图形
    # fig.show()
    if not os.path.exists("figs"):
        os.makedirs("figs")
    fig.savefig(f"figs/{pic_name}")


def plot_time_series(data: JasonData, fig_name="jason3_china_track_timeseries.png"):

    plt.figure(figsize=(10, 6))
    plt.plot(data.time, data.ssha, marker='o', linestyle='-', markersize=2)
    plt.title('SSH Anomaly Time Series')
    plt.xlabel('Time')
    plt.ylabel('SSH Anomaly (m)')
    plt.grid()
    if not os.path.exists("figs"):
        os.makedirs("figs")
    plt.savefig(f'figs/{fig_name}')
    # plt.show()


def plot_ts_trend(df: pd.DataFrame, fig_name="jason3_china_track_timeseries_trend.png"):
    """
    绘制时间序列趋势图
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df['trend'], marker='o', linestyle='-', markersize=2, label=f'Trend({df["linear_rate"].iloc[0]:.2f} mm/year)')
    plt.plot(df['time'], df['ssha'], marker='x', linestyle='--', markersize=1, label='SSH Anomaly')
    plt.title('SSH Anomaly Trend')
    plt.xlabel('Time')
    plt.ylabel('SSH Anomaly (m)')
    plt.legend()
    plt.grid()
    if not os.path.exists("figs"):
        os.makedirs("figs")
    plt.savefig(f'figs/{fig_name}')
    # plt.show()
    # plt.close()


