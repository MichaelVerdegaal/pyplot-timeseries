"""
This file contains functions and filed related to creating plots (pyplot)
"""

from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cycler import cycler
from matplotlib import ticker

from .cmaps import register_cmaps
from .constants import ONE_DAY_TIMESTEPS, ONE_TIMESTEP, ONE_WEEK_TIMESTEPS

register_cmaps()


def timeseries_style_path():
    """Returns the timeseries.mplstyle as path

    Useful in case you manually want to activate the style

    Returns:
        Path to style
    """
    return Path(__file__).parent / "timeseries.mplstyle"


def xaxis_helper(
    start_time: datetime, signal_length: int, minute_increment: int
) -> tuple[pd.DatetimeIndex, str, ticker.Locator]:
    """Calculates values necessary to format the x-axis of a timeseries plot
    with datetime values

    Args:
        start_time: start time of the signal
        signal_length: length of the signal
        minute_increment: increment of the signal

    Returns:
        timestamp collection, x-axis date format, x-axis locator
    """
    end_time = start_time + timedelta(minutes=signal_length * minute_increment)
    times = pd.date_range(
        start_time, end_time, freq=f"{minute_increment}min", inclusive="left"
    )
    # Within a day of data
    if signal_length <= ONE_DAY_TIMESTEPS:
        str_format = "%m-%d %H:%M"
        locator = mdates.HourLocator()
    # Within a week of data
    elif ONE_DAY_TIMESTEPS < signal_length <= ONE_WEEK_TIMESTEPS:
        str_format = "%m-%d %H:%M"
        locator = mdates.AutoDateLocator()
    # Within a month of data (assuming the minimum of 28 days)
    elif ONE_WEEK_TIMESTEPS < signal_length <= (28 * ONE_DAY_TIMESTEPS):
        str_format = "%m-%d %H:%M"
        locator = mdates.DayLocator()
    # More than a month of data
    else:
        str_format = "%y-%m-%d"
        locator = mdates.WeekdayLocator()

    return times, str_format, locator


def timeseries_plot(
    signal: pd.Series | np.ndarray | list,
    minute_increment: int = ONE_TIMESTEP,
    timezone_offset: int = 0,
    start_time: datetime = None,
    rows: int = 1,
    cols: int = 1,
) -> tuple[plt.Figure, plt.Axes, pd.DatetimeIndex]:
    """pyplot helper function to create a timeseries focused plot

    - Use a custom mplstyle
    - Prepare the x-axis for timestamps on the hour:minute scale
    - Space axis tickers
    - Set tight_layout to remove unused whitespace
    - Set vertical gridlines

    Args:
        signal: timeseries signal
        minute_increment: increment of the x-axis (minutes)
        timezone_offset: timezone offset in hours used for the timestamps on
         the x-axis (e.g. +2 to start at 2am)
        start_time: only applicable if signal occurs over multiple days; sets
        the start time of the signal to a specified timestamp.
        rows: number of row subplots
        cols: number of column subplots

    Returns:
        pyplot figure, pyplot axis, list of timestamps as strings
    """

    def format_axis(
        axis: plt.Axes, color_map: plt.cm
    ) -> tuple[plt.Axes, pd.DatetimeIndex]:
        """Set axis properties to our liking

        Args:
            axis: pyplot axis
            color_map: pyplot color map

        Returns:
            pyplot axis
        """
        ## Ticks
        axis.minorticks_on()
        # Format x-axis
        start_base = (
            start_time if start_time else datetime(2021, 1, 1, timezone_offset, 0, 0)
        )
        times, str_format, locator = xaxis_helper(
            start_base, signal_length, minute_increment
        )
        axis.xaxis.set_major_formatter(mdates.DateFormatter(str_format))
        axis.xaxis.set_major_locator(locator)
        fig.autofmt_xdate()
        # Set at least 10 y major ticks
        axis.yaxis.set_major_locator(ticker.MaxNLocator(10))

        ## Gridlines
        axis.xaxis.grid(which="both", color="#b2b2b2", linestyle="--", linewidth=0.5)

        ## Color cycle
        axis.set_prop_cycle(cycler(color=color_map.colors))

        return axis, times

    signal_length = len(signal)
    if signal_length < 1:
        raise ValueError("Length must be at least 1")
    if minute_increment < 1:
        raise ValueError("minute_increment must be at least 1")
    if timezone_offset not in range(-24, 24):
        raise ValueError("Timezone offset must be between -24 and 24")
    if rows < 1:
        raise ValueError("rows must be at least 1")
    if cols < 1:
        raise ValueError("cols must be at least 1")

    # Plot styling
    with plt.style.context(timeseries_style_path()):
        fig, axs = plt.subplots(rows, cols)

        ### Custom color map
        cmap = plt.get_cmap("pong7")
        plt.set_cmap(cmap)

        ### Axis formatting
        if rows == 1 and cols == 1:
            axs, times = format_axis(axs, cmap)
        else:
            # Flatten multi-dimensional axes
            axs_flat = axs.flatten()
            for ax in axs_flat:
                ax, times = format_axis(ax, cmap)

        ### Remove unused whitespace
        plt.tight_layout(pad=2)

        return fig, axs, times
