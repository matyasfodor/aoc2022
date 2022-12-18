
from itertools import cycle, islice


SHAPES = [
  [
    int('0011110', 2),
  ],
  [
    int('0001000', 2),
    int('0011100', 2),
    int('0001000', 2),
  ],
  [
    int('0000100', 2),
    int('0000100', 2),
    int('0011100', 2),
  ],
  [
    int('0010000', 2),
    int('0010000', 2),
    int('0010000', 2),
    int('0010000', 2),
  ],
  [
    int('0011000', 2),
    int('0011000', 2),
  ],
]

LINE_UPPER_LIMIT = int("10000000", 2)

def display(lines):
    ret = []
    for line in lines:
        formatted = "{0:b}".format(line).rjust(7, "0").replace("0", ".").replace("1", "@")
        ret.append(formatted)
    return ret

def display_current_state(state, offset, shape):
    return "\n".join(display(shape + [0 for _ in range(offset)] + state[::-1]))

def apply_move(shape, move):
    if move == '<':
        ret = []
        for line in shape:
            line = line << 1
            if not line < LINE_UPPER_LIMIT:
                return shape
            ret.append(line)
        return ret

    elif move == '>':        
        ret = []
        for line in shape:
            if line % 2 == 1:
                return shape
            line = line >> 1
            ret.append(line)
        return ret

def gen_movements(fname):
    with open(fname, 'r') as fp:
        instructions = fp.read().strip()
    for i, c in enumerate(instructions):
        # print("index", i)
        yield c

def collides(state, insertion, shape):
    if insertion > 0:
        working_part = state[-insertion:]
    else:
        working_part = []

    working_part.extend(0 for _ in range(len(shape) - insertion))


    for i, shape_line in enumerate(shape):
        if working_part[i] & shape_line:
            return True
    return False

def insert_to_state(state, insertion, shape):


    if insertion > 0:
        working_part = state[-insertion:]
    else:
        working_part = []
    working_part.extend(0 for _ in range(len(shape) - insertion))
    for i, shape_line in enumerate(shape):
        working_part[i] = working_part[i] | shape_line

    return (state[:-insertion] if insertion > 0 else state) + working_part

def gen_shapes(limit):
    yield from islice(cycle(SHAPES), limit)

def collision_check(container1, container2):
    for a, b in zip(container1, container2):
        if a & b > 0:
            return True
    return False

def display_containers(state_container, shape_container):
    print('\n'.join(display([a | b for a, b in zip(state_container, shape_container)])))

def main(fname, second):
    movements = cycle(gen_movements(fname))
    shapes = gen_shapes(2022)

    state = []
    pad = 3
    for shape in shapes:
        shape_container = shape + [0 for _ in range(pad + len(state))]
        state_container = [0 for _ in range(len(shape_container) - len(state))] + state[:]

        still_moving = True
        while True:
            # display_containers(state_container, shape_container)
            # print("")
            if still_moving:
                move = next(movements)
                # print("Move: ", move)
                new_shape_container = apply_move(shape_container, move)
                if collision_check(state_container, new_shape_container):
                    # print("  retract:", move)
                    pass
                else:
                    shape_container = new_shape_container

            last_item = shape_container[-1]
            new_shape_container = [0] + shape_container[:-1]
            if last_item > 0 or collision_check(state_container, new_shape_container):
                state = [a | b for a, b in zip(state_container, shape_container)]
                while state[0] == 0:
                    state.pop(0)

                break
            else:
                shape_container = new_shape_container

    # display_containers(state_container, shape_container)
    print(len(state))


fname = 'src/day17/input.txt'
second = False


main(fname, second)