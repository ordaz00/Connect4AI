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
		for r in range(6):
			for c in range(7):
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
		#print(type(board))
		listOfMoves = []
		for col in range(6):
			if board[0][col] == 0:
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
			if board[5 - row][col] == 0:
				board[5 - row][col] = position
				#print("I return a board here")
				#print(board)
				#print("end of returned board")
				return board

	def getMultiplier(self, pos, row, count):
		if pos == self.position:
			# if pos == 1:
			# 	if(row + (4 - count)) % 2 == 0:
			# 		multiplier = 3/4
			# 	else:
			# 		multiplier = 1
			# else:
			# 	if(row + (4 - count)) % 2 == 1:
			# 		multiplier = 3/4
			# 	else:
			# 		multiplier = 1
			multiplier = 1
		else:
			# if pos == 1:
			# 	if(row + (4 - count)) % 2 == 0:
			# 		multiplier = -3/4
			# 	else:
			# 		multiplier = -1
			# else:
			# 	if(row + (4 - count)) % 2 == 1:
			# 		multiplier = -3/4
			# 	else:
			# 		multiplier = -1
			multiplier = -1
		return multiplier

	def vertWin(self, board):
		threat = 0
		count = 0
		posOfMax = 0
		maxCount = 0
		lowestRow = 0
		for col in range(7):
			pos = board[5][col]
			count = 0
			if pos != 0:
				for row in range(5,-1,-1):
					if board[row][col] == pos:
						count += 1
						if count == 4:
							#print("I exit here, vert")
							if pos == self.position:
								return 100
							else:
								return -100
							
					elif board[row][col] == 0:
						if (count > maxCount) & ((row + 1 + count) >= 4):
							posOfMax = pos
							maxCount = count
							lowestRow = row + 1
						elif count == maxCount:
							if row > lowestRow:
								lowestRow = row + 1
								posOfMax = pos
						break

					else:
						pos = board[row][col]
						count = 1
		multiplier = self.getMultiplier(posOfMax, lowestRow, maxCount)
		if lowestRow > 0:
			if maxCount == 3:
				threat = 80 * multiplier
			elif maxCount == 2:
				if lowestRow > 1:
					threat = 50 * multiplier
				else:
					threat = 0
			else:
				if lowestRow > 2:
					threat = 10 * multiplier
				else:
					threat = 0
		else:
			threat = 0
		# print("maxCount ", maxCount, ", numOfSpaces ", lowestRow, ", multiplier ", multiplier, ", threat", threat)
		# print(board)
		#print("I exit here, vert")
		return threat

	def horWin(self, board):
		pos = 0
		threat = 0
		count = 0
		maxCount = 0
		maxMidSpaces = 0
		maxEndSpaces = 0
		maxBeginningSpaces = 0
		endSpace = 0
		midSpace = 0
		beginningSpace = 0
		space = 0
		maxRow = 0
		posOfMax = 0
		for row in range(5, -1, -1):
			count = 0
			endSpace = 0
			midSpace = 0
			beginningSpace = 0
			space = 0
			pos = 0
			for col in range(7):
				if board[row][col] != 0:
					if pos == 0:
						pos = board[row][col]
					if board[row][col] == pos:
						count += 1
						if space > 0:
							midSpace += space
							space = 0
						if (count == 4) & (midSpace == 0):
							#print("I exit here, hor")
							if pos == self.position:
								return 100
							else:
								return -100
					else:
						if space > 0:
							endSpace += space
						if (count > maxCount) & ((count + endSpace + midSpace + beginningSpace) >= 4):
							maxCount = count
							maxEndSpaces = endSpace
							maxMidSpaces = midSpace
							maxBeginningSpaces = beginningSpace
							maxRow = row
							posOfMax = pos
						elif count == maxCount:
							if ((endSpace + midSpace + beginningSpace) > (maxEndSpaces + maxMidSpaces + beginningSpace)):
								maxEndSpaces = endSpace
								maxMidSpaces = midSpace
								maxBeginningSpaces = beginningSpace
								maxRow = row
								posOfMax = pos
						pos = board[row][col]
						count = 1
						if space > 0:
							beginningSpace += space
							endSpace = 0
							space = 0
							midSpace = 0
						else:
							endSpace = 0
							midSpace = 0
							beginningSpace = 0
				else:
					if count == 0:
						beginningSpace += 1
					else:
						space += 1
			if space > 0:
				endSpace += space
			if (count > maxCount) & ((count + endSpace + midSpace + beginningSpace) >= 4):
				maxCount = count
				maxEndSpaces = endSpace
				maxMidSpaces = midSpace
				maxBeginningSpaces = beginningSpace
				maxRow = row
				posOfMax = pos
			elif count == maxCount:
				if ((endSpace + midSpace + beginningSpace) > (maxEndSpaces + maxMidSpaces + beginningSpace)):
					maxEndSpaces = endSpace
					maxMidSpaces = midSpace
					maxBeginningSpaces = beginningSpace
					maxRow = row
					posOfMax = pos
			if(beginningSpace == 7):
				break
		multiplier = self.getMultiplier(posOfMax, maxRow, 0)
		if((maxEndSpaces + maxMidSpaces + maxBeginningSpaces) > 0):
			if maxCount > 3:
				threat = 90 * multiplier + (-5 * maxMidSpaces)
			elif maxCount == 3:
				if (maxMidSpaces == 0):
					if (maxEndSpaces >= 1) & (maxBeginningSpaces >= 1):
						threat = 99 * multiplier
					else:
						threat = 85 * multiplier
				elif maxMidSpaces == 1:
					threat = 85 * multiplier
				else:
					threat = 75 * multiplier + (-5 * maxMidSpaces)
			elif maxCount == 2:
				if (maxMidSpaces == 0):
					if (maxEndSpaces >= 1):
						if(maxBeginningSpaces >= 1):
							threat = 70 * multiplier
						else:
							if(maxEndSpaces >= 2):
								threat = 70 * multiplier
							else:
								threat = 0
					else:
						if(maxBeginningSpaces > 2):
							threat = 70 * multiplier
						else:
							threat = 0
				else:
					if (maxMidSpaces + maxBeginningSpaces + maxEndSpaces) >= 2:
						threat = 70 * multiplier
					else:
						threat = 0
			else:
				if (maxMidSpaces + maxBeginningSpaces + maxEndSpaces) > 2:
					threat = 10 * multiplier
				else:
					threat = 0
		else:
			threat = 0
		# print("I exit here, hor")
		# print("maxCount ", maxCount, ", numOfSpaces ", (maxBeginningSpaces + maxEndSpaces + maxMidSpaces), ", multiplier ", multiplier, ", threat", threat)
		# print(board)
		return threat

	def leftDiagWin(self, board):
		count = 0
		x = 3
		y = 5
		threat = 0
		maxCount = 0
		maxMidSpaces = 0
		maxEndSpaces = 0
		maxBeginningSpaces = 0
		endSpace = 0
		midSpace = 0
		beginningSpace = 0
		space = 0
		maxRow = 0
		posOfMax = 0
		pos = 0
		while y >= 3:
			count = 0
			endSpace = 0
			midSpace = 0
			beginningSpace = 0
			space = 0
			pos = 0
			if(x == 3):
				for i in range(4):
					if(board[y - i][x - i] != 0):
						if pos == 0:
							pos = board[y][x]
						if(board[y - i][x - i] == pos):
							count += 1
							if count == 4:
								#print("I exit here, left")
								if pos == self.position:
									return 100
								else:
									return -100
						else:
							break
					elif board[y - i][x - i] == 0:
						if count == 0:
							beginningSpace += 1
						else:
							space += 1
						maxRow = y - i				
			elif (y == 3):
				for i in range(4):
					if(board[y][x] != 0):
						pos = board[y][x]
						if(board[y - i][x - i] == pos):
							count += 1
							if count == 4:
								#print("I exit here, left")
								if pos == self.position:
									return 100
								else:
									return -100
						else:
							break
					elif board[y - i][x - i] == 0:
						if count == 0:
							beginningSpace += 1
						else:
							space += 1
						maxRow = y - i			
			else:
				pos = 0
				diff = min(y, x) + 1
				for i in range(diff):
					if diff - i + count + beginningSpace + midSpace + endSpace + space >= 4:
						if(board[y - i][x - i] != 0):
							if pos == 0:
								pos = board[y - i][x - i]
							if(board[y - i][x - i] == pos):
								count += 1
								if count == 4:
									#print("I exit here, left")
									if pos == self.position:
										return 100
									else:
										return -100	
							else:
								if space > 0:
									endSpace += space
								if (count > maxCount) & ((count + endSpace + midSpace + beginningSpace) >= 4):
									maxCount = count
									maxEndSpaces = endSpace
									maxMidSpaces = midSpace
									maxBeginningSpaces = beginningSpace
									posOfMax = pos
								elif count == maxCount:
									if ((endSpace + midSpace + beginningSpace) > (maxEndSpaces + maxMidSpaces + beginningSpace)):
										maxEndSpaces = endSpace
										maxMidSpaces = midSpace
										maxBeginningSpaces = beginningSpace
										posOfMax = pos
								pos = board[y - i][x - i]
								count = 1
								if space > 0:
									endSpace += space
									space = 0
									midSpace = 0
									beginningSpace = 0
								else:
									endSpace = 0
									midSpace = 0
									beginningSpace = 0
						else:
							if count == 0:
								beginningSpace += 1
							else:
								space += 1
							maxRow = y - i
			if space > 0:
				endSpace += space
			if (count > maxCount) & ((count + endSpace + midSpace + beginningSpace) >= 4):
				maxCount = count
				maxEndSpaces = endSpace
				maxMidSpaces = midSpace
				maxBeginningSpaces = beginningSpace
				maxRow = maxRow
				posOfMax = pos
			elif count == maxCount:
				if ((endSpace + midSpace + beginningSpace) > (maxEndSpaces + maxMidSpaces + beginningSpace)):
					maxEndSpaces = endSpace
					maxMidSpaces = midSpace
					maxBeginningSpaces = beginningSpace
					maxRow = maxRow
					posOfMax = pos
			if(x < 6):
				x += 1
			else:
				y -= 1
			
		multiplier = self.getMultiplier(posOfMax, maxRow, 0)
		if((maxEndSpaces + maxMidSpaces + maxBeginningSpaces) > 0):
			if maxCount > 3:
				threat = 100 * multiplier + (-5 * maxMidSpaces)
			elif maxCount == 3:
				if (maxMidSpaces == 0):
					if (maxEndSpaces >= 1) & (maxBeginningSpaces >= 1):
						threat = 99 * multiplier
					else:
						threat = 95 * multiplier
				elif maxMidSpaces == 1:
					threat = 95 * multiplier
				else:
					threat = 95 * multiplier + (-5 * maxMidSpaces)
			elif maxCount == 2:
				if (maxMidSpaces == 0):
					if (maxEndSpaces >= 1):
						if(maxBeginningSpaces >= 1):
							threat = 80 * multiplier
						else:
							if(maxEndSpaces >= 2):
								threat = 80 * multiplier
							else:
								threat = 0
					else:
						if(maxBeginningSpaces > 2):
							threat = 80 * multiplier
						else:
							threat = 0
				else:
					if (maxMidSpaces + maxBeginningSpaces + maxEndSpaces) >= 2:
						threat = 80 * multiplier
					else:
						threat = 0
			else:
				if (maxMidSpaces + maxBeginningSpaces + maxEndSpaces) > 2:
					threat = 10 * multiplier
				else:
					threat = 0
		else:
			threat = 0
		#print("I exit here, left")
		# print("maxCount ", maxCount, ", numOfSpaces ", (maxBeginningSpaces + maxEndSpaces + maxMidSpaces), ", multiplier ", multiplier, ", threat", threat)
		# print(board)
		return threat
	
	def rightDiagWin(self, board):
		count = 0
		x = 0
		y = 3
		threat = 0
		maxCount = 0
		maxMidSpaces = 0
		maxEndSpaces = 0
		maxBeginningSpaces = 0
		endSpace = 0
		midSpace = 0
		beginningSpace = 0
		space = 0
		maxRow = 0
		posOfMax = 0
		while x < 4:
			endSpace = 0
			midSpace = 0
			beginningSpace = 0
			space = 0
			pos = 0
			if(x == 3):
				for i in range(4):
					if(board[y - i][x + i] != 0):
						if pos == 0:
							pos = board[y - i][x + i]
						if(board[y - i][x + i] == pos):
							count += 1
							if count == 4:
								#print("I exit here, right")
								if pos == self.position:
									return 100
								else:
									return -100
						else:
							break
				else:
					if count == 0:
						beginningSpace += 1
					else:
						space += 1
					maxRow = y - i
			
			elif (y == 3):
				for i in range(4):
					pos = board[y - i][x + i]
					if(board[y - i][x + i] != 0):
						if(board[y - i][x + i] == pos):
							count += 1
							if count == 4:
								#print("I exit here, right")
								if pos == self.position:
									return 100
								else:
									return -100
						else:
							break
					else:
						if count == 0:
							beginningSpace += 1
						else:
							space += 1
						maxRow = y - i
			else:
				pos = 0
				diff = min(y, x) + 1
				for i in range(diff):
					if diff - i + count + beginningSpace + midSpace + endSpace + space >= 4:
						if(board[y - i][x - i] != 0):
							if pos == 0:
								pos = board[y][x]
							if(board[y - i][x + i] == pos):
								count += 1
								if count == 4:
									#print("I exit here, right")
									if pos == self.position:
										return 100
									else:
										return -100
							else:
								if space > 0:
									endSpace += space
								if (count > maxCount) & ((count + endSpace + midSpace + beginningSpace) > 4):
									maxCount = count
									maxEndSpaces = endSpace
									maxMidSpaces = midSpace
									maxBeginningSpaces = beginningSpace
									posOfMax = pos
								elif count == maxCount:
									if ((endSpace + midSpace + beginningSpace) > (maxEndSpaces + maxMidSpaces + beginningSpace)):
										maxEndSpaces = endSpace
										maxMidSpaces = midSpace
										maxBeginningSpaces = beginningSpace
										posOfMax = pos
								pos = board[y - i][x + i]
								count = 1
								if space > 0:
									endSpace += space
									space = 0
									midSpace = 0
								else:
									endSpace = 0
									midSpace = 0
						else:
							if count == 0:
								beginningSpace += 1
							else:
								space += 1
							maxRow = y - i
			if space > 0:
				endSpace += space
			if (count > maxCount) & ((count + endSpace + midSpace + beginningSpace) >= 4):
				maxCount = count
				maxEndSpaces = endSpace
				maxMidSpaces = midSpace
				maxBeginningSpaces = beginningSpace
				maxRow = maxRow
				posOfMax = pos
			elif count == maxCount:
				if ((endSpace + midSpace + beginningSpace) > (maxEndSpaces + maxMidSpaces + beginningSpace)):
					maxEndSpaces = endSpace
					maxMidSpaces = midSpace
					maxBeginningSpaces = beginningSpace
					maxRow = maxRow
					posOfMax = pos
			if(y < 5):
				y += 1
			else:
				x += 1
		multiplier = self.getMultiplier(posOfMax, maxRow, 0)
		if((maxEndSpaces + maxMidSpaces + maxBeginningSpaces) > 0):
			if maxCount > 3:
				threat = 100 * (-5 * maxMidSpaces) * multiplier
			elif maxCount == 3:
				if (maxMidSpaces == 0):
					if (maxEndSpaces >= 1) & (maxBeginningSpaces >= 1):
						threat = 99 * multiplier
					else:
						threat = 95 * multiplier
				elif maxMidSpaces == 1:
					threat = 95 * multiplier
				else:
					threat = 95 * (-5 * maxMidSpaces) * multiplier
			elif maxCount == 2:
				if (maxMidSpaces == 0):
					if (maxEndSpaces >= 1):
						if(maxBeginningSpaces >= 1):
							threat = 80 * multiplier
						else:
							if(maxEndSpaces >= 2):
								threat = 80 * multiplier
							else:
								threat = 0
					else:
						if(maxBeginningSpaces > 2):
							threat = 80 * multiplier
						else:
							threat = 0
				else:
					if (maxMidSpaces + maxBeginningSpaces + maxEndSpaces) >= 2:
						threat = 80 * multiplier
					else:
						threat = 0
			else:
				if (maxMidSpaces + maxBeginningSpaces + maxEndSpaces) > 2:
					threat = 10 * multiplier
				else:
					threat = 0
		else:
			threat = 0	
		# print("I exit here, right")
		# print("maxCount ", maxCount, ", numOfSpaces ", (maxBeginningSpaces + maxEndSpaces + maxMidSpaces), ", multiplier ", multiplier, ", threat", threat)
		# print(board)
		return threat

	def diagWin(self,board):
		return max(self.leftDiagWin(board), self.rightDiagWin(board))

	def evaluateBoard(self, board):
		hor = self.horWin(board) 
		vert = self.vertWin(board) 
		diag = self.diagWin(board)
		threats = sorted([abs(hor), abs(vert), abs(diag)])
		if threats[1] == threats[2]:
			return 0
		else:
			if threats[2] == abs(hor):
				#print("hor, ",hor)
				return hor
			elif threats[2] == abs(vert):
				#print("vert, ",vert)
				return vert
			else:
				#print("diag, ",diag)
				return diag
		# return max(hor, vert, diag)

	
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
				#print("hello")
				cp = board.copy()
				move = self.applyMove(cp, posMove, position)
				leaves.append(self.minValue(move, depth, curDepth + 1))
			for node in range(len(leaves)):
				if leaves[node] == max(leaves):
					print("I return a move")
					return moves[node]
		elif curDepth == depth:
			for posMove in moves:
				#print("hi")
				cp = board.copy()
				move = self.applyMove(cp, posMove, position)
				eval = self.evaluateBoard(move)
				leaves.append(eval)
			return max(leaves)
		else:
			for posMove in moves:
				#print("hola")
				cp = board.copy()
				move = self.applyMove(cp,posMove, position)
				leaves.append(self.minValue(move, depth, curDepth + 1))
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
		position = self.opponent.position
		moves = self.possibleMoves(board)
		leaves = []
		if curDepth == depth:
			for posMove in moves:
				#print("arigato")
				cp = board.copy()
				move = self.applyMove(cp, posMove, position)
				eval = self.evaluateBoard(move)
				leaves.append(eval)
			return min(leaves)
		else:
			for posMove in moves:
				#print("baka")
				cp = board.copy()
				move = self.applyMove(cp, posMove, position)
				leaves.append(self.maxValue(move, depth, curDepth + 1))
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




