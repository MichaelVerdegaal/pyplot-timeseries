"""
This file contains custom matplotlib colormaps.
"""
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

# pylint: disable=pointless-string-statement
"""
This cmap originated from the need to plot multiple lines on the same plot
that frequently intersect. These colors have been chosen to have a high contrast
between each other, as with the standard matplotlib cmaps the lines
are often too hard to distinguish from each other.
"""
colors_pong7 = [
    "#1f77b4",  # tab10 blue
    "#d68d04",  # Ochre orange
    "#de182c",  # Lava red
    "#2c8a0f",  # Mint green
    "#ff0fd7",  # Fuchsia pink
    "#04d68d",  # Sky blue
    "#563d61",  # Plum purple
]
pong_7 = ListedColormap(colors_pong7, name="pong7", N=len(colors_pong7))


def register_cmaps() -> None:
    """Register the custom colormaps"""
    for cmap in [pong_7]:
        # check if cmap is already registered
        if cmap.name not in plt.colormaps():
            matplotlib.colormaps.register(cmap)
