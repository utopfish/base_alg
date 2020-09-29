# -*- coding: utf-8 -*-
"""
@Project : base_alg
@File    : load_data.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/9/29 14:56
"""
from random import randint
def gen_data(low, high, n_rows, n_cols=None):
    """Generate dataset randomly.
    Arguments:
        low {int} -- The minimum value of element generated.
        high {int} -- The maximum value of element generated.
        n_rows {int} -- Number of rows.
        n_cols {int} -- Number of columns.
    Returns:
        list -- 1d or 2d list with int
    """
    if n_cols is None:
        ret = [randint(low, high) for _ in range(n_rows)]
    else:
        ret = [[randint(low, high) for _ in range(n_cols)]
               for _ in range(n_rows)]
    return ret