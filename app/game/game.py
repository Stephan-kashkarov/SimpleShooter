import time
import random
import threading
import multiprocessing

import pygame as pg

import app.game.match as match
import app.game.map.map as maps
import app.game.player as player
import app.game.server as server


def singlePlayer(screen):
	options = match.options(
		'127.0.0.1:5000',
		1000,
		random.randint(1000, 9999)
	)
	player1 = player.PlayerClient(options.serverIP, screen)
	player2 = player.AI(options.serverIP)

	_map = maps.generateMap(options.mapSize)
	host = server.Server(_map, options.key)
	server_ = multiprocessing.Process(target=host.run)
	server_.start()
	# allow for the server to initializse
	time.sleep(1)
	game = match.Match(options, _map)

	# Making Threads
	gameThread = threading.Thread(target=game.run)
	aiThread = threading.Thread(target=player2.run)
	# Starting Threads
	gameThread.start()
	aiThread.start()
	# Running clientside
	state = player1.run()
	# Joining of threads
	gameThread.join()
	aiThread.join()
	server_.terminate()
	server_.join(5)
	time.sleep(1)
	if state == 'quit':
		pg.quit()
		quit()
	return 0
