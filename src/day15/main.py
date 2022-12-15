

import re


def main(fname, line_of_interest):
    parser = r'Sensor at x=(?P<x>-?\d+), y=(?P<y>-?\d+): closest beacon is at x=(?P<x_beacon>-?\d+), y=(?P<y_beacon>-?\d+)'
    occupied_indices = set()
    with open(fname, 'r') as fp:
        for line in fp:
            match = re.match(parser, line.strip()).groupdict()
            x = int(match['x'])
            y = int(match['y'])
            x_beacon = int(match['x_beacon'])
            y_beacon = int(match['y_beacon'])

            distance = abs(x- x_beacon) + abs(y-y_beacon)

            diff = abs(y - line_of_interest)
            if diff < distance:
                ddiff = distance - diff
                rng = range(x-ddiff, x+ddiff)
                # print(f'Sensor x={x} y={y} distance={distance} diff={diff} rng={rng}')
                occupied_indices = occupied_indices.union(set(rng))

    print(len(occupied_indices))




fname = 'src/day15/input.txt'


main(fname, 2000000)