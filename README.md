# Pyplot-timeseries

[Matplotlib's Pyplot](https://matplotlib.org/stable/tutorials/pyplot.html) is a staple within the Python packages related to visualizations. While Pyplot is very flexible, it also comes with the added drawback of requiring a lot of boilerplate, especially if your data-type is a time-series or equivalent.

This package has the goal of abstracting away code related to formatting and styling your Pyplot figures for time-series data

## Installation

Using pip

`pip install git+https://github.com/MichaelVerdegaal/pyplot-timeseries.git`

Using [Poetry](https://python-poetry.org/docs/):

`poetry add git+https://github.com/MichaelVerdegaal/pyplot-timeseries.git`

## Features

### Figure and axes helper
This is the main function of the package. It requires mainly a sample of your current x and y values, although it does give you some leeway if one of those is missing.

It returns a pyplot Figure and Axis/Axes object, which you can modify as usual. Secondarily it returns a newly generated range of x-values, which is used so you don't have to modify your existing x-values to fit to the figure.

```python
```python
from plt_ts import plot_ts 
import matplotlib.pyplot as plt
import pandas as pd

sample_x = pd.date_range("2022-01-01", "2022-01-10")
sample_y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fig, ax, new_x_values = plot_ts(x_values=sample_x)
ax.plot(new_x_values, sample_y, label='signal')
plt.title("My plot")
plt.legend()
plt.show()
```

## Custom colormaps
Currently it contains a single custom colormap, 'pong7'. This colormap originated from the frustration of trying to distinguish multiple overlapping lines from each other with the existing colormaps from matplotlib.

See plt_ts.cmaps.py for details on the colors.
