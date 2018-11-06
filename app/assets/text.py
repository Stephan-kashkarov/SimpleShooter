import pygame as pg

class textBox(object):
	def __init__(self, title, x, y, fontSize, color, screen):
		self.screen = screen
		self.font = pg.font.SysFont("Times New Roman", fontSize)
		self.pos = (x, y)
		self.fontSize = fontSize
		self.textSurf = self.font.render(title, False, color)
		self.width, self.height = self.textSurf.get_rect().size
		self.pos = (self.pos[0] - self.width/2, self.pos[1] - self.height/2)
		self.color = color

	def draw(self):
		pg.draw.rect(
			self.screen,
			self.color,
			pg.Rect(
				self.pos[0],
				self.pos[1],
				self.width,
				self.height
			)
		)
		self.screen.blit(self.textSurf, self.pos)


class buttonArray(pg.sprite.Group):
	def __init__(self, screen, items):
		self.screen = screen
		self.width, self.height = self.screen.get_rect().size
		self.items = items
		poses = self.calcitemPoses()
		self.genButtons(poses)


	def calcitemPoses(self):
		poses = []
		if len(self.items) % 2 == 0:
			itemsLen = len(self.items)
			mod = 0
			for i in range(0, itemsLen/2, -1):
				poses[i] = self.height + mod
				mod += 200
			mod = 0
			for i in range(itemsLen/2, itemsLen):
				poses[i] = self.height - mod
				mod += 200
		return poses

	def genButtons(self, poses):
		for index, item in enumerate(self.items):
			item = Button(item, index, poses[index], color=(230, 230, 230))
			self.items[index] = item

class Button(pg.sprite.Sprite):
	def __init__(self, title, value, pos, screen, color=(255, 255, 255)):
		self.screen = screen
		self.title = title
		self.value = value
		self.pos = pos
		self.color = color
		self.surface = textBox(title, pos[0], pos[1], 20, color, screen)

	def hover(self):
		pos = pg.mouse.get_pos()
		if pos[1] in range(self.y, self.y + self.surface.height):
			if pos[0] in range(self.x, self.x + self.surface.width):
				return True
		return False

	def click(self):
		if self.hover == True:
			return pg.mouse.get_pressed()[0]
		return False

	def draw(self):
		if self.hover():
			self.surface.color = (x - 20 for x in self.color)
		else:
			self.surface.color = self.color
		self.surface.draw()

	def run(self):
		if self.click():
			return self.value
		else:
			self.draw()


