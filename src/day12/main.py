from PIL import Image, ImageDraw

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

class Animation:
    def __init__(self, cell_size, start=None, end=None) -> None:
        self.frames = []
        self.cell_size = cell_size
        self.start = start
        self.end = end

    def add_frame(self, grid, visited):
        height = len(grid)
        width = len(grid[0])
        image = Image.new("RGB", (width*self.cell_size, height*self.cell_size), "black")
        draw = ImageDraw.Draw(image)
        for i, line in enumerate(grid):
            for j, e in enumerate(line):
                color = rgb(0, 28, e)
                draw.rectangle((j*self.cell_size, i*self.cell_size, (j+1) * self.cell_size, (i+1) * self.cell_size), fill=color)
                value = visited.get((i,j))
                if value is not None:
                    draw.text((j*self.cell_size, i*self.cell_size), text=str(value))
        self.frames.append(image)

    def export(self, fname):
        frame_one = self.frames[0]
        frames = [f for i, f in enumerate(self.frames) if i%4 == 0]
        frame_one.save(fname, format="GIF", append_images=frames,
                    save_all=True, duration=50, loop=0)
        


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

def get_dfs(grid, current, reverse=False, animation=None):
    visited = {
        current: 0
    }
    queue = [current]
    while queue:
        element = queue.pop(0)
        animation.add_frame(grid, visited)
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

fname = 'src/day12/input.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()

start_coord = get_coord(lines, 'S')
end_coord = get_coord(lines, 'E')

grid = [[parse(e) for e in line.strip()] for line in lines]

animation = Animation(10)
first = True
if first:
    visited = get_dfs(grid, start_coord, animation=animation)

    print(visited[end_coord])
else:

    visited = get_dfs(grid, end_coord, reverse=True, animation=animation)

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

animation.export('src/day12/animation.gif')