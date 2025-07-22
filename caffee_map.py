import pandas as pd

area_map = pd.read_csv('./area_map.csv')
area_struct = pd.read_csv('./area_struct.csv')
area_category = pd.read_csv('./area_category.csv')

# 1. 데이터 출력 및 기본 분석
print('=== area_map ===')
print(area_map.head(), '\n')

print('=== area_struct ===')
print(area_struct.head(), '\n')

print('=== area_category ===')
print(area_category.head(), '\n')


# 2. 구조물 ID를 area_category.csv 기준으로 이름으로 변환
area_struct = area_struct.merge(right=area_category, how='left', on='category')
area_struct = area_struct.drop(columns=['category'])
print(area_struct)

# 3. 세 데이터를 하나의 DataFrame으로 병합하고, area를 기준으로 정렬
merged_df = pd.merge(left=area_struct, right=area_map, on=['x', 'y'])

sorted_df = merged_df.sort_values(by='area')

merged_df.to_pickle('merged.pkl')
merged_df.to_csv('merged.csv')

# 4. area 1에 대한 데이터만 필터링해서 출력
area1_data = sorted_df[sorted_df['area'] == 1]
print('=== Area 1 Data ===')
print(area1_data, '\n')
