from typing import Dict, Literal, List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import UnivariateSpline


def get_data(dist: Literal["normal", "uniform"] = 'normal', size=1_000_000, **dist_args):
    """
    Get some random data from a distribution.
    """
    if dist == 'normal':
        return np.random.normal(size=size, **dist_args)
    elif dist == 'uniform':
        return np.random.uniform(size=size, **dist_args)


def get_quantiles(data_dict: Dict[float, np.ndarray], step: float = 0.001):
    """
    Calculate the quantiles of the data.
    """
    return {scale: {"y": np.arange(0, 1 + step, step), "x": np.quantile(scale_data, np.arange(0, 1 + step, step))} for
            scale, scale_data in data_dict.items()}


def get_diffs(data_dict: Dict[float, np.ndarray]):
    """
    Calculate the differences between the quantiles of the data.
    """
    print(data_dict[1])
    print(np.gradient(data_dict[1]["y"], data_dict[1]["x"]))

    return {scale: {"y": np.gradient(scale_data["y"], scale_data["x"]), "x": scale_data["x"]} for scale, scale_data in
            data_dict.items()}


def plot(data_dict: Dict[float, np.ndarray], type: Literal["cdf", "pd"]):
    def plot_format(function_name, title):
        plt.xlabel('x')
        plt.ylabel(function_name)
        plt.title(title)

    """
   Plot the data.
    """
    if type == 'cdf':
        for scale, scale_data in data_dict.items():
            plt.plot(scale_data["x"], scale_data["y"], label=f'sd={scale}')
        plot_format('F(x)', 'Cumulative Distribution Function')
    elif type == 'pd':
        for scale, scale_data in data_dict.items():
            plt.plot(scale_data["x"], scale_data["y"], label=f'sd={scale}')
        plot_format('f(x)', 'Probability Distribution ')


def cdf_example(scales: List[float], dist: Literal["normal", "uniform"] = 'normal', quantile_step: float = 0.01,
                rs: Optional[int] = None):
    if rs:
        np.random.seed(rs)
    data = {s: get_data(dist=dist, scale=s) for s in scales}
    data = get_quantiles(data, step=quantile_step)

    plot(data, type='cdf')
    plt.legend()
    plt.grid()
    plt.show()


def pd_example(scales: List[float], dist: Literal["normal", "uniform"] = 'normal', quantile_step: float = 0.01,
               rs: Optional[int] = None):
    if rs:
        np.random.seed(rs)
    data = {s: get_data(dist=dist, scale=s) for s in scales}
    data = get_quantiles(data, step=quantile_step)
    data = get_diffs(data)

    plot(data, type='pd')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # cdf_example([0.5, 1, 2], rs=7)
    pd_example([0.5, 1, 2], rs=7, quantile_step=0.001)
