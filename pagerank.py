#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import numpy as np
import pandas as pd
import pickle
from scipy import sparse
from scipy.sparse import lil_matrix
import threadpool
from time import time

from config import db_file
from config import pagerank_file



index2node = dict()
node2index = dict()


def PageRank(M, alpha):

    print("Pageranking...")
    start = time()

    n = M.shape[0]
    v = np.zeros(n)
    def_val = 1/n
    for i in range(n):
        v[i] = def_val
    _v = alpha*M.dot(v) + (1-alpha)*v
    while (abs(v - _v)).sum() > 0.0001:
        v = _v
        _v = alpha*M.dot(v) + (1-alpha)*v

    result = {}
    for ind, prob in enumerate(v):
        if prob != 0:
            result[index2node[ind]] = prob
    #result = [ele for ele in result if ele[1] != 0]

    stop = time()
    print("Rank done.")
    print(str(stop-start) + "sec")

    return result



def initMat(node1, node2, M):
    M[node2index[node2],node2index[node1]] = 1/len(G[node1])

def Generate_Transfer_Matrix(G):

    print("Generating Transfer Matrix...")
    start = time()

    for index,node in enumerate(G.keys()):
        node2index[node] = index
        index2node[index] = node
    n = len(node2index)
    M = lil_matrix((n, n), dtype=np.float32)

    for node1 in G.keys():
        G[node1] = {e for e in G[node1] if e in node2index}

    pool = threadpool.ThreadPool(16)
    init_vals = []
    for node1 in G.keys():
        for node2 in G[node1]:
            init_vals.append(([node1,node2,M], None))

    threqs = threadpool.makeRequests(initMat, init_vals)
    for req in threqs:
        pool.putRequest(req)
    pool.wait()

    stop = time()
    print("Generate done.")
    print(str(stop-start) + "sec")

    return M, node2index, index2node



if __name__ == '__main__':

    alpha = 0.85
    G = {}

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    cursor = c.execute("SELECT av, ref_av FROM ref")
    for row in cursor:
        if int(row[0]) not in G:
            G[int(row[0])] = {}
        G[int(row[0])][int(row[1])] = 1

    c.close()
    conn.close()

    M, node2index, index2node = Generate_Transfer_Matrix(G)
    #print(M)

    result = PageRank(M, alpha)
    #print(result)

    with open(pagerank_file, "wb") as f:
        pickle.dump(result, f)
