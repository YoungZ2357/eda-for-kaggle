import pandas as pd
from typing import Union

def calc_col_missing(df: pd.DataFrame, threshold: float = 0., remove: bool = False) -> Union[pd.DataFrame, list]:
    missing = df.isnull().mean()

    missing_cols = missing[missing > threshold]

    if remove is True:
        cols2remove = missing_cols.index
        df = df.drop(cols2remove, axis=1)
        print(f"Removed cols: {cols2remove}")
        return df

    elif remove is None or remove is False:
        return sorted(missing.to_dict().items(), key=lambda x: x[1])


def calc_row_missing(df: pd.DataFrame, threshold: float = 0., remove: bool = False) -> Union[pd.DataFrame, dict]:
    row_missing = df.isnull().mean(axis=1)
    row_missing = row_missing[row_missing > threshold]

    if remove is True:
        rows2remove = row_missing.index
        df = df.drop(index=rows2remove)
        print(f"Removed {len(rows2remove)} rows")
        return df
    elif remove is None or remove is False:
        return row_missing.to_dict()