import pandas as pd

def process_area_data():
   
    print("--- 1. CSV 파일 불러오기 및 내용 출력 ---")

    # Define file paths
    map_file = 'area_map.csv'
    struct_file = 'area_struct.csv'
    category_file = 'area_category.csv'

    # Load CSV files
    try:
        df_map = pd.read_csv(map_file)
        df_struct = pd.read_csv(struct_file)
        df_category = pd.read_csv(category_file)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure '{map_file}', '{struct_file}', and '{category_file}' are in the same directory as the script.")
        print("Current working directory:", pd.io.common.os.getcwd()) # This helps in debugging file location issues
        return None # Return None to indicate failure

    # Print contents of each DataFrame
    print(f"\n--- {map_file} 내용 (상위 5행) ---")
    print(df_map.head())
    print(f"\n--- {struct_file} 내용 (상위 5행) ---")
    print(df_struct.head())
    print(f"\n--- {category_file} 내용 (상위 5행) ---")
    print(df_category.head())

    print("\n--- 2. 구조물 ID를 이름으로 변환 ---")
    # Merge df_struct with df_category on 'category' to get structure names
    # The 'struct' column from df_category contains the human-readable names.
    df_struct_with_names = pd.merge(df_struct, df_category, on='category', how='left') 

    # Rename the 'struct' column to 'structure_name' for clarity
    df_struct_with_names = df_struct_with_names.rename(columns={'struct': 'structure_name'})

    # Drop the original 'category' ID column from this intermediate DataFrame
    df_struct_with_names = df_struct_with_names.drop(columns=['category'])

    print("\n--- 구조물 ID가 이름으로 변환된 데이터 (상위 5행) ---")
    print(df_struct_with_names.head())


    print("\n--- 3. 세 데이터를 하나의 DataFrame으로 병합 및 정렬 ---")
    # Merge df_map (contains x, y, ConstructionSite) with df_struct_with_names
    # (contains x, y, area, structure_name).
    # We use a left merge with df_map as the primary table to ensure all grid points
    # (including those without a specific 'structure_name' but possibly a 'ConstructionSite') are included.
    # Coordinates from area_map.csv  and area_struct.csv [cite: 2] are used for merging.
    final_df = pd.merge(df_map, df_struct_with_names, on=['x', 'y'], how='left')

    # Fill NaN values in 'structure_name' with a placeholder like 'Road' or 'Empty'
    # if a coordinate from df_map has no corresponding structure in df_struct.
    # For now, we'll leave them as NaN, but for later steps (like visualization or pathfinding),
    # you might want to fill these.

    # Sort the combined DataFrame by 'area'
    final_df = final_df.sort_values(by='area').reset_index(drop=True)

    print("\n--- 병합 및 'area' 기준으로 정렬된 최종 DataFrame (상위 5행) ---")
    print(final_df.head())
    # print(f"\n총 데이터 개수: {len(final_df)}")


    print("\n--- 4. Area 1 데이터만 필터링 ---")
    # Filter the DataFrame to include only data for 'area' 1.
    # The problem statement indicates that Bandalgom Coffee is concentrated in Area 1.
    area1_data = final_df[final_df['area'] == 1].copy() # .copy() is used to prevent SettingWithCopyWarning

    print("\n--- Area 1에 대한 필터링된 데이터 (상위 5행) ---")
    print(area1_data.head())
    print(f"\nArea 1 데이터 개수: {len(area1_data)}")

    # (Bonus) Print summary statistics for structure types in Area 1
    print("\n--- (보너스) Area 1 구조물 종류별 요약 통계 ---")
    #Error
    # Count occurrences of each 'structure_name' in the filtered data.
    # structure_counts = area1_data['structure_name'].value_counts(dropna=False).reset_index()
    # structure_counts.columns = ['Structure Type', 'Count']
    # print(structure_counts)
    # print("\n(참고: 'Structure Type'이 NaN인 경우는 Area 1 내에 structure_name이 명시되지 않은 좌표입니다.)")


    return area1_data # Return the processed and filtered DataFrame

if __name__ == '__main__':
    # This block runs when the script is executed directly.
    # It calls the main processing function and stores the result.
    processed_df_area1 = process_area_data()

    if processed_df_area1 is not None:
        print("\n--- 데이터 처리 완료 ---")
        # You can now use 'processed_df_area1' for the next steps (map visualization).
        # For example, to save it to a new CSV for verification:
        # processed_df_area1.to_csv('area1_processed_data_for_map.csv', index=False)

