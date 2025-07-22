import pandas as pd


def generate_area_map(area_number=None):
    area_map = pd.read_csv('area_map.csv')
    area_map.columns = area_map.columns.str.strip()
    area_struct = pd.read_csv('area_struct.csv')
    area_struct.columns = area_struct.columns.str.strip()
    area_category = pd.read_csv('area_category.csv')
    area_category.columns = area_category.columns.str.strip()

    struct_with_category = pd.merge(
        area_struct, area_category, on='category', how='left')
    struct_with_category.drop(columns=['category'], inplace=True)

    merged = pd.merge(area_map, struct_with_category,
                      on=['x', 'y'], how='left')

    merged_sorted = merged.sort_values(by=['area', 'x', 'y'])
    merged_sorted: pd.DataFrame = merged_sorted[merged_sorted['area'] == 1]

    cols = ['area'] + [col for col in merged_sorted.columns if col != 'area']
    cols = [col for col in cols if col !=
            'ConstructionSite'] + ['ConstructionSite']
    merged_sorted = merged_sorted[cols]

    output_file = 'area_map.pkl' if area_number is None else f'area_map_{area_number}.pkl'
    merged_sorted.to_pickle(f'{output_file}')

    report = merged_sorted.groupby('struct').agg(
        count=('struct', 'count'),
        avg_construction_site=('ConstructionSite', 'mean')
    ).reset_index()
    print(report)


if __name__ == "__main__":
    generate_area_map(1)
