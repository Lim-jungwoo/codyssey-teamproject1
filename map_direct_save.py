# graph = dict()
# myhome = [14,2]
# coffee = [3,12]
# coffee = [2,12]

# def main(graph, start_node):
#     visited = list()
#     need_visit = list()

#     need_visit.append(start_node)

#     while need_visit:
#         node = need_visit.pop(0)
#         if node not in visited:
#             visited.append(node)
#             need_visit.extend(graph[node])
    
#     return visited

import pandas as pd
import io
from collections import deque

# --- 1. CSV 데이터 파싱 및 맵(Dictionary) 생성 ---
# Manually recreate the content of the CSV based on your snippet
csv_content = """x,y,ConstructionSite,area, struct
1,1,0,0,
1,2,0,0,
1,3,0,0,
1,4,0,0, Building
1,5,0,0,
1,6,0,0,
1,7,0,0,
2,1,0,0,
3,1,0,0,
3,2,0,0,
2,7,1,0,
2,6,1,0,
2,5,0,0,
2,4,0,0,
2,3,0,0,
2,2,0,0,
4,4,1,0,
4,5,1,0,
4,6,1,0,
4,7,0,0,
5,1,0,0,
5,2,0,0,
5,3,0,0,
5,4,1,0,
4,2,0,0,
4,3,0,0,
4,1,0,0,
3,7,0,0,
3,6,0,0,
3,5,0,0,
3,4,0,0,
3,3,0,0,
6,6,1,0,
6,7,0,0,
7,6,1,0,
7,5,1,0,
7,3,0,0,
7,4,1,0,
7,1,0,0,
7,2,0,0,
6,1,0,0,
6,2,0,0,
6,3,0,0,
6,4,0,0,
6,5,0,0,
8,15,0,1,
8,14,0,1,
8,13,0,1,
8,12,0,1,
8,11,0,1,
8,10,0,1,
8,9,0,1,
7,15,0,1,
7,14,0,1,
7,13,0,1,
7,12,1,1,
7,11,1,1,
7,10,1,1,
7,9,1,1,
7,8,1,1,
6,15,0,1,
6,14,0,1,
6,13,0,1,
6,12,0,1,
6,11,0,1,
6,10,0,1,
6,9,1,1,
6,8,1,1,
5,15,0,1,
5,14,0,1,
5,13,0,1,
5,12,0,1,
5,11,0,1,
5,10,0,1,
5,9,1,1,
5,8,1,1,
1,15,0,1,
1,14,0,1,
1,13,0,1,
1,12,0,1,
1,11,0,1,
1,10,0,1,
1,9,0,1,
1,8,0,1,
2,15,0,1,
2,14,0,1,
2,13,0,1,
2,12,0,1,
2,11,0,1,
2,10,0,1,
2,9,0,1,
2,8,0,1,
3,15,0,1,
3,14,0,1,
3,13,0,1,
3,12,0,1,
3,11,0,1,
3,10,0,1,
3,9,0,1,
3,8,0,1,
4,15,0,1,
4,14,0,1,
4,13,0,1,
4,12,0,1,
4,11,0,1,
4,10,0,1,
4,9,0,1,
4,8,0,1,
9,15,0,2,
9,14,0,2,
9,13,0,2,
9,12,0,2,
9,11,0,2,
9,10,0,2,
9,9,0,2,
9,8,0,2,
10,15,0,2,
10,14,0,2,
10,13,0,2,
10,12,0,2,
10,11,0,2,
10,10,0,2,
10,9,0,2,
10,8,0,2,
11,15,0,2,
11,14,0,2,
11,13,0,2,
11,12,0,2,
11,11,0,2,
11,10,0,2,
11,9,0,2,
11,8,0,2,
12,15,0,2,
12,14,0,2,
12,13,0,2,
12,12,0,2,
12,11,0,2,
12,10,0,2,
12,9,0,2,
12,8,0,2,
13,15,0,2,
13,14,0,2,
13,13,0,2,
13,12,0,2,
13,11,0,2,
13,10,0,2,
13,9,0,2,
13,8,0,2,
14,15,0,2,
14,14,0,2,
14,13,0,2,
14,12,0,2,
14,11,0,2,
14,10,0,2,
14,9,0,2,
14,8,0,2,
15,15,0,2,
15,14,0,2,
15,13,0,2,
15,12,0,2,
15,11,0,2,
15,10,0,2,
15,9,0,2,
15,8,0,2,
8,7,0,2,
8,6,0,2,
8,5,0,2,
8,4,0,2,
8,3,0,2,
8,2,0,2,
8,1,0,2,
9,7,0,2,
9,6,1,2,
9,5,1,2,
9,4,1,2,
9,3,0,2,
9,2,0,2,
9,1,0,2,
10,7,0,2,
10,6,1,2,
10,5,1,2,
10,4,1,2,
10,3,0,2,
10,2,0,2,
10,1,0,2,
11,7,0,2,
11,6,1,2,
11,5,1,2,
11,4,1,2,
11,3,0,2,
11,2,0,2,
11,1,0,2,
12,7,0,2,
12,6,1,2,
12,5,1,2,
12,4,1,2,
12,3,0,2,
12,2,0,2,
12,1,0,2,
13,7,0,2,
13,6,1,2,
13,5,1,2,
13,4,1,2,
13,3,0,2,
13,2,0,2,
13,1,0,2,
14,7,0,2,
14,6,1,2,
14,5,1,2,
14,4,1,2,
14,3,0,2,
14,2,0,2,
14,1,0,2,
15,7,0,2,
15,6,1,2,
15,5,1,2,
15,4,1,2,
15,3,0,2,
15,2,0,2,
15,1,0,2,
"""

# Read the CSV content into a DataFrame
df = pd.read_csv(io.StringIO(csv_content))

# Create a dictionary representing the grid map
# Key: (x, y) tuple
# Value: dictionary of properties including 'ConstructionSite' status
data_map = {}
max_x, max_y = 0, 0
min_x, min_y = float('inf'), float('inf')

for index, row in df.iterrows():
    x = int(row['x'])
    y = int(row['y'])
    
    # Update grid boundaries
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    min_x = min(min_x, x)
    min_y = min(min_y, y)

    if (x, y) not in data_map:
        data_map[(x, y)] = {}
        
    data_map[(x, y)]['ConstructionSite'] = bool(row['ConstructionSite']) 
    
    # Initialize other specific structure types (if they were present in 'struct' column)
    data_map[(x, y)]['Apartment'] = 0
    data_map[(x, y)]['Building'] = 0
    data_map[(x, y)]['MyHome'] = 0 # Placeholder for MyHome if it appears in 'struct'
    data_map[(x, y)]['BandalgomCoffee'] = 0 # Placeholder for BandalgomCoffee if it appears in 'struct'

    if 'struct' in row and pd.notna(row['struct']):
        struct_value = str(row['struct']).strip()
        if struct_value == 'Apartment':
            data_map[(x, y)]['Apartment'] = 1
        elif struct_value == 'Building':
            data_map[(x, y)]['Building'] = 1
        # If 'MyHome' or 'BandalgomCoffee' were in 'struct' column, they would be handled here
        # e.g., elif struct_value == 'MyHome': data_map[(x,y)]['MyHome'] = 1

# --- 2. 시작, 도착 지점 및 장애물 정의 ---
# As 'MyHome' and 'BandalgomCoffee' were not explicitly found in 'struct' column of the snippet,
# we'll use the min/max coordinates as arbitrary start/end points for demonstration.
# You can change these if you know the exact coordinates for MyHome and BandalgomCoffee.

start_node = (14,2) # Assuming MyHome is at the smallest x,y coordinate
end_node = (3,12)   # Assuming BandalgomCoffee is at the largest x,y coordinate

# Ensure start/end nodes are valid and not construction sites
# If the assumed start/end points are obstacles, try to find the nearest non-obstacle.
def find_alternative_node(target_node, data_map, obstacles, min_x, max_x, min_y, max_y, is_start=True):
    if target_node not in data_map or data_map[target_node]['ConstructionSite']:
        print(f"Warning: {'Start' if is_start else 'End'} node {target_node} is a ConstructionSite or not in map. Attempting to find an alternative.")
        search_range_x = range(min_x, max_x + 1) if is_start else range(max_x, min_x - 1, -1)
        search_range_y = range(min_y, max_y + 1) if is_start else range(max_y, min_y - 1, -1)

        for r_x in search_range_x:
            for r_y in search_range_y:
                candidate_node = (r_x, r_y)
                if candidate_node in data_map and not data_map[candidate_node]['ConstructionSite']:
                    print(f"Using alternative {'start' if is_start else 'end'} node: {candidate_node}")
                    return candidate_node
    return target_node # Return original if it's valid or no alternative found

start_node = find_alternative_node(start_node, data_map, None, min_x, max_x, min_y, max_y, is_start=True)
end_node = find_alternative_node(end_node, data_map, None, min_x, max_x, min_y, max_y, is_start=False)

# --- 3. 최단 경로 탐색 (BFS) 함수 구현 ---
# Your provided 'main' function is a basic graph traversal.
# For the 'shortest path', we need to track the path taken to reach each node.
# Breadth-First Search (BFS) is ideal for unweighted shortest paths.

def find_shortest_path_bfs(start, end, data_map, min_x_bound, max_x_bound, min_y_bound, max_y_bound):
    """
    BFS를 사용하여 시작 노드에서 끝 노드까지의 최단 경로를 찾습니다.
    건설 현장(ConstructionSite)은 지나갈 수 없습니다.
    """
    if start is None or end is None:
        print("Error: Start or end node is invalid or could not be determined.")
        return None

    # 큐: (현재 노드, 현재 노드까지의 경로) 튜플을 저장
    queue = deque([(start, [start])])
    # 방문한 노드를 추적하여 무한 루프를 방지하고 최단 경로를 보장
    visited = {start}
    
    # 상하좌우 이동 정의 (대각선 이동 없음)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # (dx, dy)

    while queue:
        current_node, path = queue.popleft() # 큐의 가장 왼쪽 요소 (가장 먼저 추가된 노드) 가져오기

        # 현재 노드가 도착 노드라면, 경로 반환
        if current_node == end:
            return path

        # 현재 노드에서 이동 가능한 다음 노드들을 탐색
        for dx, dy in moves:
            next_x, next_y = current_node[0] + dx, current_node[1] + dy
            next_node = (next_x, next_y)

            # 1. 그리드 경계 내에 있는지 확인
            if not (min_x_bound <= next_x <= max_x_bound and min_y_bound <= next_y <= max_y_bound):
                continue

            # 2. 다음 노드가 data_map에 존재하는지 확인 (CSV에 없는 좌표일 수 있음)
            if next_node not in data_map:
                continue

            # 3. 다음 노드가 건설 현장(장애물)인지 확인
            if data_map[next_node]['ConstructionSite']:
                continue

            # 4. 이미 방문한 노드인지 확인
            if next_node not in visited:
                visited.add(next_node) # 방문 처리
                # 큐에 다음 노드와 그 노드까지의 새로운 경로 추가
                queue.append((next_node, path + [next_node]))
    
    return None # 경로를 찾지 못한 경우

# --- 4. 최단 경로 계산 및 결과 출력 ---
if start_node and end_node:
    shortest_path = find_shortest_path_bfs(
        start_node, end_node, data_map, min_x, max_x, min_y, max_y
    )

    if shortest_path:
        print(f"MyHome (시작점) {start_node} 에서 BandalgomCoffee (도착점) {end_node} 까지의 최단 경로:")
        print(shortest_path)
        print(f"경로 길이: {len(shortest_path) - 1} 스텝") # 시작 노드 제외한 스텝 수
    else:
        print(f"MyHome {start_node} 에서 BandalgomCoffee {end_node} 까지의 경로를 찾을 수 없습니다.")
else:
    print("시작점 또는 도착점을 유효하게 설정할 수 없어 경로를 계산할 수 없습니다.")
