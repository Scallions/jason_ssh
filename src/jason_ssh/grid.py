from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
import matplotlib.pyplot as plt
import numpy as np



def kriging_interpolation(lon, lat, ssha):

    # 1. 定义插值区域
    # grid_lon = np.linspace(np.min(lon), np.max(lon), 80)  # 可改为区域范围
    # grid_lat = np.linspace(np.min(lat), np.max(lat), 80)
    min_lon = np.floor(lon.min())
    max_lon = np.ceil(lon.max())
    min_lat = np.floor(lat.min())
    max_lat = np.ceil(lat.max())
    step = 1
    grid_lon = np.arange(min_lon, max_lon + step, step)
    grid_lat = np.arange(min_lat, max_lat + step, step)
    grid_lon2d, grid_lat2d = np.meshgrid(grid_lon, grid_lat)

    # 2. 克里金插值
    ok = OrdinaryKriging(
        lon, lat, ssha,
        variogram_model="exponential",  # 也可用 'spherical', 'gaussian', 'exponential'
        verbose=False,
        enable_plotting=False
    )

    z_kriged, ssigma = ok.execute("grid", grid_lon, grid_lat)

    # plt.figure(figsize=(10, 6))
    # plt.contourf(grid_lon2d, grid_lat2d, z_kriged, levels=50, cmap='viridis')
    # plt.colorbar(label="SSHA (m)")
    # plt.title("Jason-3 SSHA (Kriging Interpolation)")
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    # plt.grid(True)
    # plt.show()

    return z_kriged, grid_lon, grid_lat

