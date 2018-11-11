import pygame as pg

class textBox(object):
	"""Class textBox
	A simple text box object
	extendable
	"""
	def __init__(self, title, x, y, fontSize, color, bgColor, screen):
		"""param title - str | title of the thing
		param x, y - int - int | coords of text
		param fontsize - int | size of font
		color, bgColor - RGB | colors
		screen - pg.surface | screen for printing"""
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
		"""Draws the textbox"""
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
	"""Container for buttons"""
	def __init__(self, screen, items):
		"""param screen - pg.surface | for printing
		param items - [str] | list of buttons to make array of"""
		self.screen = screen
		self.width, self.height = self.screen.get_rect().size
		self.items = items
		# gets positions for the buttons
		poses = self.calcitemPoses()
		# generates the buttons 
		self.genButtons(poses)


	def calcitemPoses(self):
		"""Calculates the psositions for the buttons so that they aren't overlapping"""
		poses = [None]*len(self.items)
		if len(self.items) % 2 == 0:
			itemsLen = len(self.items)
			mod = 0
			for i in range(int(itemsLen/2), -1, -1):
				poses[i] = int(self.height/2) + mod
				mod += 100
			mod = 100
			for i in range(int(itemsLen/2)+1, itemsLen):
				poses[i] = int(self.height/2) - mod
				mod += 100
		else:
			itemsLen = len(self.items)
			mod = 0
			for i in range(int(itemsLen/2), 0, -1):
				poses[i] = int(self.height/2) + mod
				mod += 100
			poses[int(itemsLen/2)+1] = int(self.height/2)
			mod = 100
			for i in range(int(itemsLen/2) + 2 , itemsLen):
				poses[i] = int(self.height/2) - mod
				mod -= 100
		return list(reversed(poses))

	def genButtons(self, poses):
		"""Initaiisses each button into list"""
		for index, item in enumerate(self.items):
			item = Button(item, index+1, (int(self.width/2), poses[index]), self.screen, color=(230, 230, 230))
			self.items[index] = item

	def run(self):
		"""Runs the program"""
		for item in self.items:
			returns = item.run()
			if returns:
				return returns
		return False

class Button(object):
	"""Button object"""
	def __init__(self, title, value, pos, screen, color=(255, 255, 255), bgColor=(0,0,0)):
		"""param value - str | the text value of the button"""
		self.screen = screen
		self.title = title
		self.value = value
		self.pos = pos
		self.x, self.y = self.pos
		self.color = color
		self.bgColor = bgColor
		# hover color calculated
		self.altColour = (self.color[0] + 100, self.color[1] + 100, self.color[2] + 100)
		self.surface = textBox(title, pos[0], pos[1], 42, color, bgColor, screen)

	def hover(self):
		"""Hover method
		returns if button hovered
		"""
		pos = pg.mouse.get_pos()
		y = int(self.pos[1] - self.surface.height/2)
		if int(pos[1]) in range(y, y + int(self.surface.height)):
			x = int(self.pos[0] - self.surface.width/2)
			if int(pos[0]) in range(x, x + int(self.surface.width)):
				return True
		return False

	def click(self):
		"""Click method
		checks if button is clicked"""
		if self.hover() == True:
			mouse = pg.mouse.get_pressed()
			return mouse[0] # will be 1 if click
		return False

	def draw(self):
		"""Draw function
		draws the button
		supposed to change color of button
		"""
		if self.hover():
			self.surface.color = self.altColour
		else:
			self.surface.color = self.color
		self.surface.draw()

	def run(self):
		"""Runs button correctly"""
		if self.click():
			return self.value
		else:
			self.draw()
			return False


