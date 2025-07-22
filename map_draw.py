import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_pickle('merged.pkl')

# 그래프 구성
data.columns = data.columns.str.strip()

max_x = max(data['x'])
max_y = max(data['y'])

fig, ax = plt.subplots(figsize=(max_x, max_y))

ax.set_xticks(range(1, max_x + 1))
ax.set_yticks(range(1, max_y + 1))
ax.grid(True, which='both', linestyle='-', linewidth=0.5)

ax.set_xlim(left=0.5, right=max_x + 0.5)
ax.set_ylim(bottom=0.5, top=max_y + 0.5)

ax.invert_yaxis()
ax.set_aspect('equal', adjustable='box')

# 각 건물 좌표 수집
data['struct'] = data['struct'].fillna('').str.strip()
buildings = data[(data['struct'] == 'Apartment') | (data['struct'] == 'Building')]
bandalgoms = data[data['struct'] == 'BandalgomCoffee']
my_home = data[data['struct'] == 'MyHome']
construction_sites = data[data['ConstructionSite'] == 1]

# 좌표를 그래프에 표시
ax.scatter(
    x=buildings['x'],
    y=buildings['y'],
    s=200,
    c='brown',
    marker='o',
    label='Apartment & Building',
)

ax.scatter(
    x=bandalgoms['x'],
    y=bandalgoms['y'],
    s=200,
    c='green',
    marker='s',
    label='Bandalgom Coffee',
)

ax.scatter(
    x=my_home['x'],
    y=my_home['y'],
    s=200,
    c='green',
    marker='^',
    label='My Home',
)


ax.scatter(
    x=construction_sites['x'],
    y=construction_sites['y'],
    s=200,
    c='grey',
    marker='s',
    label='Construction Site',
)

# 범례
ax.legend()

# plt.show()
plt.tight_layout()
plt.savefig('map.png')
