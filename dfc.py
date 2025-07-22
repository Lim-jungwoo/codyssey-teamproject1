import pandas as pd
from collections import deque
import io

# Tool call to fetch the CSV content
# Assuming 'dourses.csv' is the file name and it's accessible via content_fetcher
try:
    csv_content = content_fetcher.fetch(
        query="dourses.csv",
        source_references=[content_fetcher.SourceReference(id="uploaded:dourses.csv", type="file")]
    )
    df = pd.read_csv(io.StringIO(csv_content))
except Exception as e:
    print(f"Error fetching or reading CSV: {e}")
    exit()

def find_shortest_path(grid, start, end):
    """
    Finds the shortest path from start to end in a grid using BFS.

    Args:
        grid (dict): A dictionary representing the grid, where keys are (x, y)
                     tuples and values are dictionaries containing 'passable' status.
        start (tuple): The (x, y) coordinates of the starting point.
        end (tuple): The (x, y) coordinates of the ending point.

    Returns:
        list: A list of (x, y) tuples representing the shortest path,
              or None if no path is found.
    """
    # Determine grid dimensions from the available coordinates
    # This ensures the grid bounds are correctly set based on the data
    max_x = max(coord[0] for coord in grid.keys()) if grid else 0
    max_y = max(coord[1] for coord in grid.keys()) if grid else 0
    rows = max_x + 1
    cols = max_y + 1

    # Queue for BFS: stores (current_node, path_so_far)
    queue = deque([(start, [start])])
    # Set to keep track of visited nodes to avoid cycles and redundant processing
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        # If the current node is the end point, we found the shortest path
        if (r, c) == end:
            return path

        # Define possible movements: up, down, left, right
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc # Calculate coordinates of the next node
            next_node = (nr, nc)

            # Check if the next node is:
            # 1. Within the grid boundaries
            # 2. An existing coordinate in our grid data
            # 3. Passable (not a construction site)
            # 4. Not yet visited
            if 0 <= nr < rows and 0 <= nc < cols and next_node in grid and \
               grid[next_node]['passable'] and next_node not in visited:
                visited.add(next_node) # Mark as visited
                # Add the next node and its path to the queue
                queue.append((next_node, path + [next_node]))

    # If the queue becomes empty and the end point was not reached, no path exists
    return None

# Create a grid representation from the DataFrame
grid = {}
for index, row in df.iterrows():
    x, y = int(row['x']), int(row['y'])
    is_construction_site = row['ConstructionSite'] == 1
    grid[(x, y)] = {'passable': not is_construction_site}

# Define start and end points directly from the CSV data
# 'MyHome' is at (14, 2)
start_point = (14, 2)
# 'BandalgomCoffee' is at (2, 12) and (3, 12). We'll use (2, 12) as the primary target.
end_point = (2, 12)

# Validate start and end points
if start_point not in grid:
    print(f"Error: Start point {start_point} is not on the map.")
    exit()
if not grid[start_point]['passable']:
    print(f"Error: Start point {start_point} is on a construction site and is impassable.")
    exit()
if end_point not in grid:
    print(f"Error: End point {end_point} is not on the map.")
    exit()
if not grid[end_point]['passable']:
    print(f"Error: End point {end_point} is on a construction site and is impassable.")
    exit()

# Find the shortest path
shortest_path = find_shortest_path(grid, start_point, end_point)

# Output the result
if shortest_path:
    print("\nShortest route found:")
    for i, (x, y) in enumerate(shortest_path):
        print(f"Step {i+1}: ({x}, {y})")
    print(f"\nTotal steps: {len(shortest_path) - 1}") # Subtract 1 because path includes start and end
else:
    print(f"\nNo path found from {start_point} to {end_point}, or the destination is impassable.")
