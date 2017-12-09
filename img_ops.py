import numpy as np

def resize(img, amount, algo="greedy"):
    img_tmp = np.copy(img)
    MAX_X = np.shape(img)[0]
    MAX_Y = np.shape(img)[1]

    if amount == 0: return img_tmp
    if amount < 0:
        amount = amount * -1
        for i in range(amount):
            # find the min cut path
            path = None
            if algo == "greedy":
                path = min_cut_greedy(img_tmp)
            elif algo == "random":
                path = min_cut_random(img_tmp)
            elif algo == "dijkstra":
                path = min_cut_dijkstra(img_tmp)
            # stitch 1 pixel at a time
            for node in path:
                nodex = node[0]
                nodey = node[1]
                # copy the row contents before and after the path node
                for x in range(0, nodex):
                    img_tmp[x, nodey] = img[x, nodey]
                for x in range(nodex+1, MAX_X):
                    img_tmp[x-1, nodey] = img[x, nodey]
    return img_tmp[0:MAX_X-amount, 0:MAX_Y]

def dijkstra(img, start_node, end_node, MAX_X, MAX_Y):
    min_cost = float("inf")
    min_path = []

def min_cut_greedy(img, MAX_X, MAX_Y):
    return None    

def min_cut_random(img, MAX_X, MAX_Y):
    min_cost = random.random()
    min_cut = []
    for y in range(0, MAX_Y):
        x = random.randrange(0, MAX_X)
        min_cut.append(x, y)
    return (min_cost, min_cut) 
