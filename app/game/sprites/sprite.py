import pygame as pg


class Sprite(pg.sprite.Sprite):
	def __init__(self, map):
		super().__init__()
		self.rotation = 0
		self.map = map
		self.pos = [0, 0]

	def update(self):
		pass

