from bearlibterminal import terminal
from bresenham import bresenham
from textwrap import wrap
from tile import Tile
from utils import DrawingMode, print_terminal

class VidaBlue:
  def __init__(self):
    self.tiles = {}
    for x in range(32):
      for y in range(32):
        self.tiles[(x, y)] = Tile('.')

    self.draw_mode = DrawingMode.char

    self.curr_char = 'x'
    self.other_char = '.'

    self.cursor_x = 0
    self.cursor_y = 0

    self.info_x_start = 32
    self.info_y_start = 0

    self.line_start_x = 0
    self.line_start_y = 0

    self.line_end_x = 0
    self.line_end_y = 0

    self.first_line_point_set = False

  def update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_ESCAPE:
      if self.first_line_point_set:
        self.first_line_point_set = False
      else:
        running = False

    elif key == terminal.TK_UP:
      if self.cursor_y - 1 >= 0:
        self.cursor_y -= 1
    elif key == terminal.TK_DOWN:
      if self.cursor_y + 1 <= 31:
        self.cursor_y += 1
    elif key == terminal.TK_LEFT:
      if self.cursor_x - 1 >= 0:
        self.cursor_x -= 1
    elif key == terminal.TK_RIGHT:
      if self.cursor_x + 1 <= 31:
        self.cursor_x += 1
    
    # Change to call code to save to file in the pause menu
    # This is placing the current tile, then saving the map
    elif terminal.check(terminal.TK_CONTROL) and key == terminal.TK_S:
      f = open('map_out.txt', 'w')
      map_str = ""
      for tile in self.tiles.values():
        map_str += tile.ch
      formatted_map_str = "\n".join(wrap(map_str, 32))
      f.write(formatted_map_str)
      f.close()

    elif key == terminal.TK_CONTROL:
      if self.draw_mode == DrawingMode.char:
        current_tile = self.tiles[(self.cursor_x, self.cursor_y)]
        current_tile.ch = self.curr_char
        self.tiles[(self.cursor_x, self.cursor_y)] = current_tile
      elif self.draw_mode == DrawingMode.line:
        if self.first_line_point_set:
          self.line_end_x = self.cursor_x
          self.line_end_y = self.cursor_y

          pts = list(bresenham(self.line_start_x, self.line_start_y, self.line_end_x, self.line_end_y))

          for pt in pts:
            tile = self.tiles[pt]
            tile.ch = self.curr_char
            self.tiles[pt] = tile

          self.first_line_point_set = False
        else:
          self.first_line_point_set = True
          self.line_start_x = self.cursor_x
          self.line_start_y = self.cursor_y

    elif key == terminal.TK_SHIFT:
      swap = self.curr_char
      self.curr_char = self.other_char
      self.other_char = swap

    elif key == terminal.TK_LBRACKET:
      if self.draw_mode == DrawingMode.char:
        self.draw_mode = DrawingMode.line
      elif self.draw_mode == DrawingMode.line:
        self.draw_mode = DrawingMode.char
    elif key == terminal.TK_RBRACKET:
      if self.draw_mode == DrawingMode.char:
        self.draw_mode = DrawingMode.line
      elif self.draw_mode == DrawingMode.line:
        self.draw_mode = DrawingMode.char

    elif terminal.check(terminal.TK_WCHAR):
      char_pressed = chr(terminal.state(terminal.TK_WCHAR))
      self.other_char = self.curr_char
      self.curr_char = char_pressed

    return running

  def draw(self):
    terminal.clear()

    for ((posx, posy), t) in self.tiles.items():
      print_terminal(posx, posy, t.ch, 'white')

      current_tile_ch = self.tiles[(self.cursor_x, self.cursor_y)].ch
      print_terminal(self.cursor_x, self.cursor_y, '%s[+]%s' % (current_tile_ch, self.curr_char), 'white')

    if self.first_line_point_set:
      pts = list(bresenham(self.line_start_x, self.line_start_y, self.cursor_x, self.cursor_y))

      for pt in pts:
        print_terminal(pt[0], pt[1], self.curr_char, 'white')

    # Determine draw mode char
    draw_mode_char = ''
    if self.draw_mode == DrawingMode.char:
      draw_mode_char = 'c'
    elif self.draw_mode == DrawingMode.line:
      draw_mode_char = '\\'

    # Draw info screen
    print_terminal(self.info_x_start, self.info_y_start, 'ctrl: %s' % self.curr_char, 'white')
    print_terminal(self.info_x_start, self.info_y_start + 1, 'hold: %s' % self.other_char, 'white')
    print_terminal(self.info_x_start, self.info_y_start + 2, 'cursor: (%s, %s)' % (self.cursor_x, self.cursor_y), 'white')
    print_terminal(self.info_x_start, self.info_y_start + 3, 'draw mode: [[%s]]' % (draw_mode_char), 'white')
    print_terminal(self.info_x_start, self.info_y_start + 4, '%s' % self.tiles[(self.cursor_x, self.cursor_y)].ch, 'white')
    terminal.refresh()