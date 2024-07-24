"""

"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from plot.xaxis import format_axis


def infer_frequency(timestamps):
    try:
        datetime_index = pd.DatetimeIndex(timestamps)
        inferred_frequency = pd.infer_freq(datetime_index)
        return inferred_frequency
    except (TypeError, ValueError):
        return None

fig_style = {
    'figure.figsize': (16, 9),
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


@mpl.rc_context(fig_style)
def plot_ts(x_values=None,
            y_values=None,
            rows=1,
            cols=1,
            frequency=None,
            custom_format=None,
            start_time=None):
    """
    Ref: https://matplotlib.org/stable/users/explain/customizing.html#temporary-rc-settings
    Ref: https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases
    """
    # TODO: minor tick formatting (they're not evenly spaced which is hard to read)
    # TODO: parameter validation
    # TODO: custom cmap
    # TODO: handle multi row/col plots
    # TOOD: pre-commit
    # TODO: cleaning
    # TODO: make it a package / usable by others
    # TODO: documentation
    # TODO: tests? ..... ugh

    if x_values is None and y_values is None:
        raise ValueError("Must provide at least 1 of x or y values")

    # Get timesteps
    periods = len(x_values) if x_values is not None else len(y_values)

    # user-provided takes priority, then inferred, then default
    freq = frequency or infer_frequency(x_values) or "1D"

    # get start time
    if not start_time:
        if x_values is not None:
            start_time = x_values[0]
        else:
            # default time
            start_time = pd.Timestamp(f"{pd.Timestamp.now().year}-01-01")

    # create new x-axis
    date_range = pd.date_range(start=start_time,
                               periods=periods,
                               freq=freq,
                               inclusive="left")

    # ...
    fig, axs = plt.subplots(rows, cols)

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
