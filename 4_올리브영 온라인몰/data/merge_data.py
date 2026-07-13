"""
올리브영 건강식품 관련 4개 카테고리(비타민, 슬리밍/이너뷰티, 영양제, 유산균)의 수집 데이터를
하나의 CSV 파일(올리브영_건강식품_수집데이터.csv)로 병합하는 스크립트입니다.
"""

import pandas as pd
import os

files = [
    r"c:\Users\tasha\OneDrive\바탕 화면\ICB10_02\project2_team3\4_올리브영 온라인몰\data\올리브영_비타민_수집데이터.csv",
    r"c:\Users\tasha\OneDrive\바탕 화면\ICB10_02\project2_team3\4_올리브영 온라인몰\data\올리브영_슬리밍_이너뷰티_수집데이터.csv",
    r"c:\Users\tasha\OneDrive\바탕 화면\ICB10_02\project2_team3\4_올리브영 온라인몰\data\올리브영_영양제_수집데이터.csv",
    r"c:\Users\tasha\OneDrive\바탕 화면\ICB10_02\project2_team3\4_올리브영 온라인몰\data\올리브영_유산균_수집데이터.csv"
]

dfs = []
for f in files:
    try:
        # Try reading with utf-8-sig first (common for Korean CSVs)
        df = pd.read_csv(f, encoding='utf-8-sig')
        print(f"Loaded {os.path.basename(f)} with utf-8-sig: {df.shape}")
    except Exception:
        try:
            # Try reading with cp949 if utf-8-sig fails
            df = pd.read_csv(f, encoding='cp949')
            print(f"Loaded {os.path.basename(f)} with cp949: {df.shape}")
        except Exception as e:
            # If both fail, try with default/latin1 or log error
            print(f"Failed to read {f}: {e}")
            raise e
    dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Write to the destination file
output_file = r"c:\Users\tasha\OneDrive\바탕 화면\ICB10_02\project2_team3\4_올리브영 온라인몰\data\올리브영_건강식품_수집데이터.csv"
merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"Successfully merged into {output_file} (Total rows: {len(merged_df)})")
