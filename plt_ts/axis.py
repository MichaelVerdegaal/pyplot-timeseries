"""
This file contains functions related to formatting pyplot axes objects.
"""
from typing import Sequence

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import dates as mdates
from matplotlib import ticker as mticker


class SmartDateLocator(mdates.AutoDateLocator):
    """A smart date locator that extends AutoDateLocator with additional functionality.

    This locator attempts to choose the best locator based on the date range and
    ensures that the number of ticks does not exceed a specified maximum.
    """

    def __init__(
        self,
        minticks: int = 5,
        maxticks: int = 10,
        interval_multiples: bool = True,
    ):
        """
        Initialize the SmartDateLocator.

        Args:
            minticks: The minimum number of ticks to display.
            maxticks: The maximum number of ticks to display.
            interval_multiples: If True, ticks will be chosen to be multiples of intervals.
        """
        super().__init__(
            minticks=minticks,
            maxticks=maxticks,
            interval_multiples=interval_multiples,
        )
        self._max_ticks = maxticks

    def get_locator(
            self, dmin: float, dmax: float
    ) -> mdates.DateLocator | mticker.MaxNLocator:
        """
        Get the appropriate locator based on the date range.

        This method first attempts to use the superclass's locator. If the resulting
        number of ticks exceeds the maximum or if an exception occurs, it falls back
        to using MaxNLocator.

        Args:
            dmin: The minimum date value.
            dmax: The maximum date value.

        Returns:
            A DateLocator from the superclass if suitable, otherwise a MaxNLocator
            with the specified maximum number of ticks.
        """
        locator = super().get_locator(dmin, dmax)
        try:
            ticks = locator()
            if isinstance(ticks, dict):
                ticks = list(ticks.keys())
            if len(ticks) > self._max_ticks:
                return mticker.MaxNLocator(self._max_ticks)
        except Exception:
            return mticker.MaxNLocator(self._max_ticks)
        return locator


def get_x_formatter(date_range: pd.DatetimeIndex) -> mticker.Formatter:
    """Get info about the date range to determine string format

    Args:
        date_range: A pandas DatetimeIndex representing the date range.

    Returns:
        Matplotlib formatter
    """
    # Get info about the date range to determine how to format the x-axis
    time_span = date_range.max() - date_range.min()

    # 1 second to 1 minute
    if pd.Timedelta("1 second") <= time_span < pd.Timedelta("1 minute"):
        str_format = "%H:%M:%S"
    # 1 minute to 1 hour
    elif pd.Timedelta("1 minute") <= time_span < pd.Timedelta("1 hour"):
        str_format = "%d %H:%M"
    # 1 hour to 1 day
    elif pd.Timedelta("1 hour") <= time_span < pd.Timedelta("1 day"):
        str_format = "%m-%d %H:%M"
    # 1 day to 7 days
    elif pd.Timedelta("1 day") <= time_span < pd.Timedelta("7 days"):
        str_format = "%Y-%m-%d"
    # 7 days to 1 month
    elif pd.Timedelta("7 days") <= time_span < pd.Timedelta("30 days"):
        str_format = "%Y-%m-%d"
    # 1 month to 3 months
    elif pd.Timedelta("30 days") <= time_span < pd.Timedelta("90 days"):
        str_format = "%Y-%m-%d"
    # 3 months to 1 year
    elif pd.Timedelta("90 days") <= time_span < pd.Timedelta("365 days"):
        str_format = "%Y-%m-%d"
    # 1 year to 3 years
    elif pd.Timedelta("365 days") <= time_span < pd.Timedelta("1095 days"):
        str_format = "%Y-%m-%d"
    else:
        str_format = "%Y-%m-%d"

    formatter = mdates.DateFormatter(str_format)
    return formatter


def format_axis(ax: plt.Axes, date_range: pd.DatetimeIndex, custom_format) -> plt.Axes:
    """Format the axis of a timeseries plot, primarily the x-axis

    Args:
        ax: The matplotlib axes
        date_range: A pandas DatetimeIndex representing the date range.
        custom_format: A string representing the custom format of the x-axis.

    Returns:
        Pyplot axes
    """
    # Get suitable formatter and locator
    if custom_format:
        x_major_formatter = mdates.DateFormatter(custom_format)
    else:
        x_major_formatter = get_x_formatter(date_range)
    x_major_locator = SmartDateLocator(maxticks=20, interval_multiples=False)
    y_major_locator = mticker.MaxNLocator(10)

    # X-axis formatting
    ax.xaxis.set_major_locator(x_major_locator)
    ax.xaxis.set_major_formatter(x_major_formatter)

    # Y-axis formatting
    ax.yaxis.set_major_locator(y_major_locator)

    # Gridlines
    ax.xaxis.grid(which="both", color="#b2b2b2", linestyle="--", linewidth=0.5)

    return ax


def infer_frequency(timestamps: Sequence) -> str | None:
    """Tries to infer the time-series frequency based on provided x-axis

    Args:
        timestamps: A sequence of timestamps

    Returns:
        Pandas infered frequency string
    """
    try:
        datetime_index = pd.DatetimeIndex(timestamps)
        inferred_frequency = pd.infer_freq(datetime_index)
        return inferred_frequency
    except (TypeError, ValueError):
        return None
