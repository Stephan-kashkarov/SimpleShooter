# imports

import pygame as pg

import app.assets.text as text
import app.assets.settings as settings

class simpleMenu(object):
	"""Simple menu object for extendablilty"""
	def __init__(self, title, items, screen):
		self.screen = screen
		self.title = text.textBox(
			title, # Text
			settings.SCREEN_WIDTH/2, # x
			settings.SCREEN_HEIGHT/6, # y
			72, # fontsize
			(0, 0, 0),
			(200, 200, 200),  # color
			screen
		)
		self.items = text.buttonArray(
			screen,
			items
		)
	
	def events(self):
		"""Event method
		for quit loop
		"""
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

	def run(self):
		"""Click and mouse tracking"""
		selected = False
		while not selected:
			pg.event.pump()
			self.screen.fill((200, 200, 200))
			self.title.draw()
			# click tracking
			selected = self.items.run()
			self.events()
			pg.display.flip()
		return selected


def menu(screen):
	"""Main menu func
	makes a preset main menu from above class
	"""
	screen.fill((200,200,200))
	result = simpleMenu(
		"Simple Shooter",
		["SinglePlayer", "Multiplayer", "Settings", "Quit"],
		screen
	)

	# returns string of clicked object
	return result.run()


def setting(screen):
	"""settings functuon
	allows for key rebind
	"""
	pass

def loadingScreen(screen):
	"""Simple loading screen
	to keep screen clean on loads
	"""
	screen.fill((0, 0, 0))
	x, y = screen.get_rect().size
	x = int(x/2)
	y = int(y/2)
	text.textBox("LOADING...", x, y, 72, (255, 255, 255), (0,0,0), screen).draw()
	pg.display.flip()
