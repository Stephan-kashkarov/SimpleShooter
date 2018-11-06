import pygame as pg

class textBox(object):
	def __init__(self, title, x, y, fontSize, color, bgColor, screen):
		self.screen = screen
		self.font = pg.font.SysFont("Times New Roman", fontSize)
		self.pos = (x, y)
		self.fontSize = fontSize
		self.textSurf = self.font.render(title, False, color)
		self.width, self.height = self.textSurf.get_rect().size
		self.pos = (self.pos[0] - self.width/2, self.pos[1] - self.height/2)
		self.color = color
		self.bgColor = bgColor

	def draw(self):
		pg.draw.rect(
			self.screen,
			self.bgColor,
			pg.Rect(
				self.pos[0],
				self.pos[1],
				self.width,
				self.height
			)
		)
		self.screen.blit(self.textSurf, self.pos)


class buttonArray(object):
	def __init__(self, screen, items):
		self.screen = screen
		self.width, self.height = self.screen.get_rect().size
		self.items = items
		poses = self.calcitemPoses()
		self.genButtons(poses)


	def calcitemPoses(self):
		poses = [None]*len(self.items)
		if len(self.items) % 2 == 0:
			itemsLen = len(self.items)
			mod = 0
			for i in range(int(itemsLen/2), -1, -1):
				poses[i] = int(self.height/2) + mod
				mod += 150
			mod = 150
			for i in range(int(itemsLen/2)+1, itemsLen):
				poses[i] = int(self.height/2) - mod
				mod += 150
		else:
			itemsLen = len(self.items)
			mod = 0
			for i in range(int(itemsLen/2), 0, -1):
				poses[i] = int(self.height/2) + mod
				mod += 150
			poses[int(itemsLen/2)+1] = int(self.height/2)
			mod = 150
			for i in range(int(itemsLen/2) + 2 , itemsLen):
				poses[i] = int(self.height/2) - mod
				mod -= 150
		return list(reversed(poses))

	def genButtons(self, poses):
		for index, item in enumerate(self.items):
			item = Button(item, index, (int(self.width/2), poses[index]), self.screen, color=(230, 230, 230))
			self.items[index] = item

	def run(self):
		for item in self.items:
			returns = item.run()
			if returns:
				return returns
		return False

class Button(object):
	def __init__(self, title, value, pos, screen, color=(255, 255, 255), bgColor=(0,0,0)):
		self.screen = screen
		self.title = title
		self.value = value
		self.pos = pos
		self.x, self.y = self.pos
		self.color = color
		self.bgColor = bgColor
		self.altColour = (self.color[0] + 100, self.color[1] + 100, self.color[2] + 100)
		self.surface = textBox(title, pos[0], pos[1], 54, color, bgColor, screen)

	def hover(self):
		pos = pg.mouse.get_pos()
		y = int(self.pos[1] - self.surface.height/2)
		if int(pos[1]) in range(y, y + int(self.surface.height)):
			x = int(self.pos[0] - self.surface.width/2)
			if int(pos[0]) in range(x, x + int(self.surface.width)):
				return True
		return False

	def click(self):
		if self.hover() == True:
			mouse = pg.mouse.get_pressed()
			return mouse[0]
		return False

	def draw(self):
		if self.hover():
			self.surface.color = self.altColour
		else:
			self.surface.color = self.color
		self.surface.draw()

	def run(self):
		if self.click():
			return self.value
		else:
			self.draw()
			return False


