# imporst

import time
import pprint
import random
import requests
import multiprocessing

import pygame as pg

import app.game.match as match
import app.assets.menu as menu
import app.game.map.map as maps
import app.game.clients.player as player
import app.game.clients.ai as ai
import app.game.server as server


def encounter(screen, controls):
	"""Lauchnes an encounter"""
	menu.loadingScreen(screen) # loading screen
	options = match.options(
		'127.0.0.1:5000',
		256,
		random.randint(1000, 9999)
	) # options object
	_map = maps.generateMap(options.mapSize) # generates map
	host = server.Server(_map, options.key) # inits server
	server_ = multiprocessing.Process(target=host.run)  # puts server on process
	server_.start()  # runs server on process
	# allow for the server to initializse
	time.sleep(1)
	player1 = player.Player(options.serverIP, _map, screen, controls) # inits player obj
	ais = []
	aiThreads = []
	for i in range( random.randint(1, 2)): # makes 1 or 2 bots
		ai_ = ai.AI(options.serverIP, _map)
		aiThreads.append(multiprocessing.Process(target=ai_.run))
		ais.append(ai_)

	ais.append(player1)
	game = match.Match(options, _map, ais)

	# Making Threads
	gameThread = multiprocessing.Process(target=game.run)
	time.sleep(1) # for sync
	# Starting Threads
	gameThread.start()
	for aiThread in aiThreads:
		aiThread.start()
	# Running clientside
	try:
		state = player1.run()
	except:
		state= True
	menu.loadingScreen(screen)
	# Joining of threads
	gameThread.terminate()
	gameThread.join()
	for aiThread in aiThreads:
		aiThread.terminate()
		aiThread.join()
	server_.terminate()
	server_.join(5)
	time.sleep(3)
	if state == False:
		pg.quit()
		quit()
	return 0

def singlePlayer(screen, controls):
	screen.fill((0,0,0))
	clock = pg.time.Clock()
	_map = _map = maps.generateMap(8)
	tileSize = screen.get_rect().height / 9
	playerPos = [1, 1]
	_map[playerPos[1]][playerPos[0]] = '4'
	enemyPoses = []
	for i in range(random.randint(2, 4)):
		x = random.randint(1, len(_map)-2)
		y = random.randint(1, len(_map)-2)
		enemyPoses.append([x, y])
		_map[y][x] = "3"

	pprint.pprint(_map)
	while True:
		for y in range(len(_map)):
			for x in range(len(_map[0])):
				point = _map[y][x]
				if point == "0":
					color = (0, 200, 0)
				elif point == "1":
					color = (200, 200, 200)
				elif point == "3":
					color = (255, 0, 0)
				elif point == "4":
					color = (0, 255, 0)
				elif point == "#":
					color = (255, 255, 255)
				pg.draw.rect(
					screen,
					color,
					pg.Rect(x*tileSize, y*tileSize, tileSize, tileSize)
				)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

		pressed = pg.key.get_pressed()


		 # im sorry for this
		if pressed[controls['up']]:
			if _map[playerPos[0]][playerPos[1] - 1] in ["0", "3"]:
				_map[playerPos[1]][playerPos[0]] = '0'
				playerPos[1] -= 1
				_map[playerPos[1]][playerPos[0]] = '4'

		elif pressed[controls['down']]:
			if _map[playerPos[0]][playerPos[1] + 1] in ["0", "3"]:
				_map[playerPos[1]][playerPos[0]] = '0'
				playerPos[1] += 1
				_map[playerPos[1]][playerPos[0]] = '4'

		elif pressed[controls['left']]:
			if _map[playerPos[0] - 1][playerPos[1]] in ["0", "3"]:
				_map[playerPos[1]][playerPos[0]] = '0'
				playerPos[0] -= 1
				_map[playerPos[1]][playerPos[0]] = '4'

		elif pressed[controls['right']]:
			if _map[playerPos[0] + 1][playerPos[1]] in ["0", "3"]:
				_map[playerPos[1]][playerPos[0]] = '0'
				playerPos[0] += 1
				_map[playerPos[1]][playerPos[0]] = '4'

		if playerPos in enemyPoses:
			encounter(screen, controls)
			enemyPoses.pop(enemyPoses.index(playerPos))
		clock.tick(10)
		pg.display.flip()

	return 0

def mulitplayerUser(screen, options, controls):
	menu.loadingScreen(screen)
	_map = requests.get('http://' + options.serverIP + '/map/get')
	try:
		player1 = player.Player(options.serverIP, _map, screen, controls)
		player1.run()
	except:
		pass
	menu.loadingScreen(screen)

def multiplayerHost(screen, options):
	menu.loadingScreen(screen)
	options = match.options(
		'127.0.0.1:5000',
		256,
		random.randint(1000, 9999)
	)
	_map = maps.generateMap(options.mapSize)
	host = server.Server(_map, options.key)
	server_ = multiprocessing.Process(target=host.run)
	server_.start()
	time.sleep(1)

