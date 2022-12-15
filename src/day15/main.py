

import re

def generate_coords(fname):
    parser = r'Sensor at x=(?P<x>-?\d+), y=(?P<y>-?\d+): closest beacon is at x=(?P<x_beacon>-?\d+), y=(?P<y_beacon>-?\d+)'
    with open(fname, 'r') as fp:
        for line in fp:
            match = re.match(parser, line.strip()).groupdict()
            x = int(match['x'])
            y = int(match['y'])
            x_beacon = int(match['x_beacon'])
            y_beacon = int(match['y_beacon'])
            yield x, y, x_beacon, y_beacon
    
def main1(fname, line_of_interest):
    occupied_indices = set()
    for x, y, x_beacon, y_beacon in generate_coords(fname):
            distance = abs(x- x_beacon) + abs(y-y_beacon)

            diff = abs(y - line_of_interest)
            if diff < distance:
                ddiff = distance - diff
                rng = range(x-ddiff, x+ddiff)
                occupied_indices = occupied_indices.union(set(rng))

    print(len(occupied_indices))

def squash_ranges(ranges):
    ranges.sort(key=lambda x: x[0])
    ret = []
    for range in ranges:
        if ret and range[0] <= ret[-1][1]:
            if ret[-1][1] < range[1]:
                ret[-1][1] = range[1]
        else:
            ret.append(range)
    return ret


def main2(fname, bounds):
    lines = [e for e in generate_coords(fname)]
    for line_of_interest in range(bounds[0], bounds[1]+1):
        ranges = []
        for x, y, x_beacon, y_beacon in lines:
                distance = abs(x- x_beacon) + abs(y-y_beacon)
                diff = abs(y - line_of_interest)
                if diff < distance:
                    ddiff = distance - diff
                    ranges.append([x-ddiff, x+ddiff+1])
        ranges = squash_ranges(ranges)
        for current_range in ranges:
            if bounds[0] < current_range[0] or current_range[1]<=bounds[1]:
                print(line_of_interest, ranges)

fname = 'src/day15/input.txt'


# main1(fname, 2000000)
# main2('src/day15/input.txt', (0, 4000000))
main2('src/day15/test.txt', (0, 20))

# y         x
# 3429555 + 2749047 * 4000000
# 11      + 14 * 4000000
