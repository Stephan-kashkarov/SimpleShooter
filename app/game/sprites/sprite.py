import pygame as pg


class Sprite(pg.sprite.Sprite):
	def __init__(self, screen, map, img):
		super().__init__()
		self.img = pg.image.load(img)
		self.rect = self.img.get_rect()
		self.rotation = 0
		self.map = map
		self.pos = [0, 0]
		self.screen = screen

	def update(self):
		pass

	def draw(self):
		pg.transform.rotate(self.img, self.rotation)
		self.screen.blit(self.img, self.pos)
