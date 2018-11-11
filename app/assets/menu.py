import pygame as pg

import app.assets.text as text
import app.assets.settings as settings

class simpleMenu(object):
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
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

	def run(self):
		selected = False
		while not selected:
			pg.event.pump()
			self.screen.fill((200, 200, 200))
			self.title.draw()
			selected = self.items.run()
			self.events()
			pg.display.flip()
		return selected


def menu(screen):
	screen.fill((200,200,200))
	result = simpleMenu(
		"Simple Shooter",
		["SinglePlayer", "Multiplayer", "Settings", "Quit"],
		screen
	)
	return result.run()

def loadingScreen(screen):
	screen.fill((0, 0, 0))
	x, y = screen.get_rect().size
	x = int(x/2)
	y = int(y/2)
	text.textBox("LOADING...", x, y, 72, (255, 255, 255), (0,0,0), screen).draw()
	pg.display.flip()