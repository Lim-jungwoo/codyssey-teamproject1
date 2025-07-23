import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def load_data(pkl_file):
    try:
        df: pd.DataFrame = pd.read_pickle(pkl_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    return df


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


def plot_map(df, output_file='map.png'):
    x_max = df['x'].max()
    y_max = df['y'].max()

    fig, ax = plt.subplots(figsize=(x_max, y_max))
    setup_plot(ax, x_max, y_max)

    draw_grid(ax, x_max, y_max)

    draw_structure(df, ax)

    draw_legend(ax)

    plt.tight_layout()
    plt.savefig(output_file)
    print(f"{output_file} 저장 완료")

def main(pkl_file='area_map.pkl'):
    df = load_data(pkl_file)
    if df is None:
        return
    plot_map(df, 'map.png')


if __name__ == "__main__":
    main("area_map.pkl")
