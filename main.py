from bearlibterminal import terminal
from vidablue import VidaBlue
from easygui import multenterbox

def main():
  (w, h, cell_size, map_name) = multenterbox('width and height', 'Vida Blue Map Maker', ['width', 'height', 'cell size', 'map name'], [32, 32, 24, 'default_name'])
  terminal.open()
  terminal.set("window.title: 'Vida Blue Map Maker'")
  terminal.set("window.fullscreen: true")
  terminal.set("window: cellsize=%sx%s" % (cell_size, cell_size))
  terminal.set("window: size=%sx%s" % (int(w) + 25, h))
  terminal.set("font: square.ttf, size = 12")
  terminal.set("input.filter={keyboard, mouse+}")

  running = True
  vida = VidaBlue(int(w), int(h), map_name)

  while running:
    vida.draw()
    running = vida.update()
  terminal.close()

if __name__ == "__main__":
  main()