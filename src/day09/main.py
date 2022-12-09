from decimal import ROUND_HALF_UP, Decimal


def disp(head, tails, size=10):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    real = int(head.real)
    imag = int(head.imag)
    grid[-1-imag][real] = 'H'
    for i, tail in enumerate(tails):
        real = int(tail.real)
        imag = int(tail.imag)
        grid[-1-imag][real] = str(i+1)
    return '\n'.join([''.join(l) for l in grid])

fname='src/day09/input.txt'
with open(fname, 'r') as fp:
    inp = fp.read()
first = False
start = 0 + 0j
head = start
tails = [start] if first else [start for _ in range(9)]
tail_coords = set([start])

directions = {
  'U': 0 + 1j,
  'D': 0 - 1j,
  'R': 1 + 0j,
  'L': -1 + 0j,
}

def custom_round(val):
    return Decimal(val).to_integral_value(rounding=ROUND_HALF_UP)

for line in inp.split('\n'):
    dir, amount = line.split(' ')
    amount = int(amount)
    for _ in range(amount):
        head += directions[dir]

        prev = head
        for i, tail in enumerate(tails):
            vector = prev - tail
            if abs(vector) > 1.5:
                vector = vector / 2
                real = vector.real
                imag = vector.imag
                real = custom_round(real)
                imag = custom_round(imag)
                new_vector = complex(real, imag)
                tail += new_vector
                if i == len(tails) - 1:
                    tail_coords.add(tail)
            tails[i] = tail
            prev = tail

print(len(tail_coords))