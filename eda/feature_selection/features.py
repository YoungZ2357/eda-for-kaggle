
from eda.feature_selection.colorgen import generate_color_rand
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def stacked_bar_grid(
        df: pd.DataFrame,
        feature_cols: list,
        label_cols: list,
        ratio: bool = False,
        colors: list = None,  # generate random colors if colors is None
        stack: bool = True,
        save_path: str = None,
        show_plot: bool = True,
        figsize: tuple = (10, 8)
) -> None:
    """以接近正方形的子图排列，绘制每一个标签列下不同离散值特征的分布图像。列必须为定类、定序类型(即离散值)。图像类别为堆叠柱状图
    备注：实际上feature_cols和label_cols可以是任意想要比较的列。该函数最初用于针对大量标签列的批量预测问题。
    :param df: 数据集，必须为pandas.DataFrame
    :param feature_cols: 待绘制特征列列名
    :param label_cols: 待绘制标签列列名.
    :param ratio: 是否以比例的形式显示
    :param colors: 图像颜色，格式为列表。若为None则随机生成特征数量个颜色
    :param stack: 是否将柱状图堆叠，默认为是
    :param save_path: 图像保存路径，若为None则不保存
    :param show_plot: 是否展示图像。每个标签会展示一次
    :param figsize: 子图大小，格式为(长, 宽)。默认为(10, 8)
    :return:
    """

    for label in label_cols:
        num_features = len(feature_cols)
        total_plots = num_features
        cols = int(np.ceil(np.sqrt(total_plots)))
        rows = int(np.ceil(total_plots / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(cols * figsize[0], rows * figsize[1]))

        axes = axes.flatten()
        plot_idx = 0
        if colors is None:
            colors = generate_color_rand(num_features)

        for feature in feature_cols:
            counts = df.groupby([feature, label]).size().unstack(fill_value=0)
            if ratio:
                counts = counts.div(counts.sum(axis=1), axis=0)

            ax = axes[plot_idx]
            counts.plot(
                kind="bar",
                stacked=stack,
                alpha=.8,
                color=colors,
                ax=ax
            )
            ax.set_title(f"{feature} -> {label}")
            plot_idx += 1

        for i in range(plot_idx, len(axes)):
            fig.delaxes(axes[i])

        if save_path:
            label_save_path = save_path.replace(".png", f"_{label}.png")
            plt.savefig(label_save_path, bbox_inches='tight')
            print(f"Plot for '{label}' saved to {label_save_path}")

        if show_plot:
            plt.show()


def boxplots_grid(
        df: pd.DataFrame,
        feature_cols: list,
        color: str = "skyblue",
        save_path: str = None,
        show_plot: bool = True,
        figsize: tuple = (10, 8)
) -> None:
    """以接近正方形的子图排列，绘制指定特征列的箱型图。列必须为数值类型(不论是否离散)。

    :param df: 数据集，必须为pandas.DataFrame
    :param feature_cols: 待绘制特征列列名
    :param color: 箱型图颜色，必须为seaborn支持的颜色字符串或色号
    :param save_path: 图像保存路径，若为None则不保存
    :param show_plot: 是否展示图像。每个标签会展示一次
    :param figsize: 子图大小，格式为(长, 宽)。默认为(10, 8)
    :return:
    """
    num_features = len(feature_cols)
    cols = int(np.ceil(np.sqrt(num_features)))
    rows = int(np.ceil(num_features / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(cols * figsize[0], rows * figsize[1]))
    axes = axes.flatten()
    for idx, feature in enumerate(feature_cols):
        sns.boxplot(data=df, y=feature, ax=axes[idx], color=color)
    if show_plot:
        plt.show()
    if save_path:
        # os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        print(f"Plot saved to {save_path}")


def single_bar_grid(
        df: pd.DataFrame,
        feature_cols: list,
        ratio: bool = False,
        color: str = "skyblue",
        save_path: str = None,
        show_plot: bool = True,
        figsize: tuple = (10, 8)
) -> None:
    """

    :param df:
    :param feature_cols:
    :param ratio:
    :param color:
    :param save_path:
    :param show_plot:
    :param figsize:
    :return:
    """
    num_features = len(feature_cols)
    cols = int(np.ceil(np.sqrt(num_features)))
    rows = int(np.ceil(num_features / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(cols * figsize[0], rows * figsize[1]))
    axes = axes.flatten()
    plot_idx = 0
    if color is None:
        color = generate_color_rand(1)
    for feature in feature_cols:
        count = df.loc[:, feature].value_counts()
        # print(count)
        ax = axes[plot_idx]
        ax.bar(x=count.index, height=count.tolist(), color=color)
        plot_idx += 1

    for i in range(plot_idx, len(axes)):
        fig.delaxes(axes[i])

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print(f"Plot  saved to {save_path}")

    if show_plot:
        plt.show()
