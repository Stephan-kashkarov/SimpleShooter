import pygame as pg

class textBox(pg.sprite.Sprite):
	def __init__(self, title, x, y, fontSize, color, screen):
		self.screen = screen
		self.width, self.height = self.screen.get_rect().size
		self.font = pg.font.SysFont("Times New Roman", fontSize)
		self.pos = (x, y)
		self.fontSize = fontSize
		self.textSurf = self.font.render(title, False, color)
		self.pos = (self.pos[0] - self.width/2, self.pos[1] - self.height/2)

	def draw(self):
		self.screen.blit(self.textSurf, self.pos)


class buttonArray(pg.sprite.Group):
	def __init__(self, screen, items):
		self.screen = screen
		self.width, self.height = self.screen.get_rect().size
		self.items = items
		poses = self.calcitemPoses()
		self.items = self.genButtons(poses)


	def calcitemPoses(self):
		poses = [x for x in self.items]
		if len(self.items) % 2 == 0:
			itemsLen = len(self.items)
			mod = 0
			for i in range(0, itemsLen/2, -1):
				poses.insert(i, self.height + mod)
				mod += 200
			mod = 0
			for i in range(itemsLen/2, itemsLen):
				poses.insert(i, self.height - mod)
				mod += 200
		return poses

	def genButtons(self):
		pass
