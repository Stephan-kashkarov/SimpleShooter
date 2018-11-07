'''Imports'''
import pygame as pg

import app.game.game as game
import app.assets.menu as menu
import app.assets.settings as settings



class Game(object):
	def __init__(self):
		pg.init()
		pg.mixer.init()
		pg.font.init()
		self.res = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
		self.screen = pg.display.set_mode(self.res)
		pg.display.set_caption("STEPHAN IS COOL MAYBE?")
		self.clock = pg.time.Clock()
		self.screen.fill((255,255,255))
		pg.display.flip()
		self.run()

	def run(self):
		while True:
			state = menu.menu(self.screen)
			print(state)
			if state == 1:
				print("!!")
				game.singlePlayer(self.screen)
			elif state == 2:
				print("TWO SELECTED")
				pass
				# options = menu.multiplayerSettings(self.screen)
				# game.multiplayer(self.screen, options)
			elif state == 3:
				print("THREE SELECTED")
				pass
				# menu.settings(self.screen)
			else:
				pg.quit()
				quit()


if __name__ == '__main__':
	Game()
