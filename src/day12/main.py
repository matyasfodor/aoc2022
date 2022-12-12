fname = 'src/day12/input.txt'

def get_coord(grid, char):
    for i, line in enumerate(grid):
        for j, curr_char in enumerate(line):
            if curr_char == char:
                return i,j

def parse(e):
    if e == 'S':
        e = 'a'
    if e == 'E':
        e = 'z'
    return ord(e) - ord('a')

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

def get_dfs(grid, current, reverse=False):
    visited = {
        current: 0
    }
    queue = [current]
    while queue:
        element = queue.pop(0)
        for dir in directions:
            new_pos = (element[0] + dir[0], element[1] + dir[1])
            new_steps = visited[element] + 1
            if new_steps < visited.get(new_pos, float('inf')) and 0 <= new_pos[0] < len(grid) and 0 <= new_pos[1] < len(grid[0]):
                if reverse:
                    if grid[element[0]][element[1]] - grid[new_pos[0]][new_pos[1]]< 2:
                        queue.append(new_pos)
                        visited[new_pos] = new_steps
                else:
                    if grid[new_pos[0]][new_pos[1]] - grid[element[0]][element[1]] < 2:
                        queue.append(new_pos)
                        visited[new_pos] = new_steps
    print(len(visited), len(grid), len(grid[0]))
    return visited

with open(fname, 'r') as fp:
    lines = fp.readlines()

start_coord = get_coord(lines, 'S')
end_coord = get_coord(lines, 'E')

grid = [[parse(e) for e in line.strip()] for line in lines]

first = False
if first:
    visited = get_dfs(grid, start_coord)

    print(visited[end_coord])
else:

    visited = get_dfs(grid, end_coord, reverse=True)

    min_steps = float('inf')
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                # Visited might not have the coord
                try:
                    min_steps = min(visited[(i, j)], min_steps)
                except:
                    pass
    print(min_steps)

