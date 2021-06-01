from bearlibterminal import terminal
from vidablue import VidaBlue

def main():
  terminal.open()
  settings = open("settings.txt", "r").read()
  terminal.set(settings)

  running = True
  vida = VidaBlue()

  while running:
    vida.draw()
    running = vida.update()
  terminal.close()

if __name__ == "__main__":
  main()