from typing import Literal
import pandas as pd
def high_corr_pairs(corr_matrix: pd.DataFrame, threshold: float = 0.8, output_type: Literal["groups", "pairs"]='groups'):
    """从相关性矩阵获取相关性大于阈值的特征组或特征对


    :param corr_matrix: 相关性矩阵，使用 pandas.DataFrame.corr()获取
    :param threshold: 定义为高相关特征的阈值，默认0.8
    :param output_type: 输出类型。使用groups来获取便于降维操作的列名称列表，使用pairs来获取便于观察特征的特征对列表(带有相关性)
    :return: 特征组或高频特征对
    """
    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        parent[find(x)] = find(y)

    for col in corr_matrix.columns:
        parent[col] = col

    pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > threshold:
                pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_value))
                union(corr_matrix.columns[i], corr_matrix.columns[j])

    if output_type == 'pairs':
        return sorted(pairs, key=lambda x: x[2])


    groups = {}
    for col in corr_matrix.columns:
        root = find(col)
        if root not in groups:
            groups[root] = []
        groups[root].append(col)

    return list(groups.values())


