"""

"""

from datetime import datetime
from typing import TypeAlias

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plt_ts.cmaps import register_cmaps
from plt_ts.axis import format_axis, infer_frequency

# Typehint alias
ACCEPTED_X: TypeAlias = list | pd.Series | np.ndarray | None
ACCEPTED_Y: TypeAlias = list | pd.Series | np.ndarray | None

# Figure settings
fig_style = {
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.xmargin": 0,
    "axes.ymargin": 0,
    "axes.zmargin": 0,
    "xtick.direction": "out",
    "ytick.direction": "out",
}
mpl.rcParams.update(fig_style)
register_cmaps()


def plot_ts(
    x_values: ACCEPTED_X = None,
    y_values: ACCEPTED_Y = None,
    rows: int = 1,
    cols: int = 1,
    frequency: str = None,
    custom_format: str = None,
    start_time: pd.Timestamp | datetime | str | None = None,
    cmap: str = "pong7",
) -> tuple[plt.Figure, plt.Axes, pd.DatetimeIndex]:
    """Helper function which formats the majority of your pytplot figure and axes

    It does many things, but the most important of these are:
    - Style settings which fit the time-series data better
    - Automatic axis formatting and tick selection
    - Custom colormap

    Note that inequally spaced samples are not supported yet.

    Ref: https://matplotlib.org/stable/api/ticker_api.html#tick-locating-and-formatting
    Ref: https://matplotlib.org/stable/users/explain/colors/colormap-manipulation.html
    Ref: https://matplotlib.org/stable/users/explain/customizing.html#temporary-rc-settings
    Ref: https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases


    Args:
        x_values: A sample of your x-values. This is used to infer a suitable
         date-time range which matches your data.
        y_values: A sample of your y-values. Mostly used in absence of x_values, to
         infer the time-step count of your data.
        rows: The number of subplot rows in your plot. Defaults to 1
        cols: The number of subplot columns in your plot. Defaults to 1
        frequency: Use this if you want to provide a custom frequency for your x-axis
         range. Is inferred if x_values is not None.
        custom_format: The formatter of the x-axis. Is inferred if x_values is not None.
        start_time: The start date-time of your data. Can be provided, but is inferred
         if x_values is not None.
        cmap: The colormap to use. Defaults to 'pong7' custom colormap.

    Returns:
        Pyplot figure, pyplot axes, newly generated x-axis values (date-range)
    """
    # Validation
    if not isinstance(x_values, list | pd.Series | np.ndarray | None):
        raise TypeError("x_values must be a list, pd.Series, np.ndarray, or None")
    if not isinstance(x_values, list | pd.Series | np.ndarray | None):
        raise TypeError("y_values must be a list, pd.Series, np.ndarray, or None")
    if x_values is None and y_values is None:
        raise ValueError("Must provide at least 1 of x or y values")
    if rows < 1:
        raise ValueError("rows must be at least 1")
    if cols < 1:
        raise ValueError("cols must be at least 1")

    # Get timesteps
    periods = len(x_values) if x_values is not None else len(y_values)

    # user-provided takes priority, then inferred, then default
    freq = frequency or infer_frequency(x_values) or "1D"

    # get start time
    if not start_time:
        if x_values is not None:
            if isinstance(x_values, pd.Series):
                start_time = x_values.iloc[0]
            else:
                start_time = x_values[0]
        else:
            # default time
            start_time = pd.Timestamp(f"{pd.Timestamp.now().year}-01-01")

    # create new x-axis values
    new_x_values = pd.date_range(
        start=start_time, periods=periods, freq=freq, inclusive="left"
    )

    # Create figure and axes (with dynamic figsize)
    plot_height = 6 + (rows * 2)
    plot_width = 14 + (cols * 2)
    fig, axs = plt.subplots(rows, cols, figsize=(plot_width, plot_height))

    # Set colormap
    cmap = plt.get_cmap(cmap)
    plt.set_cmap(cmap)

    # Axis formatting
    # TODO: Check if all formatting happens in-place
    if rows == 1 and cols == 1:
        axs = format_axis(axs, new_x_values, custom_format)
    else:
        axs_flat = axs.flatten()  # Flatten 2D list
        for ax in axs_flat:
            ax = format_axis(ax, new_x_values, custom_format)

    # This rotates and aligns the x-tick labels, to avoid overlap
    fig.autofmt_xdate()

    # This adjusts the padding around subplots to make more room
    plt.tight_layout(pad=2)

    return fig, axs, new_x_values
