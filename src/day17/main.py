
from itertools import cycle, islice
from more_itertools import peekable


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
    for c in instructions:
        yield c

def collides(state, insertion, shape):
    if insertion > 0:
        working_part = state[-insertion:]
    else:
        working_part = []

    working_part.extend(0 for _ in range(len(shape) - insertion))

    # print('working_part', working_part, insertion)

    for i, shape_line in enumerate(shape):
        if working_part[i] & shape_line:
            return True
    return False

def insert_to_state(state, insertion, shape):
    # only need to deal with "outstanding" parts

    # 1. take last insertion lines from state
    # 2. extend it to len shape
    # 3. simply add shape to thsi working sprite
    # 4. remove overlappign lines from state
    # 5. add working sprite

    if insertion > 0:
        working_part = state[-insertion:]
    else:
        working_part = []
    # print("Shape :", display(shape[::-1]))
    # print("Working part:", display(working_part[::-1]))
    working_part.extend(0 for _ in range(len(shape) - insertion))
    # print("Working part:", display(working_part[::-1]))
    for i, shape_line in enumerate(shape):
        working_part[i] = working_part[i] | shape_line
    # print("Working part:", display(working_part[::-1]))

    # print("State", display(state[::-1]))
    # print("\n")
    # print("State", display(state[:-insertion][::-1]))

    return (state[:-insertion] if insertion > 0 else state) + working_part

def gen_shapes(limit):
    yield from islice(cycle(SHAPES), limit)

def main(fname, second):
    movements = peekable(gen_movements(fname))
    shapes = gen_shapes(2022)

    state = []
    for shape in islice(shapes, 5):
        display_current_state(state, 3, shape)
        # print("new shape", shape)
        # print(display(shape))
        # print('\n')
        for i, move in enumerate(islice(movements, 3)):
            shape = apply_move(shape, move)
            print(display_current_state(state, 3 - i, shape))
            print('\n')

        insertion = 0
        still_moving = True
        while True:
            if still_moving:
                next_move = next(movements)
                next_shape = apply_move(shape, next_move)
                if collides(state, insertion, next_shape):
                    movements.prepend(next_move)
                    still_moving = False
                else:
                    shape = next_shape

            # print("try inserting", insertion, len(state), insertion + 1 < len(state))

            if insertion + 1 >= len(state) or collides(state, insertion + 1, shape):
                break
            insertion += 1


        # insertion = 0
        # is_moving = True
        # while insertion < len(state):
        #     if is_moving:
        #         move = next(movements)
        #         new_shape = apply_move(shape, move)
        #         if collides(state, insertion, shape):
        #             is_moving = False
        #             movements.prepend(move)
        #         else:
        #             shape = new_shape
            
            
            # try insertion
            # if successfull, progress
            # if unsuccesfull, backtrack
            # pass
            # try to move
        # print("Insertion", insertion)

        # print("\nbefore\n")
        # print("\n".join(display(state[::-1])))
        # print("\n")

        state = insert_to_state(state, insertion, shape[::-1])
        # print("\n")
        # print("\n".join(display(state[::-1])))
        # print("\n")
    print("################")
    print("################\n")
    print("\n".join(display(state[::-1])))


fname = 'src/day17/test.txt'
second = False


main(fname, second)