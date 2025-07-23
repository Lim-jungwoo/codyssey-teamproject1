import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_pickle('merged.pkl')

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

buildings = data[(data['struct'] == 'Apartment') | (data['struct'] == 'Building')]
bandalgoms = data[data['struct'] == 'BandalgomCoffee']
my_home = data[data['struct'] == 'MyHome']
construction_sites = data[data['ConstructionSite'] == 1]
const_sites = set(zip(construction_sites['x'], construction_sites['y']))


def bfs(df, start, destination, max_loc, const_sites):
    visited = set()
    queue = list()

    queue.append((start, [start]))
    visited.add(start)

    max_x, max_y = max_loc

    while queue:
        (x, y), route = queue.pop(0)

        if (x, y) in destination:
            return route

        for dx, dy in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if (
                1 <= nx <= max_x
                and 1 <= ny <= max_y
                and neighbor not in visited
                and neighbor not in const_sites
            ):
                visited.add(neighbor)
                queue.append((neighbor, route + [neighbor]))

    return None


my_home = data[data['struct'] == 'MyHome'].iloc[0]
start = my_home['x'], my_home['y']
max_loc = max(data['x']), max(data['y'])

bandalgoms = data[data['struct'] == 'BandalgomCoffee']
destinations = set()
for _, row in bandalgoms.iterrows():
    destinations.add((row['x'], row['y']))
route = bfs(
    df=data,
    start=start,
    destination=destinations,
    max_loc=max_loc,
    const_sites=const_sites,
)

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

if route is not None:
    route_x, route_y = zip(*route)
    plt.plot(route_x, route_y, color='red', linewidth=3, label='route')

ax.legend()
plt.tight_layout()
plt.savefig('map_final.png')

plt.show()
