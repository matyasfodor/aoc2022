
fname = 'src/day10/input.txt'

first = False

aggregate_val = 0

cycle_counter = 0
current_value = 1
prev_value = None

cycle_of_interest = [20, 60, 100, 140, 180, 220]
cycle_of_interest_iter = iter(cycle_of_interest)
current_cycle_to_track = next(cycle_of_interest_iter)
prev_cycle = None
with open(fname, 'r') as fp:
    for i, line in enumerate(fp):
        line = line.strip()
        if line == 'noop':
            cycle_counter += 1
        elif line.startswith('addx'):
            _, num = line.split(' ')
            num = int(num)
            cycle_counter += 2
            current_value += num

        if prev_cycle is not None and prev_value is not None and current_cycle_to_track is not None and prev_cycle < current_cycle_to_track <= cycle_counter:
            # print('aggregate_val += prev_value * current_cycle_to_track', aggregate_val, prev_value, current_cycle_to_track, line, prev_cycle, cycle_counter, i)
            aggregate_val += prev_value * current_cycle_to_track
            try:
                current_cycle_to_track = next(cycle_of_interest_iter)
            except StopIteration:
                current_cycle_to_track = None

        prev_value = current_value
        prev_cycle = cycle_counter

print(aggregate_val)
