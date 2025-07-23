import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.axes import Axes
from matplotlib.lines import Line2D


def load_data(pkl_file: str):
    try:
        df: pd.DataFrame = pd.read_pickle(pkl_file)
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    return df


def extract_map_info(df: pd.DataFrame):
    x_max: int = df['x'].max()
    y_max: int = df['y'].max()
    construction_site = set()
    start = None
    end = set()

    for _, row in df.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        if row['ConstructionSite'] > 0:
            construction_site.add((x, y))

        struct: str = row['struct']
        if struct == 'MyHome':
            start = (x, y)
        elif struct == 'BandalgomCoffee':
            end.add((x, y))

    return construction_site, start, end, x_max, y_max


def bfs(construction_site: set, start: tuple, end: set, x_max: int, y_max: int):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = set()
    visited.add(start)
    prev = {}
    q = []
    q.append(start)
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


def save_path(path: list):
    path_df = pd.DataFrame(path, columns=['x', 'y'])
    path_df.to_csv('home_to_cafe.csv', index=False)


def setup_plot(ax: Axes, x_max: int, y_max: int):
    ax.set_xlim(0.5, x_max + 0.5)
    ax.set_ylim(0.5, y_max + 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xticks(range(1, x_max + 1))
    ax.set_yticks(range(1, y_max + 1))


def draw_grid(ax: Axes, x_max: int, y_max: int):
    for x in range(1, x_max + 2):
        ax.axvline(x - 0.5, color='lightgray', linewidth=0.5)
    for y in range(1, y_max + 2):
        ax.axhline(y - 0.5, color='lightgray', linewidth=0.5)


def draw_structure(df: pd.DataFrame, ax: Axes):
    non_construction: pd.DataFrame = None
    has_construction_site = df.get('ConstructionSite')
    if has_construction_site is not None:
        construction = df[df['ConstructionSite'] > 0]
        ax.scatter(
            construction['x'],
            construction['y'],
            marker='s',
            color='grey',
            s=900,
        )
        non_construction = df[df['ConstructionSite'] == 0]
    else:
        non_construction = df

    for _, row in non_construction.iterrows():
        struct = row['struct']

        if struct in ['Apartment', 'Building']:
            ax.plot(row['x'], row['y'], marker='o', color='brown',
                    markersize=30)
        elif struct == 'BandalgomCoffee':
            ax.plot(row['x'], row['y'], marker='s', color='green',
                    markersize=30)
        elif struct == 'MyHome':
            ax.plot(row['x'], row['y'], marker='^',
                    color='green', markersize=30)


def draw_legend(ax: Axes):
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


def draw_path(ax: Axes, path: list):
    xs, ys = zip(*path)
    ax.plot(xs, ys, '-', color='red', linewidth=2)


def plot_map(df: pd.DataFrame, path: list, output_file: str = 'map_final.png'):
    x_max = df['x'].max()
    y_max = df['y'].max()

    fig, ax = plt.subplots(figsize=(x_max, y_max))

    setup_plot(ax, x_max, y_max)

    draw_grid(ax, x_max, y_max)

    draw_structure(df, ax)

    draw_legend(ax)

    if path:
        draw_path(ax, path)

    plt.tight_layout()
    plt.savefig(output_file)
    print(f"{output_file} 저장 완료")


def main(pkl_file: str = "area_map.pkl"):
    df = load_data(pkl_file)
    if df is None:
        return

    try:
        grid, start, end, x_max, y_max = extract_map_info(df)
        if not start or not end:
            raise Exception('집이나 반달곰 커피숍이 없습니다.')

        path, fast_end = bfs(grid, start, end, x_max, y_max)
        if not path:
            raise Exception('경로를 찾을 수 없습니다.')
        print(f'가장 가까운 반달곰 커피숍 위치: {fast_end}')

        save_path(path)

        plot_map(df, path, output_file='map_final.png')

    except Exception as e:
        print(f"오류 발생: {e}")
        return


if __name__ == "__main__":
    main("area_map.pkl")
