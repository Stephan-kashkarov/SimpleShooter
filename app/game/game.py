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


def singlePlayer(screen):
	menu.loadingScreen(screen)
	controls = {
		'up': pg.K_w,
		'down': pg.K_s,
		'left': pg.K_a,
		'right': pg.K_d,
		'reload': pg.K_r
        }
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

def mulitplayerUser(screen, options):
	menu.loadingScreen(screen)
	player1 = player.Player(options.serverIP, options._map, options.screen, options.controls)
	player1.run()
	menu.loadingScreen(screen)

def multiplayerHost(screen, options):
	pass