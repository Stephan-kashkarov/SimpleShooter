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
			42, # fontsize
			(0,0,0), # color
			screen
		)
		self.items = text.buttonArray(
			screen,
			items,
			True
		)

	def run(self):
		selected = False
		while not selected:
			pg.display.fill((200, 200, 200))
			self.title.draw()
			selected = self.items.draw()
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
