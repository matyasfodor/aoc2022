import re

first = False
fname = 'src/day04/input.txt'

def get_stacks(stack_lines):
  stacks = []
  for stack_line in stack_lines[::-1]:
    parts = []
    while len(stack_line) > 0:
      e = stack_line[:4]
      stack_line = stack_line[4:]
      # print(e)
      if e.startswith('['):
        parts.append(e[1])
      else:
        parts.append(None)
    # parts = stack_line.replace('\n', '').replace('    ', ' . ').split(' ')
    # print('asd', parts)
    stacks.append(parts)
  stacks = list(map(lambda x: list(filter(lambda y: y is not None, x)), zip(*stacks)))
  return stacks

def apply_move_first(stack, move):
  match = re.match('move (\d+) from (\d+) to (\d+)', move)
  quantity, from_col, to_col = map(int, match.groups())
  for _ in range(quantity):
    el = stack[from_col-1].pop()
    stack[to_col-1].append(el)
  return stack

def apply_move_second(stack, move):
  match = re.match('move (\d+) from (\d+) to (\d+)', move)
  quantity, from_col, to_col = map(int, match.groups())
  moved_items = stack[from_col-1][-quantity:]
  stack[from_col-1] = stack[from_col-1][:-quantity]
  stack[to_col-1].extend(moved_items)
  # for _ in range(quantity):
  #   el = stack[from_col-1].pop()
  #   stack[to_col-1].append(el)
  return stack

def get_top_elements(stack):
  return ''.join(e[-1] for e in stack)

with open(fname, 'r') as fp:
  stack_lines = []
  move_lines = []
  for line in fp:
    if line.strip().startswith('['):
      stack_lines.append(line)
    if line.startswith('move'):
      move_lines.append(line)

  apply_move = apply_move_first if first else apply_move_second

  stacks = get_stacks(stack_lines)
  for move in move_lines:
    stacks = apply_move(stacks, move)
  top_elements = get_top_elements(stacks)
  print(top_elements)