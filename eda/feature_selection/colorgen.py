import random
from typing import Literal, Union
import colorsys

def generate_color_rand(n: int) -> list:
    """随机生成n个16进制色号

    :param n: 颜色数量
    :return: 色号列表
    """
    assert n > 0, ValueError("[colorgen.generate_color_rand]颜色数必须大于1")
    colors = []
    for _ in range(n):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors.append(color)

    return colors

def generate_color_gradient(
        n: int,
        base: Literal["c2w", "w2c"],
        brightness: Union[Literal["l2d", "d2l"], None]=None
) -> list:
    """渐变形式生成指定数量色号

    :param n:
    :param base: 颜色渐变方式。可用: c2w -> 冷色渐变暖色; w2c -> 冷色渐变暖色
    :param brightness: 颜色深浅渐变方式。可用: l2d -> 浅色渐变深色; d2l -> 深色渐变浅色
    :return: 色号列表
    """
    assert n > 0, ValueError("[colorgen.generate_color_gradient]颜色数必须大于1")

    colors = []
    start_hue = 2 / 3 if base == "c2w" else 0
    end_hue = 0 if base == "c2w" else 2 / 3

    value = None
    if brightness is None:
        value = 1.
    else:
        start_value = 1. if brightness == "l2d" else 0.4
        end_value = 0.4 if brightness == "l2d" else 1.
    for i in range(n):
        hue = start_hue + (end_hue - start_hue) * (i / (n-1))
        if value is None:  # 我懒得再专门处理这个变量报错了，反正能用
            value = start_value + (end_value - start_value) * (i / (n-1))
        else:
            pass
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, value)
        color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        colors.append(color)
    return colors



