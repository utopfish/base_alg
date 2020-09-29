# -*- coding: utf-8 -*-
"""
@Project : base_alg
@File    : test_kd_tree.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/9/29 14:51
"""
import sys, os
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))


import pytest
from utils.load_data import gen_data
from utils.metric import get_euclidean_distance
from alg.kd_tree import KDTree



def test_kdtree():
    low = 0
    high = 100
    n_rows = 1000
    n_cols = 5
    X = gen_data(low, high, n_rows, n_cols)
    y = gen_data(low, high, n_rows)
    Xi = gen_data(low, high, n_cols)
    yi = gen_data(low, high, 1)
    X.extend([Xi])
    y.extend(yi)
    tree = KDTree()
    tree.build_tree(X, y)

    nd = tree.nearest_neighbour_search(Xi)
    ret1 = get_euclidean_distance(Xi, nd.split[0])
    assert ret1==0

if __name__=="__main__":
    pytest.main()