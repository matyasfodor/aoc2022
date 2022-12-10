
fname = 'src/day10/input.txt'


def prev_solution(fname):
    aggregate_val = 0

    cycle_counter = 0
    current_value = 1
    prev_value = None

    cycle_of_interest = [20, 60, 100, 140, 180, 220]
    cycle_of_interest_iter = iter(cycle_of_interest)
    current_cycle_to_track = next(cycle_of_interest_iter)
    prev_cycle = None
    with open(fname, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line == 'noop':
                cycle_counter += 1
            elif line.startswith('addx'):
                _, num = line.split(' ')
                num = int(num)
                cycle_counter += 2
                current_value += num

            if prev_cycle is not None and prev_value is not None and current_cycle_to_track is not None and prev_cycle < current_cycle_to_track <= cycle_counter:
                aggregate_val += prev_value * current_cycle_to_track
                try:
                    current_cycle_to_track = next(cycle_of_interest_iter)
                except StopIteration:
                    current_cycle_to_track = None

            prev_value = current_value
            prev_cycle = cycle_counter

    return aggregate_val

def new_solution(fname, second):
    if second:
        lines = [['.' for _ in range(40)] for _ in range(6)]
        current_line_no = -1
    else:
        aggregate_val = 0
    current_value = 1
    instruction_length = 0
    increment_value = 0
    cycle = 0
    cycle_of_interest = [20, 60, 100, 140, 180, 220]
    with open(fname, 'r') as fp:
        while True:
            if instruction_length == 0:
                current_value += increment_value
                try:
                    line = next(fp).strip()
                except StopIteration:
                    break
                if line == 'noop':
                    instruction_length = 0
                    increment_value = 0
                elif line.startswith('addx'):
                    _, num = line.split(' ')
                    num = int(num)
                    instruction_length = 1
                    increment_value = num
            else:
                instruction_length -= 1

            cycle += 1

            if second:
                pos = (cycle - 1) % 40
                if pos == 0:
                    current_line_no += 1

                if pos - 2 < current_value <= pos + 1:
                    lines[current_line_no][pos] = '#'
            else:
                if cycle in cycle_of_interest:
                    aggregate_val += current_value * cycle

    if second:
        aggregate_val = '\n'.join(''.join(l) for l in lines)
    return aggregate_val


print(new_solution(fname, second=True))