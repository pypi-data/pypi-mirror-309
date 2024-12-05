# tests/test_merge_dataframes.py
import pandas as pd
from merge_dataframes import merge_dataframes

def test_merge_dataframes():
    df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']})
    df2 = pd.DataFrame({'id': [1, 2, 4], 'age': [24, 25, 23]})

    merged_inner = merge_dataframes(df1, df2, on='id', how='inner')
    assert merged_inner.shape[0] == 2  # Inner join should return 2 rows

    merged_outer = merge_dataframes(df1, df2, on='id', how='outer')
    assert merged_outer.shape[0] == 4  # Outer join should return 4 rows

    print("All tests passed!")
