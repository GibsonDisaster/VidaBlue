from bearlibterminal import terminal
from tile import Tile
from utils import print_terminal

class VidaBlue:
  def __init__(self):
    self.tiles = {}
    for x in range(32):
      for y in range(32):
        self.tiles[(x, y)] = Tile('.')

    self.curr_char = 'x'
    self.other_char = '.'

    self.cursor_x = 0
    self.cursor_y = 0

  def update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_ESCAPE:
      running = False

    return running

  def draw(self):
    terminal.clear()

    for ((posx, posy), t) in self.tiles.items():
      print_terminal(posx, posy, t.ch, 'white')

    print_terminal(0, 0, '#', 'white')

    terminal.refresh()