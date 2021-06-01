from bearlibterminal import terminal
from bresenham import bresenham
from textwrap import wrap
from tile import Tile
from utils import DrawingMode, EditMode, get_text_input, print_terminal

class VidaBlue:
  def __init__(self):
    self.tiles = {}
    for x in range(32):
      for y in range(32):
        self.tiles[(x, y)] = Tile('.')

    self.draw_mode = DrawingMode.char
    self.edit_mode = EditMode.chars

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

    self.colors = ["white", "gray", "red","flame","orange","amber","yellow","lime","chartreuse","green","sea","turquoise","cyan","sky","azure","blue","han","violet","purple","fuchsia","magenta","pink","crimson","transparent"]
    self.color_index = 0

    self.paused_index = 0

  def update(self):
    running = True

    if self.edit_mode == EditMode.chars:
      running = self.chars_update()
    elif self.edit_mode == EditMode.solidity:
      running = self.solidity_update()
    elif self.edit_mode == EditMode.interactable:
      running = self.interact_update()
    elif self.edit_mode == EditMode.color:
      running = self.color_update()
    elif self.edit_mode == EditMode.paused:
      running = self.paused_update()
    elif self.edit_mode == EditMode.save:
      running = self.save_update()
    elif self.edit_mode == EditMode.load:
      running = self.load_update()

    return running

  def chars_update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_ESCAPE:
      if self.first_line_point_set:
        self.first_line_point_set = False
      else:
        self.edit_mode = EditMode.paused

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

    elif key == terminal.TK_CONTROL:
      if self.draw_mode == DrawingMode.char:
        current_tile = self.tiles[(self.cursor_x, self.cursor_y)]
        current_tile.ch = self.curr_char
        current_tile.color = self.colors[self.color_index]
        self.tiles[(self.cursor_x, self.cursor_y)] = current_tile
      elif self.draw_mode == DrawingMode.line:
        if self.first_line_point_set:
          self.line_end_x = self.cursor_x
          self.line_end_y = self.cursor_y

          pts = list(bresenham(self.line_start_x, self.line_start_y, self.line_end_x, self.line_end_y))

          for pt in pts:
            tile = self.tiles[pt]
            tile.ch = self.curr_char
            tile.color = self.colors[self.color_index]
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

    elif terminal.check(terminal.TK_ALT):
      self.edit_mode = EditMode.color

    elif terminal.check(terminal.TK_TAB):
      self.edit_mode = EditMode.solidity

    return running

  def solidity_update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_ESCAPE:
      if self.first_line_point_set:
        self.first_line_point_set = False
      else:
        self.edit_mode = EditMode.paused

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

    elif key == terminal.TK_CONTROL:
      if self.draw_mode == DrawingMode.char:
        tile = self.tiles[(self.cursor_x, self.cursor_y)]
        tile.solid = not tile.solid
        self.tiles[(self.cursor_x, self.cursor_y)] = tile
      elif self.draw_mode == DrawingMode.line:
        if self.first_line_point_set:
          self.line_end_x = self.cursor_x
          self.line_end_y = self.cursor_y

          pts = list(bresenham(self.line_start_x, self.line_start_y, self.line_end_x, self.line_end_y))

          for pt in pts:
            tile = self.tiles[pt]
            tile.solid = not tile.solid
            self.tiles[pt] = tile

          self.first_line_point_set = False
        else:
          self.first_line_point_set = True
          self.line_start_x = self.cursor_x
          self.line_start_y = self.cursor_y

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

    elif terminal.check(terminal.TK_TAB):
      self.edit_mode = EditMode.interactable

    return running

  def interact_update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_ESCAPE:
      if self.first_line_point_set:
        self.first_line_point_set = False
      else:
        self.edit_mode = EditMode.paused

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

    elif key == terminal.TK_CONTROL:
      if self.draw_mode == DrawingMode.char:
        tile = self.tiles[(self.cursor_x, self.cursor_y)]
        tile.interact = not tile.interact
        self.tiles[(self.cursor_x, self.cursor_y)] = tile
      elif self.draw_mode == DrawingMode.line:
        if self.first_line_point_set:
          self.line_end_x = self.cursor_x
          self.line_end_y = self.cursor_y

          pts = list(bresenham(self.line_start_x, self.line_start_y, self.line_end_x, self.line_end_y))

          for pt in pts:
            tile = self.tiles[pt]
            tile.interact = not tile.interact
            self.tiles[pt] = tile

          self.first_line_point_set = False
        else:
          self.first_line_point_set = True
          self.line_start_x = self.cursor_x
          self.line_start_y = self.cursor_y

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

    elif terminal.check(terminal.TK_TAB):
      self.edit_mode = EditMode.chars

    return running

  def color_update(self):
    key = terminal.read()
    running = True

    if key == terminal.TK_UP:
      if self.color_index == 0:
        self.color_index = len(self.colors) - 1
      else:
        self.color_index -= 1
    elif key == terminal.TK_DOWN:
      if self.color_index == len(self.colors) - 1:
        self.color_index = 0
      else:
        self.color_index += 1
    
    if terminal.check(terminal.TK_ALT):
      self.edit_mode = EditMode.chars

    return running

  def paused_update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_UP:
      if self.paused_index == 0:
        self.paused_index = 3
      else:
        self.paused_index -= 1
    elif key == terminal.TK_DOWN:
      if self.paused_index == 4:
        self.paused_index = 0
      else:
        self.paused_index += 1

    elif terminal.check(terminal.TK_CONTROL):
      if self.paused_index == 0: # Return to map
        self.edit_mode = EditMode.chars
      elif self.paused_index == 1: # Save map
        # Code to open window to input map name
        import easygui
  
        # message to be displayed
        message = "Please name file without whitespace"
          
        # window title
        title = "Save map as..."
          
        # long text
        text = [""]
                  
        # creating a multi password box
        map_name = easygui.textbox(message, title, text)

        # Save tile chars to file
        f = open('out/%s.txt' % map_name, 'w+')
        map_str = ""
        for y in range(32):
          for x in range(32):
            map_str += self.tiles[(x, y)].ch
        formatted_map_str = "\n".join(wrap(map_str, 32))
        f.write(formatted_map_str)
        f.close()

        print(map_str)

        # Save tile solidity to file
        f = open('out/%s_solidity.txt' % map_name, 'w+')
        map_str = ""
        for y in range(32):
          for x in range(32):
            tile = self.tiles[(x, y)]
            if tile.solid:
              map_str += '1'
            else:
              map_str += '0'
        formatted_map_str = "\n".join(wrap(map_str, 32))
        f.write(formatted_map_str)
        f.close()

        # Save tile interactability to file
        f = open('out/%s_interact.txt' % map_name, 'w+')
        map_str = ""
        for y in range(32):
          for x in range(32):
            tile = self.tiles[(x, y)]
            if tile.interact:
              map_str += '1'
            else:
              map_str += '0'
        formatted_map_str = "\n".join(wrap(map_str, 32))
        f.write(formatted_map_str)
        f.close()
      elif self.paused_index == 2: # Load map
        import easygui

        map_path = easygui.fileopenbox(title='map file')
        solid_path = easygui.fileopenbox(title='map solidity file')
        interact_path = easygui.fileopenbox(title='map interact file')

        # Load tiles with chars from map_path
        char_mapf = open(map_path, 'r').read()
        
        x, y = 0, 0
        for line in char_mapf:
          for char in line:
            if char == '\n':
              y += 1
              x = 0
            else:
              tile = self.tiles[(x, y)]
              tile.ch = char
              self.tiles[(x, y)] = tile
              x += 1

        # Load tiles with solidity from solid_path
        solid_mapf = open(solid_path, 'r').read()
        
        x, y = 0, 0
        for line in solid_mapf:
          for char in line:
            if char == '\n':
              y += 1
              x = 0
            else:
              tile = self.tiles[(x, y)]
              if char == '0':
                tile.solid = False
              else:
                tile.solid = True
              self.tiles[(x, y)] = tile
              x += 1

        # Load tiles with interact from interact_path
        interact_mapf = open(interact_path, 'r').read()
        
        x, y = 0, 0
        for line in interact_mapf:
          for char in line:
            if char == '\n':
              y += 1
              x = 0
            else:
              tile = self.tiles[(x, y)]
              if char == '0':
                tile.interact = False
              else:
                tile.interact = True
              self.tiles[(x, y)] = tile
              x += 1

      elif self.paused_index == 3: # Quit
        running = False

    elif key == terminal.TK_SPACE:
      pass

    return running

  def save_update(self):
    running = True

    return running

  def load_update(self):
    running = True

    return running

  def draw(self):
    terminal.clear()

    if self.edit_mode == EditMode.chars:
      self.chars_draw()
    elif self.edit_mode == EditMode.solidity:
      self.solidity_draw()
    elif self.edit_mode == EditMode.interactable:
      self.interact_draw()
    elif self.edit_mode == EditMode.color:
      self.color_draw()
    elif self.edit_mode == EditMode.paused:
      self.paused_draw()
    elif self.edit_mode == EditMode.save:
      self.save_draw()
    elif self.edit_mode == EditMode.load:
      self.load_draw()

    terminal.refresh()

  def chars_draw(self):
    for ((posx, posy), t) in self.tiles.items():
      print_terminal(posx, posy, t.ch, t.color)

      current_tile_ch = self.tiles[(self.cursor_x, self.cursor_y)].ch
      print_terminal(self.cursor_x, self.cursor_y, '%s[+]%s' % (current_tile_ch, self.curr_char), 'white')

    if self.first_line_point_set:
      pts = list(bresenham(self.line_start_x, self.line_start_y, self.cursor_x, self.cursor_y))

      for pt in pts:
        print_terminal(pt[0], pt[1], self.curr_char, self.colors[self.color_index])

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
    print_terminal(self.info_x_start, self.info_y_start + 4, 'color: %s' % self.colors[self.color_index], self.colors[self.color_index])

  def solidity_draw(self):
    for ((posx, posy), t) in self.tiles.items():
      if t.solid:
        print_terminal(posx, posy, t.ch, 'green')
      else:
        print_terminal(posx, posy, t.ch, 'white')

    if self.first_line_point_set:
      pts = list(bresenham(self.line_start_x, self.line_start_y, self.cursor_x, self.cursor_y))

      current_tile_ch = self.tiles[(self.cursor_x, self.cursor_y)].ch
      for pt in pts:
        print_terminal(pt[0], pt[1], '%s[+]å' % current_tile_ch, 'white')

    current_tile_ch = self.tiles[(self.cursor_x, self.cursor_y)].ch
    print_terminal(self.cursor_x, self.cursor_y, '%s[+]å' % current_tile_ch, 'white')

    draw_mode_char = ''
    if self.draw_mode == DrawingMode.char:
      draw_mode_char = 'c'
    elif self.draw_mode == DrawingMode.line:
      draw_mode_char = '\\'


    print_terminal(self.info_x_start, self.info_y_start, '[[Solidity Mode]]', 'white')
    print_terminal(self.info_x_start, self.info_y_start + 1, 'draw mode: [[%s]]' % (draw_mode_char), 'white')

  def interact_draw(self):
    for ((posx, posy), t) in self.tiles.items():
      if t.interact:
        print_terminal(posx, posy, t.ch, 'blue')
      else:
        print_terminal(posx, posy, t.ch, 'white')

    if self.first_line_point_set:
      pts = list(bresenham(self.line_start_x, self.line_start_y, self.cursor_x, self.cursor_y))

      current_tile_ch = self.tiles[(self.cursor_x, self.cursor_y)].ch
      for pt in pts:
        print_terminal(pt[0], pt[1], '%s[+]å' % current_tile_ch, 'white')

    current_tile_ch = self.tiles[(self.cursor_x, self.cursor_y)].ch
    print_terminal(self.cursor_x, self.cursor_y, '%s[+]å' % current_tile_ch, 'white')

    draw_mode_char = ''
    if self.draw_mode == DrawingMode.char:
      draw_mode_char = 'c'
    elif self.draw_mode == DrawingMode.line:
      draw_mode_char = '\\'

    print_terminal(self.info_x_start, self.info_y_start, '[[Interact Mode]]', 'white')
    print_terminal(self.info_x_start, self.info_y_start + 1, 'draw mode: [[%s]]' % (draw_mode_char), 'white')

  def color_draw(self):
    y = 0
    for c in self.colors:
      if c == self.colors[self.color_index]:
        print_terminal(0, y, c, 'blue')
        y += 1
      else:
        print_terminal(0, y, c, 'white')
        y += 1

  def paused_draw(self):
    options = ['Return to map', 'Save map', 'Load map', 'Quit']

    print_terminal(0, 0, 'PAUSED', 'white')

    for y, option in enumerate(options):
      if y == self.paused_index:
        print_terminal(0, y + 1, option, 'blue')
      else:
        print_terminal(0, y + 1, option, 'white')

  def save_draw(self):
    pass

  def load_draw(self):
    pass