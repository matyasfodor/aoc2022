

from collections import defaultdict
from functools import lru_cache
from itertools import pairwise, permutations
from pprint import pprint
import random
import re


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

def solver4(graph, distance_matrix):
    # task: find the best ordering for a given set of keys

    keys = graph.keys()
    keys = [k for k in keys if k != 'AA']

    @lru_cache()
    def cost_function(ordering):
        ordering = ['AA'] + list(ordering)
        return get_agg(graph, distance_matrix, ordering, 30)

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
    for i in range(1000):
        random.seed(i)
        num_generations = 100
        pool_size = 40
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
            pool_with_values.sort(key=lambda x: x[1])
            # print('Best in current gen:', pool_with_values[-1])
            best_score = max(best_score, pool_with_values[-1][1])
            print(best_score)
            pool = [p for (p, _) in pool_with_values[-pool_size:]]

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

    print(solver4(graph, distance_matrix))
    # print(get_agg(graph, distance_matrix, ['AA', 'MD', 'DS', 'YW', 'SS', 'FS', 'KI', 'SQ', 'PZ', 'TX', 'HG', 'IK', 'JE', 'IT', 'YB', 'CR'], 30))


fname = 'src/day16/input.txt'

main(fname)
# 1624 - too high
# 1469 - too low
# 1574 - too low


# 1579 - not

# 1580 - not checked

# Best: ['MD', 'DS', 'YW', 'SS', 'FS', 'KI', 'SQ', 'PZ', 'TX', 'HG', 'IK', 'JE', 'IT', 'YB', 'CR']