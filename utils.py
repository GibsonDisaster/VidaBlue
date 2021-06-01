from bearlibterminal import terminal

def print_terminal(x, y, g, c):
  old_color = terminal.TK_COLOR
  terminal.color(c)
  terminal.printf(x, y, g)
  terminal.color(old_color)