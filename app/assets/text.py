import pygame as pg

class textBox(pg.sprite.Sprite):
	def __init__(self, title, x, y, fontSize, color, screen):
		self.screen = screen
		self.font = pg.font.SysFont("Times New Roman", fontSize)
		self.pos = (x, y)
		self.fontSize = fontSize
		self.textSurf = self.font.render(title, False, color)
		self.width, self.height = self.textSurf.get_rect().size
		self.pos = (self.pos[0] - self.width/2, self.pos[1] - self.height/2)

	def draw(self):
		self.screen.blit(self.textSurf, self.pos)


class buttonArray(pg.sprite.Group):
	def __init__(self, screen, items, vert=False):
		self.screen = screen
		self.items = items
		self.vert = vert
		poses = self.calcitemPoses()
		self.items = self.genButtons(poses)


	def calcitemPoses(self):
		pass
	
