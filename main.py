'''Imports'''
import pygame as pg

import app.game.game as game
import app.assets.menu as menu
import app.assets.settings as settings



class Game(object):
	"""Game object
		main container for game
	"""
	def __init__(self):
		# pygame inits
		pg.init()
		pg.mixer.init()
		pg.font.init()
		# screen inits
		self.res = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
		self.screen = pg.display.set_mode(self.res)
		pg.display.set_caption("STEPHAN IS COOL MAYBE?")
		self.screen.fill((255,255,255))
		pg.display.flip()
		# control inits
		self.controls = {
			'up': pg.K_w,
			'down': pg.K_s,
			'left': pg.K_a,
			'right': pg.K_d,
			'reload': pg.K_r
        }
		# runs game
		self.run()

	def run(self):
		"""Run funtion
			runs the game
		"""
		while True:
			state = menu.menu(self.screen)
			if state == 1:
				game.singlePlayer(self.screen, self.controls)
			elif state == 2:
				pass
				# options = menu.multiplayerSettings(self.screen)
				# game.multiplayer(self.screen, options)
			elif state == 3:
				pass
				menu.setting(self.screen)
			else:
				pg.quit()
				quit()


if __name__ == '__main__': # allows for extention
	Game()
