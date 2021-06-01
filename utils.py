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

def print_terminal(x, y, g, c):
  old_color = terminal.TK_COLOR
  terminal.color(c)
  terminal.printf(x, y, g)
  terminal.color(old_color)