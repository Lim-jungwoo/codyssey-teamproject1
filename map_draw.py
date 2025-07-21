import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform

# 운영체제별 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    mpl.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    mpl.rc('font', family='Malgun Gothic')
else:  # Linux 등
    mpl.rc('font', family='NanumGothic')  # 설치 필요

# 마이너스 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

import sys
if len(sys.argv) < 2:
    print("Usage: python map_draw.py csv_file_name.csv")
    sys.exit(1)

csv_file = sys.argv[1]

df = pd.read_csv(csv_file)
df.columns = df.columns.str.strip()

x_max = df['x'].max()
y_max = df['y'].max()

fig, ax = plt.subplots(figsize=(x_max, y_max))

print(x_max, y_max)

for x in range(1, x_max + 2):
    ax.axvline(x - 0.5, color = 'lightgray', linewidth = 0.5)
for y in range(1, y_max + 2):
    ax.axhline(y - 0.5, color = 'lightgray', linewidth = 0.5)

construction = df[df['ConstructionSite'] > 0]
for _, row in construction.iterrows():
    ax.plot(row['x'], row['y'], marker = 's', color = 'grey', markersize = 30)

non_construction = df[df['ConstructionSite'] == 0]

for _, row in non_construction.iterrows():
    struct = row['struct'].strip()

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
# ax.set_title('지역 구조물 지도')

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker = 's', color = 'grey', label = '건설 현장', markersize = 10),
    Line2D([0], [0], marker = 'o', color = 'brown', label = '아파트/건물', markersize = 10),
    Line2D([0], [0], marker = 's', color = 'green', label = '반달곰 커피', markersize = 10),
    Line2D([0], [0], marker = '^', color = 'green', label = '내 집', markersize = 10)
]
ax.legend(handles = legend_elements, loc = 'upper right', fontsize = 10)

plt.tight_layout()
plt.savefig('map.png')
