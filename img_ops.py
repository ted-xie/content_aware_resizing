import numpy as np
from utils import CLAMP_RANGE
import random

def resize(img, amount, algo="greedy"):
    img_tmp = np.copy(img)
    MAX_X = np.shape(img)[1]
    MAX_Y = np.shape(img)[0]
    random.seed(1234)

    if amount == 0: return img_tmp
    if amount > 0:
        for i in range(amount):
            # find the min cut path
            path = None
            if algo == "greedy":
                path = min_cut_greedy(img_tmp, MAX_X-i, MAX_Y)
            elif algo == "random":
                path = min_cut_random(img_tmp, MAX_X-i, MAX_Y)
            elif algo == "dijkstra":
                path = min_cut_dijkstra(img_tmp)
            # stitch 1 pixel at a time
            img_tmp2 = np.zeros((MAX_Y, MAX_X-i-1))
            for node in path:
                nodex = node[1]
                nodey = node[0]
                # copy the row contents before and after the path node
                row = img_tmp[nodey, :]
                new_row = row[np.arange(len(row)) != nodex]
                img_tmp2[nodey, :] = new_row
            img_tmp = img_tmp2
    return img_tmp[0:MAX_Y, 0:MAX_X-amount]

def generate_greedy_paths(x, y, MAX_X, MAX_Y):
    return [] 

def min_cut_greedy(img, MAX_X, MAX_Y):
    costs = [0.0] * len(paths)
    paths = generate_greedy_paths(MAX_X, MAX_Y)

    for path in paths:
        for node in paths:
            x = node[1]
            y = node[0]
            costs[i] += img[y, x]

    # find minimum cost path
    min_cost = costs[0]
    min_path = None
    for i in range(len(costs)):
        if costs[i] < min_cost:
            min_cost = costs[i]
            min_path = paths[i]

    return min_path

def min_cut_greedy_old(img, MAX_X, MAX_Y):
    costs = [0] * MAX_X
    for y in range(0, MAX_Y):
        tmp = [0] * MAX_X
        for x in range(0, MAX_X):
            SW = CLAMP_RANGE(x-1, 0, MAX_X-1)
            S = CLAMP_RANGE(x, 0, MAX_X-1)
            SE = CLAMP_RANGE(x+1, 0, MAX_X-1)

            left = costs[SW]
            center = costs[S]
            right = costs[SE]

            shortest = min([left, center, right])
            tmp[x] = shortest + img[y, x]
        for x in range(0, MAX_X):
            costs[x] = tmp[x]

    # find the minimum cost end-point
    cost_min = costs[0]
    idx_min = 0
    for x in range(0, MAX_X):
        if costs[x] < cost_min:
            idx_min = x
            cost_min = costs[x]

    print(idx_min)
    path = [0] * MAX_Y
    # greedily backtrack to find path
    path[MAX_Y-1] = idx_min
    for y in range(MAX_Y-2, 0, -1):
        x = path[y+1]
        W = CLAMP_RANGE(x-1, 0, MAX_X-1)
        X = CLAMP_RANGE(x, 0, MAX_X-1)
        E = CLAMP_RANGE(x+1, 0, MAX_X-1)

        candidates_locs = [W, X, E]
        candidates = [img[y, W], img[y, X], img[y, E]]
        candidates_min = candidates[0]
        candidates_idx = 0
        for i in range(3):
            if candidates[i] < candidates_min:
                candidates_idx = i
                candidates_min = candidates[i]
        path[y] = candidates_locs[candidates_idx]
    min_cut = []
    for row in range(len(path)):
        min_cut.append((row, path[row]))
    return min_cut

def min_cut_random(img, MAX_X, MAX_Y):
    # choose random start point
    path = []
    start = random.randint(0, MAX_X-1)
    path.append((0, start))

    for y in range(1, MAX_Y):
        x = path[y-1][1]
        NW = CLAMP_RANGE(x-1, 0, MAX_X-1)
        N = CLAMP_RANGE(x, 0, MAX_X-1)
        NE = CLAMP_RANGE(x+1, 0, MAX_X-1)

        candidates = [NW, N, NE]
        rand_idx = random.randint(0, 2)
        sel = candidates[rand_idx]
        path.append((y, sel))
    return path
