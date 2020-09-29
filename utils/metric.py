# -*- coding: utf-8 -*-
"""
@Project : base_alg
@File    : metric.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/9/29 15:02
"""
from numpy import array
def get_euclidean_distance(arr1, arr2) -> float:
    """"Calculate the Euclidean distance of two vectors.
    Arguments:
        arr1 {List}
        arr2 {List}
    Returns:
        float
    """
    arr1=array(arr1)
    arr2=array(arr2)
    return ((arr1 - arr2) ** 2).sum() ** 0.5