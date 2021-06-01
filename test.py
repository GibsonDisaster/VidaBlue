t = {}

for x in range(10):
  for y in range(10):
    t[(x, y)] = '.'

for pos, val in t.items():
  print(pos)