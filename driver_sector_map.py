##############################################################################
# Import FastF1 and load the data

import fastf1

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np


fastf1.Cache.enable_cache('cache')  # replace with your cache directory

session = fastf1.get_session(2023, 'Azerbaijan', 'R')
session.load()

# Select the two drivers you want to compare
driver1 = session.laps.pick_fastest(driver = 'VER')
driver2 = session.laps.pick_fastest(driver = 'PER')

# Get the telemetry data for both drivers
tel1 = driver1.get_telemetry()
tel2 = driver2.get_telementry()

# Calculate the sector times for both drivers
sector_times1 = fastf1.utils.calc_sector_times(tel1)
sector_times2 = fastf1.utils.calc_sector_times(tel2)

# Find the fastest sector for each lap for both drivers
fastest_sectors1 = np.argmin(sector_times1, axis=1)
fastest_sectors2 = np.argmin(sector_times2, axis=1)

# Create a list of colors based on the fastest sector for each lap for both drivers
colors1 = [cm.get_cmap('Paired')(fastest_sectors1[i] / 3) for i in range(len(fastest_sectors1))]
colors2 = [cm.get_cmap('Paired')(fastest_sectors2[i] / 3) for i in range(len(fastest_sectors2))]

# Prepare the data for plotting by converting it to the appropriate numpy data types
x1 = np.array(tel1['X'].values)
y1 = np.array(tel1['Y'].values)

points1 = np.array([x1, y1]).T.reshape(-1, 1, 2)
segments1 = np.concatenate([points1[:-1], points1[1:]], axis=1)

x2 = np.array(tel2['X'].values)
y2 = np.array(tel2['Y'].values)

points2 = np.array([x2, y2]).T.reshape(-1, 1, 2)
segments2 = np.concatenate([points2[:-1], points2[1:]], axis=1)

# Create line collections for both drivers with different colors for each sector
lc_driver1 = LineCollection(segments1, colors=colors1, linewidths=4)
lc_driver2 = LineCollection(segments2, colors=colors2, linewidths=4)

# Create the plot
fig, ax = plt.subplots()
ax.add_collection(lc_driver1)
ax.add_collection(lc_driver2)
ax.axis('equal')
ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

title = plt.suptitle(
    f"Fastest Sector Visualization\n"
    f"{driver1} (blue) vs {driver2} (orange) - {session.event['EventName']} {session.event.year}"
)

plt.show()
