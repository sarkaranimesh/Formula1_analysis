# Import libraries
import fastf1 as ff1
import matplotlib.pyplot as plt

# Enable cache (optional but recommended)
import pandas as pd

ff1.Cache.enable_cache('cache')

# Load session data
session = ff1.get_session(2023, 'Azerbaijan', 'R')
session.load()
drivers = ["VER","PER","LEC","ALO","RUS"]
# Pick drivers
driver1 = session.laps.pick_driver('VER')
driver2 = session.laps.pick_driver('PER')
driver3 = session.laps.pick_driver('LEC')
driver4 = session.laps.pick_driver('ALO')
driver5 = session.laps.pick_driver('RUS')
# get all compound for the driver
driver1_compound = pd.unique(driver1['Compound'])
driver2_compound = pd.unique(driver2['Compound'])
driver3_compound = pd.unique(driver3['Compound'])
driver4_compound = pd.unique(driver4['Compound'])
driver5_compound = pd.unique(driver5['Compound'])



# Group laps by tyre compound
driver1_tyres = driver1.groupby('Compound')
driver2_tyres = driver2.groupby('Compound')
driver3_tyres = driver3.groupby('Compound')
driver4_tyres = driver4.groupby('Compound')
driver5_tyres = driver5.groupby('Compound')



# Get maximum laps driven in each compound
driver1_compound_max = {}
for cm in driver1_compound:
    a = driver1_tyres.get_group(cm)
    driver1_compound_max[cm] = a.count()['Compound']
print(driver1_compound_max)

driver2_compound_max = {}
for cm in driver2_compound:
    a = driver2_tyres.get_group(cm)
    driver2_compound_max[cm] = a.count()['Compound']
print(driver2_compound_max)

driver3_compound_max = {}
for cm in driver3_compound:
    a = driver3_tyres.get_group(cm)
    driver3_compound_max[cm] = a.count()['Compound']
print(driver3_compound_max)

driver4_compound_max = {}
for cm in driver4_compound:
    a = driver4_tyres.get_group(cm)
    driver4_compound_max[cm] = a.count()['Compound']
print(driver4_compound_max)

driver5_compound_max = {}
for cm in driver5_compound:
    a = driver5_tyres.get_group(cm)
    driver5_compound_max[cm] = a.count()['Compound']
print(driver5_compound_max)

# plot
hard_laps = [driver1_compound_max['HARD'],driver2_compound_max['HARD'],driver3_compound_max['HARD'],driver4_compound_max['HARD'],driver5_compound_max['HARD'],]
medium_laps = [driver1_compound_max['MEDIUM'],driver2_compound_max['MEDIUM'],driver2_compound_max['MEDIUM'],driver4_compound_max['MEDIUM'],driver5_compound_max['MEDIUM']]
soft_laps= [0,0,0,0,driver5_compound_max['SOFT']]
# Set the width of the bars
bar_width = 0.1
# Set the x-coordinates for each driver
x1 = [i for i in range(len(drivers))]
x2 = [i + bar_width for i in x1]
x3 = [i + bar_width for i in x2]

# Plot the bars for each tyre type
fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.set_facecolor('black')

bars1=ax.bar(x1, hard_laps, width=bar_width, label="Hard",color = 'white')
bars2=ax.bar(x2, medium_laps, width=bar_width, label="Medium",color = 'yellow')
bars3=ax.bar(x3, soft_laps, width=bar_width, label="Soft",color = 'red')

# Add some details to the plot
ax.tick_params(axis='both', which='major', size=10, width=3, labelsize=15, color='white', labelcolor='white')
ax.spines['left'].set_linewidth(3)
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_linewidth(3)
ax.spines['bottom'].set_color('white')

plt.xlabel("Drivers",fontsize=18, fontweight='bold', color='white')
plt.ylabel("Number of laps",fontsize=18, fontweight='bold', color='white')
plt.title("Number of laps by drivers and tyre types",fontsize=20, fontweight='bold', color='white')
plt.xticks([i + bar_width for i in range(len(drivers))], drivers)
plt.legend()

# Add text annotations for each bar height
for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, height, ha="center", va="bottom", color = 'white')

for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, height, ha="center", va="bottom", color = 'white')

for bar in bars3:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, height, ha="center", va="bottom", color = 'white')
# Show the plot
plt.show()


