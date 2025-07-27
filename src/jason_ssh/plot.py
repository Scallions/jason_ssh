from matplotlib import pyplot as plt
import xarray as xr
import pygmt

def plot_map(lon, lat, ssha, time):
    down_sample_factor = 10
    lon = lon[::down_sample_factor]
    lat = lat[::down_sample_factor]
    ssha = ssha[::down_sample_factor]
    plt.figure(figsize=(10, 6))
    plt.scatter(lon, lat, c=ssha, cmap='viridis', marker='o', s=0.5)
    plt.colorbar(label='SSH Anomaly (m)')
    plt.title('SSH Anomaly Map')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    plt.savefig(f'figs/xx.png')
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
    ds.to_netcdf("data/jason3_ssha_kriging.nc")



    fig = pygmt.Figure()

    min_lon = float(ds.lon.min())
    max_lon = float(ds.lon.max())
    min_lat = float(ds.lat.min())
    max_lat = float(ds.lat.max())

    # 构建 PyGMT region 列表
    region = [min_lon, max_lon, min_lat, max_lat]

    # 读取 netCDF 网格数据绘图
    fig.grdimage(
        grid="data/jason3_ssha_kriging.nc",
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

    fig.savefig(f"figs/{pic_name}")
