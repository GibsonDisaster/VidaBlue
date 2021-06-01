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

def print_terminal(x, y, g, c):
  old_color = terminal.TK_COLOR
  terminal.color(c)
  terminal.printf(x, y, g)
  terminal.color(old_color)

def get_text_input():
  res = ''

  while not terminal.check(terminal.TK_ENTER):
    if terminal.check(terminal.TK_WCHAR):
      char_pressed = chr(terminal.state(terminal.TK_WCHAR))
      res += char_pressed

  print(res)