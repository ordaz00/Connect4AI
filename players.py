from operator import le
import random
from re import T
import time
from turtle import pos, position
import pygame
import math

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	
	def isFirstMove(self, board):
		"""Finds if minimax is the first player and if its the first move

		Args:
			env (connect4): [is the connect4 object, can be used to determine the state of the board]

		Returns:
			[bool]: [a bool that denotes whether its the first move and minimax is the first player]
		"""
		if self.position != 1:
			return False
		for r in range(len(board)):
			for c in range(len(board[0])):
				if board[r][c] != 0:
					return False
		return True

	def possibleMoves(self, board):
		"""Finds the possible moves that can be made given a board state, does this by cheking if the top row of a colum is open

		Args:
			board (numpy array): [board state used to find the possible moves]

		Returns:
			[list]: [a list of open columns, which make up the possible moves]
		"""
		listOfMoves = []
		for col in range(len(board[0])):
			if board[len(board) - 1][col] == 0:
				listOfMoves.append(col)
		return listOfMoves
	
	def applyMove(self, board, col, position):
		"""applies a move to a copy of the board state

		Args:
			board (numpy array): [copy of the board state]
			col (int): [column to apply the move at]
			position (int): [player position; essentially the token that will be applied to the board]

		Returns:
			[numpy array]: [the new board state made after applying the move]
		"""
		for row in range(len(board)):
			if board[row][col] == 0:
				board[row][col] = position
				return board
	
	def maxValue(self, board, depth, curDepth):
		"""The max part of the minimax algorithm, finds the move max would make

		Args:
			board (numpy array): [the state of the board that is going to be used to choose the next move]
			depth (int): [the depth we are searching too, from the root]
			curDepth (int): [how deep we are in the tree]

		Returns:
			[int]: [the value of max's best move]
		"""
		position = self.position
		moves = self.possibleMoves(board)
		leaves = []
		if curDepth == 0:
			for posMove in moves:
				leaves.append(self.minValue(posMove,depth,curDepth + 1))
			for node in leaves:
				if leaves[node] == max(leaves):
					return node
		elif curDepth == depth:
			for posMove in moves:
				move = self.applyMove(board,posMove, position)
				eval = self.evaluateBoard(move)
				leaves.append(eval)
			return max(leaves)
		else:
			for posMove in moves:
				leaves.append(self.minValue(posMove,depth,curDepth + 1))
			return max(leaves)

	def minValue(self, board, depth, curDepth):
		"""The min part of the minimax algorithm, finds the move min would make

		Args:
			board (numpy array): [the state of the board that is going to be used to choose the next move]
			depth (int): [the depth we are searching too, from the root]
			curDepth (int): [how deep we are in the tree]

		Returns:
			[int]: [the value of min's best move]
		"""
		if self.position == 1:
			position = 2
		else:
			position = 1
		moves = self.possibleMoves(board)
		leaves = []
		if curDepth == depth:
			for posMove in moves:
				move = self.applyMove(board, posMove, position)
				eval = self.evaluateBoard(move)
				leaves.append(eval)
			return min(leaves)
		else:
			for posMove in moves:

				leaves.append(self.maxValue(posMove,depth,curDepth + 1))
			return min(leaves)
			
	def getMove(self, board, depth):
		"""Employs the minimax algorithm to find the position of the best move at the depth that's being searching too

		Args:
			board (numpy array): [an array that contains the game board]
			depth (int): [the depth we want to search to]

		Returns:
			[int]: [the column of best possible move that can be made at the depth that's being searched too]
		"""
		return self.maxValue(board, depth, 0)

	def play(self, env, move):
		"""makes a move

		Args:
			env (connect4): [the connect 4 object, that is used to create and play the game]
			move (list): [a list that will contain the column that will be played]
		"""
		depth = 3
		board = env.getBoard()
		if(self.isFirstMove(board)):
			move[:] = [3]
		else:
			move[:] = [self.getMove(board, depth)]

class alphaBetaAI(connect4Player):

	def play(self, env, move):
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




