import random

import pygame as pg

import app.game.sprites.sprite as sprite
import app.game.sprites.bullet as bullet


class Soldier(sprite.Sprite):
	def __init__(self, map, pos, id):
		super().__init__(map, id)
		self.pos = pos