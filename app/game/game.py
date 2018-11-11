import time
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
	# allow for the server to initializse
	time.sleep(1)
	player1 = player.Player(options.serverIP, _map, screen, controls)
	player2 = ai.AI(options.serverIP, _map)
	players = [player1, player2]
	game = match.Match(options, _map, players)

	# Making Threads
	gameThread = multiprocessing.Process(target=game.run)
	aiThread = multiprocessing.Process(target=player2.run)
	time.sleep(1)
	# Starting Threads
	gameThread.start()
	aiThread.start()
	# Running clientside
	try:
		state = player1.run()
	except:
		pass
	menu.loadingScreen(screen)
	# Joining of threads
	gameThread.terminate()
	gameThread.join()
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
	_map = _map = maps.generateMap(9)
	tileSize = screen.get_rect().height / 9
	playerPos = [1, 1]
	enemyPoses = []
	for i in range(random.randint(3, 5)):
		enemyPoses.append([random.randint(1, len(map)-1), random.randint(1, len(map)-1)])
		_map[enemyPoses[-1][1]][enemyPoses[-1][0]] == "3"
	while True:
		for y in range(len(_map)):
			for x in range(len(_map[0])):
				point = _map[y][x]
				if point == "0":
					color = (0, 200, 0)
				elif point == "1":
					color = (200, 200, 200)
				elif point == "2":
					color = (255, 0, 0)
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

		if pressed[controls['up']]:
			playerPos[1] -= 1 if _map[playerPos[0]][playerPos[1] - 1] in ["1", "0"] else 0
		elif pressed[controls['down']]:
			playerPos[1] += 1 if _map[playerPos[0]][playerPos[1] + 1] in ["1", "0"] else 0
		elif pressed[controls['left']]:
			playerPos[0] -= 1 if _map[playerPos[0] - 1][playerPos[1]] in ["1", "0"] else 0
		elif pressed[controls['right']]:
			playerPos[0] += 1 if _map[playerPos[0] + 1][playerPos[1]] in ["1", "0"] else 0

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

