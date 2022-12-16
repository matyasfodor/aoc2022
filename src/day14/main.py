from itertools import pairwise
from PIL import Image, ImageDraw


class Animation:
    def __init__(self, cell_size) -> None:
        self.frames = []
        self.cell_size = cell_size

    def add_frame(self, mx):
        height = len(mx)
        width = len(mx[0])
        image = Image.new("RGB", (width*self.cell_size, height*self.cell_size), "black")
        draw = ImageDraw.Draw(image)
        for i, line in enumerate(mx):
            for j, e in enumerate(line):
                if e == '#':
                    draw.rectangle((j*self.cell_size, i*self.cell_size, (j+1) * self.cell_size, (i+1) * self.cell_size), fill=(165, 99, 41))
                elif e == 'o':
                    draw.rectangle((j*self.cell_size, i*self.cell_size, (j+1) * self.cell_size, (i+1) * self.cell_size), fill=(125, 125, 255))
                elif e == '+':
                    draw.rectangle((j*self.cell_size, i*self.cell_size, (j+1) * self.cell_size, (i+1) * self.cell_size), fill=(0, 0, 255))
                # draw.text((j*self.cell_size, i*self.cell_size), text=str(e))
        self.frames.append(image)

    def export(self, fname):
        frame_one = self.frames[0]
        subsample = None
        frames = [f for i, f in enumerate(self.frames) if subsample is None or i % subsample == 0]
        print('start save')
        frame_one.save(fname, format="GIF", append_images=frames,
                    save_all=True, duration=50, loop=0)
        print('saved')
        


def draw(x_min, y_min, x_max, y_max, line_set, settlement, current_sand, animation):
    mx = []
    for i in range(x_min, x_max + 1):
        mx_line = []
        for j in range(y_min, y_max+ 1):
            if (i,j) in line_set:
                elem = '#'
            elif (i,j) in settlement:
                elem = 'o'
            elif (i, j) == tuple(current_sand):
                elem = '+'
            else:
                elem = '.'
            mx_line.append(elem)
        mx.append(mx_line)
    mx = list(zip(*mx))
    animation.add_frame(mx)

    def format(mx):
        return '\n'.join(''.join(l) for l in mx)
    return format(mx)

def coord_add(a,b):
    return (a[0] + b[0], a[1] + b[1])

def main(fname, second):
    animation = Animation(10)
    lines = []
    line_set = set()
    with open(fname, 'r') as fp:
        for line in fp:
            split_lines = line.strip().split(' -> ')
            for pair in pairwise(map(lambda l: list(map(int, l.split(','))), split_lines)):
                pair = list(pair)
                pair.sort(key=lambda a: (a[0], a[1]))
                lines.append(pair)

                for i in range(pair[0][0], pair[1][0]+1):
                    for j in range(pair[0][1], pair[1][1]+1):
                        line_set.add((i, j))
    x_min = float('inf')
    y_min = 0 # sand
    x_max = 500 # sand
    y_max = 0
    for pair in lines:
        x_min = min(x_min, pair[0][0], pair[1][0])
        y_min = min(y_min, pair[0][1], pair[1][1])
        x_max = max(x_max, pair[0][0], pair[1][0])
        y_max = max(y_max, pair[0][1], pair[1][1])

    # Add line to the bottom
    if second:
        for i in range(500 - y_max - 2, 500 + y_max + 3):
            line_set.add((i, y_max + 2))
        # print(x_min, x_max)
        x_min = min(x_min, 500 - y_max - 2)
        x_max = max(x_max, 500 + y_max + 2)
        y_max += 2
        # print(x_min, x_max)


    current_sand = (500, 0)
    settlement = set()
    cntr = 0
    while True:
        print(cntr)
        cntr+=1
        # TODO do not break here for second
        if not second and current_sand[1] > y_max:
            break
        if second and (500, 0) in settlement:
            break
        if cntr % 25 == 0:
            draw(x_min, y_min, x_max, y_max, line_set, settlement, current_sand, animation)
        new_pos = coord_add(current_sand, (0, 1))
        if not (new_pos in settlement or new_pos in line_set):
            current_sand = new_pos
            continue
        # try diagonal
        new_pos = coord_add(current_sand, (-1, 1))
        if not (new_pos in settlement or new_pos in line_set):
            current_sand = new_pos
            continue

        new_pos = coord_add(current_sand, (1, 1))
        if not (new_pos in settlement or new_pos in line_set):
            current_sand = new_pos
            continue

        settlement.add(current_sand)
        current_sand = (500, 0)

    animation.export('src/day14/animation.gif')
    return len(settlement)


fname = 'src/day14/input.txt'

print(main(fname, False))
