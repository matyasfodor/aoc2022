import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation
from matplotlib import rcParams


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

    return ret


def plot_mx(mx):
    data = np.array(mx)
    voxelarray = np.zeros(data.shape, dtype=bool)
    voxelarray[data < 2] = True
    colors= np.zeros(list(data.shape) + [4], dtype=np.float32)

    colors[voxelarray == 1] = [0,1,0,0.3]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.axis('off')

    ax.voxels(voxelarray, facecolors=colors)

    voxelarray = np.zeros(data.shape, dtype=bool)
    voxelarray[data == 0] = True

    colors= np.zeros(list(data.shape) + [4], dtype=np.float32)

    colors[data == 0] = [0.5, 0.2, 0.8, 1]

    ax.voxels(voxelarray, facecolors=colors)

    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)

    def animate(i):
        ax.view_init(30, i * 10)
        return fig ,
        # redDot.set_data(i, np.sin(i))
        # return redDot,

    rcParams['animation.convert_path'] = os.path.dirname(__file__)

    myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0.0, 36, 1), \
                                        interval=100, blit=True, repeat=False)

    myAnimation.save('myAnimation.gif', writer='imagemagick', fps=10)

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
        plot_mx(mx)
        hole_surface = 0
        for i in range(height):
            for j in range(height):
                for k in range(height):
                    if mx[i][j][k] == 0:
                        hole_surface += count_neighbors(mx, 1, i,j,k)

        print(hole_surface)

        sum_sides -= hole_surface
    print(sum_sides)


fname = 'src/day18/input.txt'
second = True

main(fname, second)