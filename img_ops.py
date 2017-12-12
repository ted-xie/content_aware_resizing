import numpy as np
from utils import CLAMP_RANGE
import random
from scipy import ndimage, misc

def resize(img, amount, algo="greedy"):
    img_tmp = np.copy(img)
    gradient = ndimage.gaussian_gradient_magnitude(img, sigma=5)
    MAX_X = np.shape(img)[1]
    MAX_Y = np.shape(img)[0]
    random.seed(1234)

    if amount == 0: return img_tmp
    if amount > 0:
        for i in range(amount):
            # find the min cut path on the gradient
            path = None
            if algo == "greedy":
                path = min_cut_greedy(gradient, MAX_X-i, MAX_Y)
            elif algo == "random":
                path = min_cut_random(gradient, MAX_X-i, MAX_Y)
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

def min_cut_greedy(img, MAX_X, MAX_Y):
    costs = np.zeros(MAX_X)
    paths = [None] * MAX_X

    # Initialize paths
    for x in range(MAX_X):
        paths[x] = [(0, x)]

    for x in range(MAX_X):
        for y in range(1, MAX_Y):
            last_x = paths[x][y-1][1]
            CTR_x = CLAMP_RANGE(x, 0, MAX_X-1)
            CTR_y = CLAMP_RANGE(y, 0, MAX_Y-1)
            L_x = CLAMP_RANGE(x-1, 0, MAX_X-1)
            L_y = CLAMP_RANGE(y, 0, MAX_Y-1)
            R_x = CLAMP_RANGE(x+1, 0, MAX_X-1)
            R_y = CLAMP_RANGE(y, 0, MAX_Y-1)

            CTR = img[CTR_y, CTR_x]
            L = img[L_y, L_x]
            R = img[R_y, R_x]

            candidates_val = [L, CTR, R]
            candidates_x = [L_x, CTR_x, R_x]
            candidates_y = [L_y, CTR_y, R_y]

            min_cost = candidates_val[0]
            min_idx = 0
            for i in range(3):
                if candidates_val[i] < min_cost:
                    min_cost = candidates_val[i]
                    min_idx = i

            min_x = candidates_x[min_idx]
            min_y = candidates_y[min_idx]

            costs[x] += min_cost
            paths[x].append((min_y, min_x))

    # find minimum-cost path
    best_path = paths[0]
    min_path_cost = costs[0]
    for i in range(len(paths)):
        if costs[i] < min_path_cost:
            min_path_cost = costs[i]
            best_path = paths[i]
    return best_path

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
