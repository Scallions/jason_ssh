

import numpy as np
import pandas as pd

from jason_ssh.data import JasonData


def trend_all(data: JasonData):
    
    df = data.to_dataframe()
    time = np.array(df["time"].values - df["time"].values[0], dtype='timedelta64[s]') / np.timedelta64(1, 'Y').astype('timedelta64[s]')
    # 转化为mm
    ssha = np.array(df["ssha"].values) * 1000
    # 使用线性回归计算趋势
    A = np.vstack([time.astype(float), np.ones(len(time))]).T
    m, c = np.linalg.lstsq(A, ssha, rcond=None)[0]
    trend = m * time.astype(float) + c
    df["trend"] = trend / 1000  # 转回m
    df["linear_rate"] = m
    return df[["time", "ssha", "trend", "linear_rate"]]

def trend_by_track(data: JasonData):
    
    df = data.to_dataframe()
    df = df.groupby(["period_id", "track_id"], as_index=False).mean()
    
    # 对每个track_id计算趋势
    for track_id in np.unique(df["track_id"]):
        track_df = df[df["track_id"] == track_id]
        track_df = track_df.sort_values(by="time")
        # 计算ssha趋势, 年变化率
        time = np.array(track_df["time"].values - track_df["time"].values[0], dtype='timedelta64[s]') / np.timedelta64(1, 'Y').astype('timedelta64[s]')
        # 转化为mm
        ssha = np.array(track_df["ssha"].values) * 1000
        # 使用线性回归计算趋势
        A = np.vstack([time.astype(float), np.ones(len(time))]).T
        m, c = np.linalg.lstsq(A, ssha, rcond=None)[0]
        trend = m * time.astype(float) + c
        track_df["trend"] = trend
        track_df["linear_rate"] = m
        df.loc[df["track_id"] == track_id, "trend"] = trend
        df.loc[df["track_id"] == track_id, "linear_rate"] = m

    return df[["period_id", "track_id", "trend", "linear_rate"]]

def trend_by_period(data: JasonData) -> pd.DataFrame:
    """
    按 period_id 计算趋势
    """
    df = data.to_dataframe()
    df = df.groupby("period_id").mean().reset_index()
    
    # 对每个period_id计算趋势
    for period_id in np.unique(df["period_id"]):
        period_df = df[df["period_id"] == period_id]
        period_df = period_df.sort_values(by="time")
        # 计算ssha趋势, 年变化率
        time = np.array(period_df["time"].values - period_df["time"].values[0], dtype='timedelta64[s]') / np.timedelta64(1, 'Y').astype('timedelta64[s]')
        # 转化为mm
        ssha = np.array(period_df["ssha"].values) * 1000
        # 使用线性回归计算趋势
        A = np.vstack([time.astype(float), np.ones(len(time))]).T
        m, c = np.linalg.lstsq(A, ssha, rcond=None)[0]
        trend = m * time.astype(float) + c
        df.loc[df["period_id"] == period_id, "trend"] = trend
        df.loc[df["period_id"] == period_id, "linear_rate"] = m

    return df[["period_id", "trend", "linear_rate"]]