from bearlibterminal import terminal
from vidablue import VidaBlue
from easygui import multenterbox

def main():
  (w, h) = multenterbox('width and height', 'Vida Blue Map Maker', ['width', 'height'], [32, 32])
  terminal.open()
  terminal.set("window.title: 'Vida Blue Map Maker'")
  terminal.set("window.fullscreen: true")
  terminal.set("window: size=%sx%s" % (int(w) + 25, h))
  terminal.set("font: square.ttf, size = 12")

  running = True
  vida = VidaBlue(width=32, height=64)

  while running:
    vida.draw()
    running = vida.update()
  terminal.close()

if __name__ == "__main__":
  main()