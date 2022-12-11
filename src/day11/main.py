from collections import defaultdict
from pprint import pformat

import numpy as np

fname = 'src/day11/input.txt'

class Monkey:
    def __init__(self, name, items, operation, operation_const, test_const, if_true_monkey, if_false_monkey) -> None:
        self.name = name
        self.items = items
        self.operation = operation
        self.operation_const = operation_const
        self.test_const = test_const
        self.if_true_monkey = if_true_monkey
        self.if_false_monkey = if_false_monkey
        self.activity = 0

    def __repr__(self) -> str:
        return pformat(vars(self))

    def next_round(self, second, divisor):
        update = defaultdict(list)
        for worry_level in self.items:
            operand1 = worry_level
            operand2 = worry_level if self.operation_const is None else self.operation_const
            worry_level = operand1 * operand2 if self.operation == 'MULTIPLY' else operand1 + operand2

            if second:
                worry_level = worry_level % divisor
            else:
                worry_level = int(worry_level / 3.0)
            target = self.if_true_monkey if worry_level % self.test_const == 0 else self.if_false_monkey
            update[target].append(worry_level)
            self.activity += 1
        self.items = []
        return update

    def update(self, items):
        self.items = self.items + items
            

def parse_monkey(title,starting_items, operation_line,test_line, if_true, if_false):
    _, starting_items = starting_items.split(':')
    starting_items = list(map(int, starting_items.strip().split(', ')))

    # Operation: new = old * 19 - we only need the last two items
    operation_line_parts = operation_line.strip().split(' ')
    operation = 'MULTIPLY' if operation_line_parts[-2] == '*' else 'ADDITON'
    if operation_line_parts[-1] == 'old':
        operation_const = None
    else:
        operation_const = int(operation_line_parts[-1])
    
    test_line_parts = test_line.strip().split(' ')
    test_const = int(test_line_parts[-1])

    if_true_monkey = int(if_true.strip().split(' ')[-1])
    if_false_monkey = int(if_false.strip().split(' ')[-1])
    return Monkey(title, starting_items, operation, operation_const, test_const, if_true_monkey, if_false_monkey)

second = True
monkeys = []
with open(fname, 'r') as fp:
    while True:
        title = next(fp)
        starting_items = next(fp)
        operation = next(fp)
        test = next(fp)
        if_true = next(fp)
        if_false = next(fp)
        monkey = parse_monkey(title,starting_items, operation,test, if_true, if_false)
        monkeys.append(monkey)
        try:
            next(fp)
        except StopIteration:
            break

test_const_prod = 1
for m in monkeys:
    test_const_prod *= m.test_const

print(test_const_prod)

for current_round in range(10000 if second else 20):
    for monkey_i in range(len(monkeys)):
        update = monkeys[monkey_i].next_round(second, test_const_prod)
        for key in update.keys():
            monkeys[key].update(update[key])
    
    if (current_round + 1) in [1, 20, 1000, 2000]:
        print('round ', current_round)
        print('Monkeys', [m.activity for m in monkeys])
        print('\n')

elements = sorted([m.activity for m in monkeys])[-2:]
print(elements)
print(elements[0] * elements[1])