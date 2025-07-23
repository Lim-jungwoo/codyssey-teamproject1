import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D


def load_data(pkl_file: str):
    df: pd.DataFrame = pd.read_pickle(pkl_file)
    df.columns = df.columns.str.strip()
    return df


def extract_map_info(df: pd.DataFrame):
    x_max = df['x'].max()
    y_max = df['y'].max()
    construction_site = set()
    start = None
    end = set()
    for _, row in df.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        if row['ConstructionSite'] > 0:
            construction_site.add((x, y))
        struct = row['struct'].strip() if pd.notna(
            row['struct']) else 'Nothing'
        if struct == 'MyHome':
            start = (x, y)
        elif struct == 'BandalgomCoffee':
            end.add((x, y))
    return construction_site, start, end, x_max, y_max


def bfs(construction_site, start, end, x_max, y_max):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = set()
    prev = {}
    q = []
    q.append(start)
    visited.add(start)
    fast_end = None
    while q:
        cur = q.pop(0)
        if cur in end:
            fast_end = cur
            break
        for dx, dy in dirs:
            nx, ny = cur[0] + dx, cur[1] + dy
            if 0 < nx <= x_max and 0 < ny <= y_max and (nx, ny) not in visited and (nx, ny) not in construction_site:
                visited.add((nx, ny))
                prev[(nx, ny)] = cur
                q.append((nx, ny))
    if not fast_end:
        return None, None
    path = []
    cur = fast_end
    while cur != start:
        path.append(cur)
        cur = prev.get(cur)
    path.append(start)
    path.reverse()
    return path, fast_end


def save_path(path):
    path_df = pd.DataFrame(path, columns=['x', 'y'])
    path_df.to_csv('home_to_cafe.csv', index=False)


def setup_plot(ax: plt.Axes, x_max, y_max):
    ax.set_xlim(0.5, x_max + 0.5)
    ax.set_ylim(0.5, y_max + 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xticks(range(1, x_max + 1))
    ax.set_yticks(range(1, y_max + 1))


def draw_grid(ax: plt.Axes, x_max, y_max):
    for x in range(1, x_max + 2):
        ax.axvline(x - 0.5, color='lightgray', linewidth=0.5)
    for y in range(1, y_max + 2):
        ax.axhline(y - 0.5, color='lightgray', linewidth=0.5)


def draw_structure(df: pd.DataFrame, ax: plt.Axes):
    construction = df[df['ConstructionSite'] > 0]
    ax.scatter(
        construction['x'],
        construction['y'],
        marker='s',
        color='grey',
        s=900,
    )

    non_construction = df[df['ConstructionSite'] == 0]
    for _, row in non_construction.iterrows():
        struct = row['struct'].strip() if pd.notna(
            row['struct']) else 'Nothing'

        if struct in ['Apartment', 'Building']:
            ax.plot(row['x'], row['y'], marker='o', color='brown',
                    markersize=30)
        elif struct == 'BandalgomCoffee':
            ax.plot(row['x'], row['y'], marker='s', color='green',
                    markersize=30)
        elif struct == 'MyHome':
            ax.plot(row['x'], row['y'], marker='^',
                    color='green', markersize=30)


def draw_legend(ax: plt.Axes):
    legend_elements = [
        Line2D([0], [0], marker='s', color='grey',
               label='Construction Site', markersize=10),
        Line2D([0], [0], marker='o', color='brown',
               label='Apartment/Building', markersize=10),
        Line2D([0], [0], marker='s', color='green',
               label='BandalgomCoffee', markersize=10),
        Line2D([0], [0], marker='^', color='green',
               label='MyHome', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)


def draw_path(ax: plt.Axes, path):
    xs, ys = zip(*path)
    ax.plot(xs, ys, '-', color='red', linewidth=2)


def plot_map(df: pd.DataFrame, path, x_max, y_max):
    fig, ax = plt.subplots(figsize=(x_max, y_max))

    setup_plot(ax, x_max, y_max)

    draw_grid(ax, x_max, y_max)

    draw_structure(df, ax)

    draw_legend(ax)

    if path:
        draw_path(ax, path)

    plt.tight_layout()
    plt.savefig('map_final.png')


def main(pkl_file="area_map.pkl"):
    df = load_data(pkl_file)
    try:
        grid, start, end, x_max, y_max = extract_map_info(df)
        if not start or not end:
            raise Exception('집이나 반달곰 커피숍이 없습니다.')

        path, fast_end = bfs(grid, start, end, x_max, y_max)
        if not path:
            raise Exception('경로를 찾을 수 없습니다.')
        print(f'가장 가까운 반달곰 커피숍 위치: {fast_end}')

        save_path(path)

        plot_map(df, path, x_max, y_max)

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main("area_map.pkl")
