from enum import Enum
from bearlibterminal import terminal

class DrawingMode(Enum):
  char = 0
  line = 1

class EditMode(Enum):
  chars = 0
  solidity = 1
  interactable = 2
  color = 3
  paused = 4
  save = 5
  load = 6
  properties = 7

def print_terminal(x, y, g, c):
  old_color = terminal.TK_COLOR
  terminal.color(c)
  terminal.printf(x, y, g)
  terminal.color(old_color)

def create_properties_str(x, y, name, desc):
  return '%s,%s,%s,%s' % (x, y, name, desc)

def read_properties_file(filepath):
  result = []
  with open(filepath, "r") as fp:
      for i in fp.readlines():
          tmp = i.split(",")
          try:
              result.append((int(tmp[0]), int(tmp[1]), str(tmp[2]), str(tmp[3])))
          except:pass

  return result