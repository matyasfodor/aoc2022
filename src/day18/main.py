
def get_neighbors(mx, i, j, k):
    ret = []
    if i > 0:
        ret.append([i-1, j, k])
    
    if i < len(mx) - 1 :
        ret.append([i+1, j, k])

    if j > 0:
        ret.append([i, j-1, k])
    
    if j < len(mx) - 1:
        ret.append([i, j+1, k])

    if k > 0:
        ret.append([i, j, k-1])
    
    if k < len(mx) - 1:
        ret.append([i, j, k+ 1])
    return ret

def count_neighbors(mx, neighbor_value, i, j, k):
    ret = 0
    for neighbor in get_neighbors(mx, i, j, k):
        x, y, z = neighbor
        if mx[x][y][z] == neighbor_value:
            ret += 1
    # if i > 0 and mx[i-1][j][k] == 1:
    #     ret += 1
    
    # if i < len(mx) - 1 and mx[i+1][j][k] == 1:
    #     ret += 1

    # if j > 0 and mx[i][j-1][k] == 1:
    #     ret += 1
    
    # if j < len(mx) - 1 and mx[i][j+1][k] == 1:
    #     ret += 1

    # if k > 0 and mx[i][j][k-1] == 1:
    #     ret += 1
    
    # if k < len(mx) - 1 and mx[i][j][k+1] == 1:
    #     ret += 1

    return ret


def fill(mx, fill_value):
    if mx[0][0][0] == 0:
        mx[0][0][0] = 2

    visited = set([(0,0,0)])
    queue = [(0,0,0)]
    while queue:
        item = queue.pop(0)
        neighbors = get_neighbors(mx, *item)
        for neighbor in neighbors:
            x, y, z = neighbor
            if tuple(neighbor) not in visited and mx[x][y][z] == 0:
                mx[x][y][z] = fill_value
                visited.add(tuple(neighbor))
                queue.append(neighbor)
    return mx

def main(fname, second):
    coords = []

    max_item = 0

    with open(fname, 'r') as fp:
        for line in fp:
            item = list(map(int, line.strip().split(',')))
            max_item = max([max_item] + item)
            coords.append(item)

    height = max_item + 1

    mx = [[[0 for _ in range(height)] for _ in range(height)] for _ in range(height)]

    for i, j ,k in coords:
        mx[i][j][k] = 1


    sum_sides = 0

    for i in range(height):
        for j in range(height):
            for k in range(height):
                if mx[i][j][k] == 1:
                    sum_sides += 6 - count_neighbors(mx, 1, i, j, k)
    
    if second:
        mx = fill(mx, 2)
        hole_surface = 0
        for i in range(height):
            for j in range(height):
                for k in range(height):
                    if mx[i][j][k] == 0:
                        hole_surface += count_neighbors(mx, 1, i,j,k)

        sum_sides -= hole_surface

    # layer_groups = defaultdict(list)
    # for coord in coords:
    #     layer_groups[coord[0]].append(coord)

    # layer_keys = sorted(layer_groups.keys())
    
    # prev = None
    # for key in layer_keys:
    print(sum_sides)


fname = 'src/day18/input.txt'
second = True

main(fname, second)