

from collections import defaultdict
from functools import lru_cache
import hashlib
from itertools import pairwise, permutations
from PIL import Image, ImageDraw
import random
import re


def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

@lru_cache()
def get_ordering_color(ordering):

    hash_value = abs(hash(ordering)) % 1000
    print(hash_value)
    color = rgb(0, 1000, hash_value)
    return color


class Animation:
    def __init__(self, cell_size) -> None:
        self.frames = []
        self.cell_size = cell_size

    def add_frame(self, pool, max_so_far):
        pool = pool[::-1]
        height = len(pool)
        width = len(pool[0][0]) + 4
        # height = len(mx)
        # width = len(mx[0])
        image = Image.new("RGB", (width*self.cell_size, height*self.cell_size), "black")
        draw = ImageDraw.Draw(image)
        for i, (ordering, cost) in enumerate(pool):
            # color = #get_ordering_color(tuple(ordering))
            color = rgb(0, max_so_far, cost)
            for j, e in enumerate(ordering):
                draw.text((j*self.cell_size, i*self.cell_size), text=str(e), fill=color)

            draw.text(((j+2) * self.cell_size, i*self.cell_size), text=str(cost))
        self.frames.append(image)

    def export(self, fname):
        frame_one = self.frames[0]
        subsample = None
        frames = [f for i, f in enumerate(self.frames) if subsample is None or i % subsample == 0]
        print('start save')
        frame_one.save(fname, format="GIF", append_images=frames,
                    save_all=True, duration=250, loop=0)
        print('saved')
        


def dfs(graph):
    @lru_cache()
    def inner(current, open_valves, current_rate, cum_rate, minutes):
        print(current, open_valves, current_rate, cum_rate, minutes)
        if minutes <= 0:
            return cum_rate
        # print('graph[current]["targets"]', graph[current]['targets'])
        res = [inner(t, open_valves, current_rate, cum_rate + current_rate, minutes -time) for t, time in graph[current]['targets']]
        if graph[current]['rate'] > 0 and current not in open_valves:
            open_valves = open_valves.union(frozenset(current))
            current_rate += graph[current]['rate']
            minutes -= 1
            if minutes > 0:
                res.extend(inner(t, open_valves, current_rate, cum_rate + current_rate, minutes-time) for t, time in graph[current]['targets'])
        # print(current, open_valves, current_rate, cum_rate, minutes)
        # try:
        ret = max(res)
        # except:

        return ret

    return inner('AA', frozenset(), 0, 0, 30)

def solver2(graph):
    current = 'AA'
    visited = set([current])
    rate = 0
    agg = 0
    minutes_left = 30
    while minutes_left > 0:
        current_node = graph[current]
        targets = [(t,d) for (t,d) in current_node['targets'] if t not in visited and d < minutes_left]
        if not targets:
            break
        # targets.sort()
        targets = list(map(lambda e: [e[0], e[1], (1.0 * graph[e[0]]['rate']) / e[1]], targets))
        print(targets, current)
        (current, distance, _) = max(targets, key=lambda x:x[2])
        visited.add(current)
        agg += rate * (distance+1)
        rate += graph[current]['rate']
        minutes_left -= (distance+1)

    agg += minutes_left*rate
    print(visited, rate, agg)


def get_agg(graph,distance_matrix, ordering, minutes):
    current_time = 0
    ret = 0
    current_rate = 0
    for s, t in pairwise(ordering):
        # print(current_time, current_rate, ret)
        travel_time = distance_matrix[s][t]+1
        if current_time + travel_time < minutes:
            ret += travel_time * current_rate
            current_rate += graph[t]['rate']
            current_time += travel_time
        else:
            break

    ret += (minutes - current_time) * current_rate
    return ret

def solver3(graph, distance_matrix):
    keys = graph.keys()
    keys = [k for k in keys if k != 'AA']
    current_max = 0
    for perm in permutations(keys):
        ordering = ['AA'] + list(perm)
        current_agg = get_agg(graph, distance_matrix, ordering, 30)
        current_max = max(current_agg, current_max)
    return current_max

def shuffle(arr):
    ret = arr[:]
    random.shuffle(ret)
    return ret

def solver4(graph, distance_matrix, second):
    # task: find the best ordering for a given set of keys

    animation = Animation(20)

    time = 26 if second else 30

    keys = graph.keys()
    keys = [k for k in keys if k != 'AA']

    @lru_cache()
    def cost_function(ordering):
        if second:
            half = int(len(ordering) / 2.0)
            first_half = ['AA'] + list(ordering[:half])
            second_half = ['AA'] + list(ordering[half:])
            return get_agg(graph, distance_matrix, first_half, time) + get_agg(graph, distance_matrix, second_half, time)
        else:
            ordering = ['AA'] + list(ordering)
            return get_agg(graph, distance_matrix, ordering, time)

    def mutation(ordering):
        i1 = random.randint(0, len(ordering)-1)
        i2 = random.randint(0, len(ordering)-2)
        if i2 == i1:
            i2 = len(ordering)-1
        ret = ordering[:]
        t1 = ordering[i1]
        t2 = ordering[i2]
        ret[i1] = t2
        ret[i2] = t1
        return ret

    best_score = 0
    for i in range(1):
        random.seed(i)
        num_generations = 100
        pool_size = 10
        # keep = 0.5

        pool = [shuffle(keys) for _ in range(pool_size)]
        for _ in range(num_generations):
            # pool_with_values = [(p, cost_function(p)) for p in pool]
            new_generation = [mutation(p) for p in pool]
            pool.extend(new_generation)
            pool_with_values = [(p, cost_function(tuple(p))) for p in pool]
            # pool_with_values.
            wild_types = [shuffle(keys) for _ in range(pool_size)]
            pool_with_values.extend(((p, cost_function(tuple(p))) for p in wild_types))
            # animation.add_frame(pool_with_values)
            pool_with_values.sort(key=lambda x: x[1])
            animation.add_frame(pool_with_values, 1600)
            # print('Best in current gen:', pool_with_values[-1])
            best_score = max(best_score, pool_with_values[-1][1])
            print(best_score)
            pool = [p for (p, _) in pool_with_values[-pool_size:]]

    animation.export('src/day16/animation.gif')

    return best_score

def solver5(graph, distance_matrix):
    keys = graph.keys()
    keys = [k for k in keys if k != 'AA']
    keys.sort(key=lambda k: -graph[k]['rate'])

    @lru_cache()
    def cost_function(ordering):
        ordering = ['AA'] + list(ordering)
        return get_agg(graph, distance_matrix, ordering, 30)

    print(keys)
    print(cost_function(tuple(keys)))

def get_distance(graph, k1, k2):
    visited = set()
    queue = [(k1, 0)]
    while queue:
        current, distance = queue.pop(0)
        if k2 == current:
            return distance
        neighbors = graph[current]['targets']
        for (n, d) in neighbors:
            # print(queue, visited, n)
            if n not in visited:
                queue.append((n, distance + d))
                visited.add(n)

def contract(graph, default_keepers):
    keepers = [*default_keepers]
    for key in graph.keys():
        if graph[key]['rate'] > 0:
            keepers.append(key)
    # Computeroutes between keepers
    ret = {}
    for k1 in keepers:
        ret[k1] = {**graph[k1]}
        ret[k1]['targets'] = []
        for k2 in keepers:
            if k1 == k2:
                continue
            distance = get_distance(graph, k1, k2)
            ret[k1]['targets'].append((k2, distance))
    return ret


def main(fname):
    graph = {}
    pattern = r'Valve (?P<source>\S+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<targets>(([A-Z]+)(, )?)+)'
    with open(fname, 'r') as fp:
        for line in fp:
            match = re.match(pattern, line.strip())
            match_dict = match.groupdict()
            source = match_dict['source']
            rate = int(match_dict['rate'])
            targets = list(map(lambda x: (x, 1), match_dict['targets'].split(', ')))
            graph[source] = {
                'rate': rate,
                'targets': targets
            }


    # print(get_distance(graph, 'AA', 'JJ'))
    # pprint(graph)
    graph = contract(graph, ['AA'])
    # pprint(graph)

    distance_matrix = defaultdict(dict)
    for s in graph.keys():
        for t, d in graph[s]['targets']:
            distance_matrix[s][t] = d
    second = False

    print(solver4(graph, distance_matrix, second))
    # print(get_agg(graph, distance_matrix, ['AA', 'MD', 'DS', 'YW', 'SS', 'FS', 'KI', 'SQ', 'PZ', 'TX', 'HG', 'IK', 'JE', 'IT', 'YB', 'CR'], 30))


fname = 'src/day16/input.txt'

main(fname)
# 1624 - too high
# 1469 - too low
# 1574 - too low


# 1579 - not

# 1580 - not checked

# Best: ['MD', 'DS', 'YW', 'SS', 'FS', 'KI', 'SQ', 'PZ', 'TX', 'HG', 'IK', 'JE', 'IT', 'YB', 'CR']