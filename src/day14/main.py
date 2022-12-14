


from itertools import pairwise


def draw(x_min, y_min, x_max, y_max, line_set, settlement, current_sand):
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

    def format(mx):
        mx = zip(*mx)
        return '\n'.join(''.join(l) for l in mx)
    return format(mx)

def coord_add(a,b):
    return (a[0] + b[0], a[1] + b[1])

def main(fname, second):
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
    while True:
        # TODO do not break here for second
        if not second and current_sand[1] > y_max:
            break
        if second and (500, 0) in settlement:
            break
        # print(draw(x_min, y_min, x_max, y_max, line_set, settlement, current_sand))
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

    return len(settlement)


fname = 'src/day14/input.txt'

print(main(fname, True))
