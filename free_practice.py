import fastf1 as ff1
from fastf1 import plotting
import matplotlib.ticker as ticker
from matplotlib import  pyplot as plt
import numpy as np
import pandas as pd

# define a function to format the y-axis tick labels
def format_time(y, pos):
    minutes = int(y // 60)
    seconds = int(y % 60)
    millis = int((y % 1) * 1000)
    return f"{minutes:02d}:{seconds:02d}:{millis:03d}"
# enable plotting settup in fast f1
ff1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)
# enable the cache by providing the name of the chache folder
ff1.Cache.enable_cache('..\cache')
# free practice data
fp_1 = ff1.get_session(2023,'Azerbaijan','FP1')
fp_1.load()
fp1_laps = fp_1.laps
# sprint shoot out data
sprint_shootout = ff1.get_session(2023,'Azerbaijan','SS')
sprint_shootout.load()
ss_laps = sprint_shootout.laps
# sprint race data
sprint_race = ff1.get_session(2023,'Azerbaijan','S')
sprint_race.load()
sr_laps = sprint_race.laps
# Qualifying data
Quali = ff1.get_session(2023,'Azerbaijan','Q')
Quali.load()
Quali_laps = Quali.laps
# Race data
Race = ff1.get_session(2023,'Azerbaijan','R')
Race.load()
Race_laps = Race.laps

# create a dictionary to store lap times for each driver from session datas
driver_laptimes = {"FP1": {}, "Qualifying": {},"Sprint_Shoot":{},"Sprint": {},"Race":{}}
# get unique drivers in fp1_laps
drivers = pd.unique(fp1_laps['Driver'])

# populate driver_teams with the corresponding team name for each driver
driver_teams = []
for driver in drivers:
    team_name = fp1_laps.loc[fp1_laps['Driver'] == driver, 'Team'].unique()[0]
    driver_teams.append(team_name)

# loop through each driver and collect their lap times in various sessions

for driver in drivers:
    driver_laptimes["FP1"][driver] = fp1_laps.pick_driver(driver)["LapTime"].dt.total_seconds()
    driver_laptimes["Qualifying"][driver] = Quali_laps.pick_driver(driver)["LapTime"].dt.total_seconds()
    driver_laptimes["Sprint_Shoot"][driver] = ss_laps.pick_driver(driver)["LapTime"].dt.total_seconds()
    driver_laptimes["Sprint"][driver] = sr_laps.pick_driver(driver)["LapTime"].dt.total_seconds()
    driver_laptimes["Race"][driver] = Race_laps.pick_driver(driver)["LapTime"].dt.total_seconds()
print(driver_laptimes)

# collect all laptimes except for the Race event
laptimes = {}
sessions = ["FP1","Qualifying","Sprint_Shoot","Sprint"]
for driver in drivers:
    laptimes[driver] = []
    for session in sessions:
        laptimes[driver].extend(driver_laptimes[session][driver])
# clean data
laptimes_clean = {}
for driver in drivers:
    data = laptimes[driver]
    laptimes_clean[driver] = []
    for i in range(len(laptimes[driver])):
        if np.isnan(data[i]):
            continue
        else:
            laptimes_clean[driver].append(data[i])

# race event laptimes
race_laptimes = {}
for driver in drivers:
    race_laptimes[driver] = driver_laptimes["Race"][driver]
# clean race laptime data
race_laptimes_clean = {}
for driver in drivers:
    data = race_laptimes[driver]
    race_laptimes_clean[driver] = []
    for time in data:
        if np.isnan(time):
            continue
        else:
            race_laptimes_clean[driver].append(time)


## Plotting data
fig,(ax1,ax2) = plt.subplots(nrows=2, ncols=1)
# plot box plot with mean and standard deviation for each driver
bp = ax1.boxplot(laptimes_clean.values(),patch_artist = True,labels=drivers, showmeans=True, meanline=True)
bp2 = ax2.boxplot(race_laptimes_clean.values(),patch_artist = True,labels=drivers, showmeans=True, meanline=True)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))

# get team colors for each driver
colors = []
for team in driver_teams:
    colors.append(ff1.plotting.team_color(team))
print(colors)

for i in range(np.size(drivers)):
    colors.append(ff1.plotting.driver_color(drivers[i]))
for patch,color in zip(bp['boxes'],colors):
    patch.set_facecolor(color)

ax2.set_xlabel('Drivers')
plt.suptitle(f"{Race.event['EventName']} {Race.event.year} \n"
             f"FP1 Qualifying Spring average pace")
ax1.set_title("Average pace distribution during FP1,Quali,Sprints")
ax2.set_title("Pace distribution during race")
# plot_filename = plt_title.replace(" "," ")+".png"
#
# plt.savefig(plot_filename, dpi=300)

plt.show()
