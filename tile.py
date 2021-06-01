class Tile:
  def __init__(self, ch):
    self.ch = ch
    self.color = 'white'
    self.solid = False
    self.interact = False
    self.has_properties = False
    self.name = ''
    self.desc = ''