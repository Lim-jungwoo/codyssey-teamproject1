import pandas as pd


def load_data():
    area_map = pd.read_csv('area_map.csv')
    area_map.columns = area_map.columns.str.strip()

    area_struct = pd.read_csv('area_struct.csv')
    area_struct.columns = area_struct.columns.str.strip()

    area_category = pd.read_csv('area_category.csv')
    area_category.columns = area_category.columns.str.strip()

    return area_map, area_struct, area_category


def generate_map(output_file: str = 'area_map.pkl'):
    area_map, area_struct, area_category = load_data()

    struct_with_category = pd.merge(
        area_struct, area_category, on='category', how='left')
    struct_with_category.drop(columns=['category'], inplace=True)

    merged = pd.merge(area_map, struct_with_category,
                      on=['x', 'y'], how='left')

    merged_sorted = merged.sort_values(by=['area', 'x', 'y'])

    cols = ['area'] + [col for col in merged_sorted.columns if col != 'area']
    cols = [col for col in cols if col !=
            'ConstructionSite'] + ['ConstructionSite']
    merged_sorted = merged_sorted[cols]

    merged_sorted.to_pickle(f'{output_file}')
    print(f"{output_file} 저장 완료")

    print("\n==========area 1 정보===========\n")
    area1: pd.DataFrame = merged_sorted[merged_sorted['area'] == 1]
    print(area1)

    print("\n==========구조물 통계 보고서===========\n")
    report = merged_sorted.groupby('struct').agg(
        count=('struct', 'count'),
        avg_construction_site=('ConstructionSite', 'mean')
    ).reset_index()
    print(report)


def main(output_file: str = 'area_map.pkl'):
    try:
        generate_map(output_file)
    except Exception as e:
        print(f"오류 발생: {e}")
        return


if __name__ == "__main__":
    main()
