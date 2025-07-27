

import netCDF4 as nc
from datetime import datetime, timedelta
import numpy as np
import xarray as xr
import pygmt
import pandas as pd

import glob
from dataclasses import dataclass
import os

@dataclass
class JasonData:
    time: np.ndarray
    lat: np.ndarray
    lon: np.ndarray
    ssha: np.ndarray
    mss: np.ndarray
    track_id: np.ndarray
    period_id: np.ndarray

    def to_dataframe(self):
        return pd.DataFrame({
            "time": self.time,
            "lat": self.lat,
            "lon": self.lon,
            "ssha": self.ssha,
            "mss": self.mss,
            "track_id": self.track_id,
            "period_id": self.period_id
        })
    
    @staticmethod
    def from_dataframe(df: pd.DataFrame):
        return JasonData(
            time=np.array(df["time"].values),
            lat=np.array(df["lat"].values),
            lon=np.array(df["lon"].values),
            ssha=np.array(df["ssha"].values),
            mss=np.array(df["mss"].values),
            track_id=np.array(df["track_id"].values),
            period_id=np.array(df["period_id"].values)
        )
    
    def sort_by_time(self):
        sorted_indices = np.argsort(self.time)
        return JasonData(
            time=self.time[sorted_indices],
            lat=self.lat[sorted_indices],
            lon=self.lon[sorted_indices],
            ssha=self.ssha[sorted_indices],
            mss=self.mss[sorted_indices],
            track_id=self.track_id[sorted_indices],
            period_id=self.period_id[sorted_indices]
        )
def read_data(file_path):
    dataset = nc.Dataset(file_path)
    data_01 = dataset.groups["data_01"]
    time = data_01["time"][:].data
    lat = data_01["latitude"][:].data
    lon = data_01["longitude"][:].data
    ssha = data_01["ku"]["ssha"][:].data
    mss = data_01["mean_sea_surface_sol1"][:].data
    ref_date = datetime(2000, 1, 1)
    dates = np.array([ref_date + timedelta(seconds=t) for t in time])
    valid = ~data_01["ku"]["ssha"][:].mask

    dates = dates[valid]
    lat = lat[valid]
    lon = lon[valid]
    ssha = ssha[valid]
    mss = mss[valid]
    return dates, lat, lon, ssha, mss


def read_dir_data(data_dir):
    file_paths = glob.glob(f"{data_dir}\\**\\*.nc")
    datasets = []
    for file_path in file_paths:
        # 使用 load_data 加载数据，并拼接
        file_name = os.path.basename(file_path)
        track_id = file_name.split("_")[3]
        period_id = file_name.split("_")[2]
        dates, lat, lon, ssha, mss = read_data(file_path)
        track_id = np.full(dates.shape, track_id)
        period_id = np.full(dates.shape, period_id)
        datasets.append((dates, lat, lon, ssha, mss, track_id, period_id))
    # 拼接到一个数组
    dates = np.concatenate([d[0] for d in datasets])
    lat = np.concatenate([d[1] for d in datasets])
    lon = np.concatenate([d[2] for d in datasets])
    ssha = np.concatenate([d[3] for d in datasets])
    mss = np.concatenate([d[4] for d in datasets])
    track_id = np.concatenate([d[5] for d in datasets])
    period_id = np.concatenate([d[6] for d in datasets])
    # 按日期排序
    sorted_indices = np.argsort(dates)
    dates = dates[sorted_indices]
    lat = lat[sorted_indices]
    lon = lon[sorted_indices]
    ssha = ssha[sorted_indices]
    mss = mss[sorted_indices]
    track_id = track_id[sorted_indices]
    period_id = period_id[sorted_indices]
    # 返回 JasonData 对象
    return JasonData(
        time=dates,
        lat=lat,
        lon=lon,
        ssha=ssha,
        mss=mss,
        track_id=track_id,
        period_id=period_id
    )

def filter_region(data: JasonData, lon_range, lat_range):
    region_mask = (data.lon >= lon_range[0]) & (data.lon <= lon_range[1]) & \
                  (data.lat >= lat_range[0]) & (data.lat <= lat_range[1])
    return JasonData(
        time=data.time[region_mask],
        lat=data.lat[region_mask],
        lon=data.lon[region_mask],
        ssha=data.ssha[region_mask],
        mss=data.mss[region_mask],
        track_id=data.track_id[region_mask],
        period_id=data.period_id[region_mask]
    )


def filter_date(data: JasonData, start_date, end_date):
    time_mask = (data.time >= start_date) & (data.time <= end_date)
    return JasonData(
        time=data.time[time_mask],
        lat=data.lat[time_mask],
        lon=data.lon[time_mask],
        ssha=data.ssha[time_mask],
        mss=data.mss[time_mask],
        track_id=data.track_id[time_mask],
        period_id=data.period_id[time_mask]
    )


def filter_period(data: JasonData, period_id):
    period_mask = (data.period_id == period_id)
    return JasonData(
        time=data.time[period_mask],
        lat=data.lat[period_mask],
        lon=data.lon[period_mask],
        ssha=data.ssha[period_mask],
        mss=data.mss[period_mask],
        track_id=data.track_id[period_mask],
        period_id=data.period_id[period_mask]
    )

def save_data(file_path, data: JasonData):
    np.savez(file_path, time=data.time, lat=data.lat, lon=data.lon, ssha=data.ssha, mss=data.mss, track_id=data.track_id, period_id=data.period_id)


def load_data(file_path):
    data = np.load(file_path, allow_pickle=True)
    return JasonData(
        time=data['time'],
        lat=data['lat'],
        lon=data['lon'],
        ssha=data['ssha'],
        mss=data['mss'],
        track_id=data['track_id'],
        period_id=data['period_id']
    )

def mask_sea(z_kriged, grid_lon, grid_lat):
    # 创建 xarray 数据结构
    ds = xr.Dataset(
        {
            "ssha": (["lat", "lon"], z_kriged)
        },
        coords={
            "lon": grid_lon,
            "lat": grid_lat
        },
    )
    region = [float(ds.lon.min()), float(ds.lon.max()),
            float(ds.lat.min()), float(ds.lat.max())]

    # 生成陆地掩码，陆地=1，海洋=0
    land_mask = pygmt.grdlandmask(
        region=region,
        spacing=1,                 # 必须匹配你的格网间距
        maskvalues=[1, 0],           # [陆地值, 海洋值]
        resolution="auto"
    )
    masked_ssha = ds["ssha"].where(land_mask == 0)
    masked_ds = xr.Dataset(
        {"ssha": (["lat", "lon"], masked_ssha.data)},
        coords={"lat": ds.lat, "lon": ds.lon}
    )
    return masked_ds


def group_mean_by_track(data: JasonData):
    """
    按 period_id 和 track_id 分组计算平均值，拼接成新的序列
    """
    df = data.to_dataframe()
    df = df.groupby(["period_id", "track_id"], as_index=False).mean()
    data = JasonData.from_dataframe(df)
    # 按日期排序
    data = data.sort_by_time()
    return data


def remove_period(data: JasonData, period_id):
    """
    移除指定 period_id 的数据
    """
    period_mask = (data.period_id != period_id)
    return JasonData(
        time=data.time[period_mask],
        lat=data.lat[period_mask],
        lon=data.lon[period_mask],
        ssha=data.ssha[period_mask],
        mss=data.mss[period_mask],
        track_id=data.track_id[period_mask],
        period_id=data.period_id[period_mask]
    )

