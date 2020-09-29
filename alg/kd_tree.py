# -*- coding: utf-8 -*-
"""
@Project : base_alg
@File    : kd_tree.py
@Author  : Mr.Liu Meng
@E-mail  : utopfish@163.com
@Time    : 2020/9/29 11:13
"""

from utils.metric import get_euclidean_distance

"""
如何建立KDTree
1. 建立根节点；
2. 选取方差最大的特征作为分割特征；
3. 选择该特征的中位数作为分割点；
4. 将数据集中该特征小于中位数的传递给根节点的左儿子，大于中位数的传递给根节点的右儿子；
5. 递归执行步骤2-4，直到所有数据都被建立到KD Tree的节点上为止。

如何搜索KDtree
1. 从根节点开始，根据目标在分割特征中是否小于或大于当前节点，向左或向右移动。
2. 一旦算法到达叶节点，它就将节点保存为“当前最佳”。
3. 回溯，即从叶节点再返回到根节点 (使用root=root.father)
4. 如果当前节点比当前最佳节点更接近，那么它就成为当前最好的。回溯的过程中也计算距离
5. 如果目标距离当前节点的父节点所在的数据集分割为两份的超平面的距离更接近，说明当前节点的兄弟节点所在的子树有可能包
含更近的点。因此需要对这个兄弟节点设为根节点递归执行1-4步。(使用队列方法，对兄弟节点的执行为将兄弟节点和兄弟节点对应
找到的叶子节点，加入到队列中，队列为空后返回的即为最接近的节点)
"""


class Node:
    def __init__(self):
        self.father = None
        self.left = None
        self.right = None
        self.feature = None
        self.split = None

    def __str__(self):
        return "feature: {}, split: {}".format(str(self.feature), str(self.split))

    # 获取兄弟节点的值，使用装饰器将方法当作属性调用
    @property
    def brother(self):
        if not self.father:
            return None
        elif self.father.left is self:
            return self.father.right
        else:
            return self.father.left


class KDTree:
    def __init__(self):
        self.root = Node()

    # 查看节点值
    def __str__(self):
        ret = []
        i = 0
        que = [(self.root, -1)]
        while que:
            node, idx_father = que.pop(0)
            ret.append("{} -> {}: {}".format(idx_father, i, node))
            if node.left:
                que.append((node.left, i))
            if node.right:
                que.append((node.right, i))
            i += 1
        return "\n".join(ret)

    def _get_median_idx(self, X, idxs, feature):
        n = len(idxs)
        k = n // 2
        # 找到方差最大
        col = map(lambda i: (i, X[i][feature]), idxs)
        sorted_idxs = map(lambda x: x[0], sorted(col, key=lambda x: x[1]))
        median_idx = list(sorted_idxs)[k]
        return median_idx

    def _get_variance(self, X, idxs, feature):
        n = len(idxs)
        col_sum = col_sum_sqr = 0
        for idx in idxs:
            xi = X[idx][feature]
            col_sum += xi
            col_sum_sqr += xi ** 2
        # float 不能进行位运算 **2 不能写成<<1
        return col_sum_sqr / n - (col_sum / n) ** 2

    # 选取方差最大的特征作为分割点特征
    def _choose_feature(self, X, idxs):
        m = len(X[0])
        variances = map(lambda j: (
            j, self._get_variance(X, idxs, j)), range(m))
        return max(variances, key=lambda x: x[1])[0]

    # 将大于和小于中位数的元素分别放入两个列表中
    def _split_feature(self, X, idxs, feature, median_idx):
        idxs_split = [[], []]
        split_val = X[median_idx][feature]
        for idx in idxs:
            if idx == median_idx:
                continue
            xi = X[idx][feature]
            if xi < split_val:
                idxs_split[0].append(idx)
            else:
                idxs_split[1].append(idx)
        return idxs_split

    def build_tree(self, X, y):
        nd = self.root
        idxs = range(len(X))
        que = [(nd, idxs)]
        while que:
            nd, idxs = que.pop(0)
            n = len(idxs)
            # Stop split if there is only one element in this node
            if n == 1:
                nd.split = (X[idxs[0]], y[idxs[0]])
                continue
            # Split
            feature = self._choose_feature(X, idxs)
            median_idx = self._get_median_idx(X, idxs, feature)
            idxs_left, idxs_right = self._split_feature(
                X, idxs, feature, median_idx)
            # Update properties of current node
            nd.feature = feature
            nd.split = (X[median_idx], y[median_idx])
            # Put children of current node in que
            if idxs_left != []:
                nd.left = Node()
                nd.left.father = nd
                que.append((nd.left, idxs_left))
            if idxs_right != []:
                nd.right = Node()
                nd.right.father = nd
                que.append((nd.right, idxs_right))

    def _search(self, Xi, nd):
        while nd.left or nd.right:
            if not nd.left:
                nd = nd.right
            elif not nd.right:
                nd = nd.left
            else:
                if Xi[nd.feature] < nd.split[0][nd.feature]:
                    nd = nd.left
                else:
                    nd = nd.right
        return nd

    def _get_eu_dist(self, Xi, nd):
        X0 = nd.split[0]
        return get_euclidean_distance(Xi, X0)

    # 计算超平面距离
    def _get_hyper_plane_dist(self, Xi, nd):
        j = nd.feature
        X0 = nd.split[0]
        return abs(Xi[j] - X0[j])

    def nearest_neighbour_search(self, Xi):
        dist_best = float('inf')
        nd_best = self._search(Xi, self.root)
        que = [(self.root, nd_best)]
        while que:
            nd_root, nd_cur = que.pop(0)
            dist = self._get_eu_dist(Xi, nd_root)
            if dist < dist_best:
                dist_best, nd_best = dist, nd_root
            while nd_cur is not nd_root:
                dist = self._get_eu_dist(Xi, nd_cur)
                # Update best node, distance and visit flag.
                if dist < dist_best:
                    dist_best, nd_best = dist, nd_cur
                # If it's necessary to visit brother node.
                if nd_cur.brother and dist_best > \
                        self._get_hyper_plane_dist(Xi, nd_cur.father):
                    _nd_best = self._search(Xi, nd_cur.brother)
                    que.append((nd_cur.brother, _nd_best))
                # Back track.
                nd_cur = nd_cur.father
        return nd_best

