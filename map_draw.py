#미 완성

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv('dourses.csv')

# Rename the column ' struct' to 'struct' to ensure consistency.
df.rename(columns={' struct': 'struct'}, inplace=True)

# Fill NaN values in 'struct' column with 'Unknown' to handle missing data gracefully.
df['struct'].fillna('Unknown', inplace=True)

# Determine the maximum x and y coordinates to set plot boundaries.
max_x = df['x'].max()
max_y = df['y'].max()

# Create the plot
plt.figure(figsize=(10, 10))

# Define colors and markers for different structure types.
colors = {
    'Building': 'brown',
    'Apartment': 'brown',
    'Asiatic black bear coffee': 'green',
    'My house': 'green',
    'ConstructionSite': 'gray',
    'Unknown': 'lightgray'
}

markers = {
    'Building': 'o',
    'Apartment': 'o',
    'Asiatic black bear coffee': 's',
    'My house': '^',
    'ConstructionSite': 's',
    'Unknown': 'o'
}


df['plot_type'] = df.apply(lambda row: 'ConstructionSite' if row['ConstructionSite'] == 1 else row['struct'], axis=1)
print(df['plot_type'])

# Plot each point based on its 'plot_type'.
for struct_type in df['plot_type'].unique():
    subset = df[df['plot_type'] == struct_type]
    
    # Retrieve marker and color based on 'struct_type', with fallbacks for undefined types.
    marker = markers.get(struct_type)
    color = colors.get(struct_type)

    plt.scatter(subset['x'], subset['y'], color=color, marker=marker, label=struct_type)

# Configure grid lines to enhance readability of coordinates.
plt.xticks(np.arange(1, max_x + 1, 1))
plt.yticks(np.arange(1, max_y + 1, 1))
plt.grid(True, which='both', color='lightgray', linestyle='-', linewidth=0.5)

# Set plot labels and title.
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Area Map Visualization')

# Adjust plot limits and invert y-axis to match the desired map orientation (top-left is 1,1).
plt.xlim(0.5, max_x + 0.5)
plt.ylim(0.5, max_y + 0.5)
plt.gca().invert_yaxis()

# Display a legend to explain the symbols and colors. Positioned outside to avoid clutter.
plt.legend(title='Structure Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the generated map as a PNG image.
plt.savefig('map.png')
