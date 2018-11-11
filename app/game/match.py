import os
import time
import json
import requests

import pygame as pg

import app.game.sprites.bullet as _bullet
import app.game.sprites.soldier as soldier


class options(object):
	"""Options object
	made to make initalisers for clients short
	"""
	def __init__(self, serverIP, mapSize, key):
		self.serverIP = serverIP
		self.mapSize = mapSize
		self.key = key


class Match(object):
	"""Match class
	game instance runs all calculations
	"""
	def __init__(self, options, _map, players):
		self.serverIP = 'http://' + options.serverIP
		self.map = _map
		self.key = options.key
		self.clock = pg.time.Clock()
		# sends map to server
		self.sendMap()
		time.sleep(2) # sync timer
		self.players = players
		self.playerGroup = pg.sprite.Group()
		self.bulletGroup = pg.sprite.Group()
		self.unitPoses = {'players':{}, 'bullets':[]}
		id = 0
		for player in self.players: # generates players
			self.playerGroup.add(soldier.Soldier(self.map, player.pos, id))
			id += 1
			self.unitPoses['players'][player.id] = [player.pos, player.rot, [0, 0], player.health]
		self.setUnits() # sends units to server
		self.clock = pg.time.Clock()

	# Unit Processing

	def getUnits(self):
		"""Gets units from server"""
		self.unitPoses = requests.get(str(self.serverIP + '/units/get')).json()

	def setUnits(self):
		"""Sets units on server"""
		requests.post(
			str(self.serverIP + '/units/set'),
			json=json.dumps({
				'key': self.key,
				'payload': self.unitPoses
			})
		)
	
	def updateUnits(self):
		""" updates units
		bulk of calculatons here
		"""
		for bullet in self.unitPoses['bullets']:
			"""Iterates bullets"""
			if str(bullet[3]) in [str(bullet.id) for bullet in self.bulletGroup.sprites()]:
				"""checks for existance"""
				for bulletObj in self.bulletGroup.sprites():
					if str(bulletObj.id) == str(bullet[3]):
						""""Finds object"""
						if bulletObj.dead:
							self.bulletGroup.remove(bulletObj)
							bulletObj.kill()
							bullet[3] = -1
						else:
							bulletObj.update()
							bullet[0] = bulletObj.pos
			else:
				if str(bullet[3]) != '-1':
					# draws dead object
					newBullet = _bullet.Bullet(self.map, bullet[0], bullet[3], bullet[1], bullet[2])
					self.bulletGroup.add(newBullet)

		# collisons
		collisons = pg.sprite.groupcollide(self.playerGroup, self.bulletGroup, False, False)
		# GROUPCOLIDE DOESENT WORK AND I am a little annoyed cos i only found out a few hours ago
		for player, bullets in collisons.items():
			"""Iterates collided objects"""
			for bullet in bullets:
				# for each bullet per player
				if str(bullet.ownerid) != str(player.id):
					# cgekcks that bullet isnt theirs
					print("Player {} has been hit. Health left: {}".format(player.id, player.health))
					player.health -= 2 # subtracts health
					self.unitPoses['players'][str(player.id)][3] = player.health
					if player.health <= 0: # check if player dead
						self.unitPoses['players'][str(player.id)][3] = 0 # forces health to be zero
						self.setUnits()
						player.kill()
						bullet.kill()
						del self.unitPoses['players'][str(player.id)] # deletes player
						return 0
					break

		for id, player in self.unitPoses['players'].items():
			"""Updates player poses"""
			if self.map[player[0][1] + player[2][1]][player[0][0] + player[2][0]] not in ["#", "1"]:
				player[0][0] += player[2][0]
				player[0][1] += player[2][1]
				for playerObj in self.playerGroup.sprites():
					if playerObj.id == str(id):
						player[3] = player.health
						playerObj.move(player[0])
		self.clock.tick(128)
		# limits frame rate

	# Map Processing
	def sendMap(self):
		# sends map to server
		requests.post(
			str(self.serverIP + '/map/set'),
			json=json.dumps({
				'key': self.key,
				'map': self.map
			})
		)

	def checkWin(self):
		return False if not bool(requests.get(self.serverIP + '/game/over')) else True

	def run(self):
		""""Runs the right way"""
		while True:
			self.getUnits()
			if self.updateUnits() == 0:
				break
			self.setUnits()
			# if self.checkWin() == True:
			# 	break
