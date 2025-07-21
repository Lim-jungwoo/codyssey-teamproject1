import pandas as pd

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
area1 = merged_sorted[merged_sorted['area'] == 1]

cols = ['area'] + [col for col in area1.columns if col != 'area']
cols = [col for col in cols if col != 'ConstructionSite'] + ['ConstructionSite']
# print(cols)
area1 = area1[cols]
# print(area1.head(30))
# print(area1.columns)

area1.fillna('없음').to_csv('area1.csv', index = False)

report = merged_sorted.groupby('struct').agg(
    count = ('struct', 'count'),
    avg_construction_site = ('ConstructionSite', 'mean')
).reset_index()
print(report)