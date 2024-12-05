# merge_dataframes.py
import pandas as pd

def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how: str = 'inner') -> pd.DataFrame:
    """
    Merges two dataframes on a specified column with a specified method.
    
    Parameters:
    df1 (pd.DataFrame): The first dataframe to merge.
    df2 (pd.DataFrame): The second dataframe to merge.
    on (str): The column name on which to join.
    how (str): The type of join to perform ('left', 'right', 'outer', 'inner'). Default is 'inner'.
    
    Returns:
    pd.DataFrame: A merged dataframe.
    """
    merged_df = pd.merge(df1, df2, on=on, how=how)
    return merged_df
