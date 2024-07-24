import numpy as np
import pandas as pd


def generate_time_series(start_time, interval, num_steps, interval_type='minutes',
                         slope=1, intercept=0, noise_level=0.1):
    """
    Generate a time series with specified interval and number of steps.
    The values will follow a linear trend with added noise.

    Parameters:
    start_time (str): The starting time of the time series in 'YYYY-MM-DD HH:MM:SS' format.
    interval (int): The interval between each step.
    num_steps (int): The number of steps in the time series.
    interval_type (str): The type of interval ('seconds', 'minutes', 'hours', 'days', 'weeks').
    slope (float): The slope of the linear trend.
    intercept (float): The intercept of the linear trend.
    noise_level (float): The standard deviation of the noise.

    Returns:
    pd.DataFrame: A DataFrame with a time series.
    """
    start = pd.to_datetime(start_time)

    if interval_type not in ['seconds', 'minutes', 'hours', 'days', 'weeks']:
        raise ValueError(
            "interval_type must be one of 'seconds', 'minutes', 'hours', 'days', 'weeks'")

    time_series = pd.date_range(start=start, periods=num_steps,
                                freq=pd.DateOffset(**{interval_type: interval}))

    # Generate linear trend with noise
    linear_trend = slope * np.arange(num_steps) + intercept
    noise = np.random.randn(num_steps) * noise_level
    data = linear_trend + noise

    df = pd.DataFrame({'timestamp': time_series, 'value': data})

    return df
