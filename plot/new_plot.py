"""

"""
from typing import Type
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot.cmaps import register_cmaps
from plot.xaxis import format_axis, infer_frequency

# Typehint alias
type ACCEPTED_X = list | pd.Series | np.ndarray | None
type ACCEPTED_Y = list | pd.Series | np.ndarray | None

# Figure settings
fig_style = {
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.xmargin': 0,
    'axes.ymargin': 0,
    'axes.zmargin': 0,
    'xtick.direction': 'out',
    'ytick.direction': 'out'
}
mpl.rcParams.update(fig_style)
register_cmaps()


def plot_ts(x_values: ACCEPTED_X = None,
            y_values: ACCEPTED_Y = None,
            rows: int = 1,
            cols: int = 1,
            frequency: str = None,
            custom_format: str = None,
            start_time: pd.Timestamp | datetime | str | None = None,
            cmap: str = "pong7",
            ) -> tuple[plt.Figure, plt.Axes, pd.DatetimeIndex]:
    """
    Ref: https://matplotlib.org/stable/users/explain/customizing.html#temporary-rc-settings
    Ref: https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases
    """
    # TODO: pre-commit
    # TODO: cleaning
    # TODO: make it a package / usable by others
    # TODO: documentation
    # TODO: tests?
    # Validation
    if not isinstance(x_values, type(ACCEPTED_X)):
        raise TypeError("x_values must be a list, pd.Series, np.ndarray, or None")
    if not isinstance(y_values, type(ACCEPTED_Y)):
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

    # create new x-axis
    date_range = pd.date_range(start=start_time,
                               periods=periods,
                               freq=freq,
                               inclusive="left")

    # Create subplots
    plot_height = 6 + (rows * 2)
    plot_width = 14 + (cols * 2)
    fig, axs = plt.subplots(rows, cols, figsize=(plot_width, plot_height))

    # Set colormap
    cmap = plt.get_cmap(cmap)
    plt.set_cmap(cmap)

    # Axis formatting
    if rows == 1 and cols == 1:
        axs = format_axis(axs, date_range, custom_format)
    else:
        axs_flat = axs.flatten()  # Flatten 2D list
        for ax in axs_flat:
            ax = format_axis(ax, date_range, custom_format)

    # This rotates and aligns the xtick labels, to avoid overlap
    fig.autofmt_xdate()

    # This adjusts the padding around subplots to make more room
    plt.tight_layout(pad=2)

    return fig, axs, date_range
