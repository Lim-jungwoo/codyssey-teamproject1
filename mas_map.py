import pandas as pd

import sys
output_file = None
area_number = None
if len(sys.argv) == 1:
    output_file = 'all_area.csv'
elif len(sys.argv) == 2:
    try:
        area_number = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid area number.")
        sys.exit(1)
    output_file = f'area{sys.argv[1]}.csv'
else:
    print("Usage: python mas_map.py [area_number]")
    sys.exit(1)

area_map = pd.read_csv('area_map.csv')
area_struct = pd.read_csv('area_struct.csv')
area_category = pd.read_csv('area_category.csv')
area_category.columns = area_category.columns.str.strip()

struct_with_category = pd.merge(area_struct, area_category, on = 'category', how = 'left')
struct_with_category.drop(columns = ['category'], inplace = True)
# print(struct_with_category.head(30))

merged = pd.merge(area_map, struct_with_category, on = ['x', 'y'], how = 'left')
# print(merged.head(30))

merged_sorted = merged.sort_values(by = ['area', 'x', 'y'])
# print(merged_sorted.head(30))
if area_number is not None:
    merged_sorted = merged_sorted[merged_sorted['area'] == area_number]

cols = ['area'] + [col for col in merged_sorted.columns if col != 'area']
cols = [col for col in cols if col != 'ConstructionSite'] + ['ConstructionSite']
# print(cols)
merged_sorted = merged_sorted[cols]
# print(merged_sorted.head(30))
# print(merged_sorted.columns)

merged_sorted.fillna('없음').to_csv(f'{output_file}', index = False)

report = merged_sorted.groupby('struct').agg(
    count = ('struct', 'count'),
    avg_construction_site = ('ConstructionSite', 'mean')
).reset_index()
print(report)