import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
if platform.system() == 'Darwin':
    mpl.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    mpl.rc('font', family='Malgun Gothic')
else:
    mpl.rc('font', family='NanumGothic')
mpl.rcParams['axes.unicode_minus'] = False

import sys
if len(sys.argv) < 2:
    print('Usage: python map_direct_save.py [pkl_file].pkl')
    sys.exit(1)

pkl_file = sys.argv[1]

df = pd.read_pickle(pkl_file)
df.columns = df.columns.str.strip()

x_max = df['x'].max()
y_max = df['y'].max()
grid = [[0 for _ in range(x_max + 1)] for _ in range(y_max + 1)]

start = None
end = set()

for _, row in df.iterrows():
    x = int(row['x'])
    y = int(row['y'])
    if row['ConstructionSite'] > 0:
        grid[y][x] = 1
    struct = row['struct'].strip() if pd.notna(row['struct']) else 'Nothing'
    if struct == 'MyHome':
        start = (x, y)
    elif struct == 'BandalgomCoffee':
        end.add((x, y))

if not start or not end:
    print('집이나 반달곰 커피숍이 없습니다.')
    sys.exit(1)

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
visited = set()
prev = {}

from collections import deque
q = deque()
q.append(start)
visited.add(start)

fast_end = None

while q:
    cur = q.popleft()
    if cur in end:
        fast_end = cur
        break
    for dx, dy in dirs:
        nx, ny = cur[0] + dx, cur[1] + dy
        if 0 < nx <= x_max and 0 < ny <= y_max and (nx, ny) not in visited and grid[ny][nx] == 0:
            visited.add((nx, ny))
            prev[(nx, ny)] = cur
            q.append((nx, ny))

if not fast_end:
    print('경로를 찾을 수 없습니다.')
    sys.exit(1)

path = []
while cur != start:
    path.append(cur)
    cur = prev.get(cur)

path.append(start)
path.reverse()

path_df = pd.DataFrame(path, columns=['x', 'y'])
path_df.to_csv('home_to_cafe.csv', index = False)

fig, ax = plt.subplots(figsize = (x_max, y_max))

for x in range(1, x_max + 2):
    ax.axvline(x - 0.5, color = 'lightgray', linewidth = 0.5)
for y in range(1, y_max + 2):
    ax.axhline(y - 0.5, color = 'lightgray', linewidth = 0.5)

construction = df[df['ConstructionSite'] > 0]
for _, row in construction.iterrows():
    ax.plot(row['x'], row['y'], marker = 's', color = 'grey', markersize = 30)

non_construction = df[df['ConstructionSite'] == 0]

for _, row in non_construction.iterrows():
    struct = row['struct'].strip() if pd.notna(row['struct']) else 'Nothing'

    if struct in ['Apartment', 'Building']:
        ax.plot(row['x'], row['y'], marker = 'o', color = 'brown', markersize = 30)
    elif struct == 'BandalgomCoffee':
        ax.plot(row['x'], row['y'], marker = 's', color = 'green', markersize = 30)
    elif struct == 'MyHome':
        ax.plot(row['x'], row['y'], marker = '^', color = 'green', markersize = 30)

ax.set_xlim(0.5, x_max + 0.5)
ax.set_ylim(0.5, y_max + 0.5)
ax.set_aspect('equal')
ax.invert_yaxis()
ax.set_xticks(range(1, x_max + 1))
ax.set_yticks(range(1, y_max + 1))

path_for_plot = [(x, y) for (x, y) in path]
xs, ys = zip(*path_for_plot)
ax.plot(xs, ys, '-', color='red', linewidth=2, label='최단 경로')

plt.tight_layout()
plt.savefig('map_final.png')