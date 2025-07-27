import sys
from concurrent.futures import ProcessPoolExecutor
import tkinter.filedialog
from typing import Optional

import gradio as gr
import webview

from jason_ssh.data import JasonData, filter_region, group_mean_by_track, load_data, read_dir_data
from jason_ssh.grid import kriging_interpolation
from jason_ssh.plot import plot_grid, plot_time_series, plot_ts_trend
from jason_ssh.trend import trend_all

def greet(name):
    return "Hello " + name + "!"

jason_data: Optional[JasonData] = None
china_lon_range = (100, 130)
china_lat_range = (0, 43)
east_lon_range = (120, 130)
east_lat_range = (25, 35)

def select_dir():
    global jason_data
    dir = tkinter.filedialog.askdirectory()
    if dir:
        print(f"Selected directory: {dir}")
        # jason_data = read_dir_data(dir)
        dir = "data/ssh_data.npz"
        jason_data = load_data(dir)
        jason_data.sort_by_time()
        return "Loaded data from " + dir
    else:
        print("No directory selected")
        return None


def interpolate():
    global jason_data
    if jason_data is None:
        return "No data loaded"
    data = filter_region(jason_data, china_lon_range, china_lat_range)
    z_kriged, grid_lon, grid_lat = kriging_interpolation(data.lon, data.lat, data.ssha)
    plot_grid(z_kriged, grid_lon, grid_lat, pic_name=f"jason3_ssha_kriging_east.png")
    # 返回 gradio image
    image_path = f"figs/jason3_ssha_kriging_east.png"
    return gr.Image(image_path, label="Kriged SSH Anomaly Map")

def trend():
    global jason_data
    if jason_data is None:
        return "No data loaded"
    data = filter_region(jason_data, east_lon_range, east_lat_range)
    data = group_mean_by_track(data)
    df = trend_all(data)
    plot_ts_trend(df, "jason3_east_track_timeseries_trend.png")
    return gr.Image("figs/jason3_east_track_timeseries_trend.png", label="Trend Image")


def gui():
    with gr.Blocks() as demo:
        with gr.Tab(label="Data"):
            btn = gr.Button("Load Data")
            dir_output = gr.Textbox(label="Selected Directory")
            btn.click(select_dir, outputs=dir_output)
        with gr.Tab(label="插值"):
            grid_img = gr.Image(label="Grid Image")
            btn2 = gr.Button("插值")
            btn2.click(interpolate, outputs=grid_img)
        with gr.Tab(label="趋势"):
            trend_img = gr.Image(label="Trend Image")
            btn3 = gr.Button("趋势")
            btn3.click(trend, outputs=trend_img)

    demo.launch(prevent_thread_lock=True)

def on_window_close():
    sys.exit()


def launch_webview():
    window = webview.create_window("App", "http://localhost:7860/")
    window.events.closed += on_window_close
    webview.start()


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        executor.submit(gui)
        executor.submit(launch_webview)