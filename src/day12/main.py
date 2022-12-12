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

# def get_dfs(grid, current, end):
#     visited = {
#         current: 0,
#     }
#     def dfs(current, steps, trace):
#         # print(steps)
#         if current == end:
#             return steps, trace
#         res = None
#         min_trace = None
#         for dir in directions:
#             new_pos = (current[0] + dir[0], current[1] + dir[1])
#             new_steps = steps + 1
#             if new_steps < visited.get(new_pos, float('inf')) and 0 <= new_pos[0] <= len(grid) and 0 <= new_pos[1] < len(grid[0]):
#                 if new_pos == end:
#                     return new_steps, trace + [new_pos]
#                 visited[new_pos] = new_steps
#                 rec, new_trace = dfs(new_pos, new_steps, trace +[new_pos])
#                 if res is None:
#                     res = rec
#                     min_trace = new_trace
#                 if rec is not None:
#                     rec = min(rec, res)
#                     min_trace = new_trace
#         return res, min_trace
#     return dfs(current, 0, [current])

def get_dfs(grid, current, end):
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

visited = get_dfs(grid, start_coord, end_coord)

# print(res)
if end_coord in visited:
    print(visited[end_coord])
else:
    for i in range(len(grid)):
        line = list(lines[i].strip())
        for j in range(len(grid[1])):
            if (i, j) in visited:
                line[j] = '.'

        print(''.join(line))
