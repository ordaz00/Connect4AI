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
		i = len(board[0])
		listOfMoves = []
		for col in range(i):
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
			if board[len(board) - row - 1][col] == 0:
				board[len(board) - row - 1][col] = position
				return board

	def horWin(self, board, row, col, position):
		inARow = 0
		for col in range(len(board[0])):
			if board[row][col] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False

	def vertWin(self, board, row, col, position):
		inARow = 0
		boardHeight = len(board)
		for row in range(boardHeight):
			if board[boardHeight - row - 1][col] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False

	def leftDiagWin(self, board, row, col, position):
		inARow = 0
		diff = min(row, col)
		x = col - diff
		y = row - diff
		for i in range(len(board) - y):
			if board[y + i][x + i] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False
	
	def rightDiagWin(self, board, row, col,  position):
		inARow = 0
		diff = min((len(board) - row - 1), col)
		x = col - diff
		y = row + diff
		for i in range(y + 1):
			if board[y - i][x + i] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False

	def diagWin(self,board, row, col,  position):
		return (self.leftDiagWin(board, row, col, position) | self.rightDiagWin(board, row, col, position))

	def isGameOver(self,board, row, col, position):
		if self.horWin(board, row, col, position) | self.vertWin(board, row, col, position) | self.diagWin(board, row, col, position):
			if position == self.position:
				return 100
			else:
				return -100
		else:
			return 0

	def edgeCaseEval(self, count, numThreats, window, evalType):
		windowLength = len(window)
		eval = 0
		if numThreats == 0:
			if evalType != 4:
				eval = 0
			else:
				eval = 75
		else:
			if evalType == 1:
				if count == 1:
					if numThreats < 3:
						eval = 0
					else:
						eval = 35
				elif count == 2:
					if numThreats < 2:
						eval = 0
					else:
						eval = 35
				else:
					eval = 70
			elif evalType == 2:
				if count == 1:
					if numThreats < 3:
						eval = 0
					else:
						eval = 35
				elif count == 2:
					if(windowLength == 4):
						eval = 0
					else:
						eval = 55
				else:
					if windowLength <= 5:
						eval = 70
					else:
						if window[4] == 0:
							eval = 70
						else:
							eval = 55
			elif evalType == 3:
				if count == 1:
					if numThreats == 3:
						eval = 35
					else:
						eval = 0
				elif count == 2:
					if windowLength == 4:
						eval = 0
					else:
						eval = 50
				else:
					if windowLength <= 5:
						eval = 65
					else:
						if window[4] == 0:
							eval = 65
						else:
							eval = 40
			else:
				if count == 1:
					eval = 15
				if count == 2:
					eval = 80
				else:
					eval = 60
		return eval

	def edgeCase(self, board, row, col, rowIter, colIter, evalType):
		newRow = row
		newCol = col
		count = 0
		blockCount = 0
		spaceCount = 0
		window = []
		threatHeight = []
		position = board[row][col]

		while ((newRow >= 0 & newRow < len(board)) & (newCol >= 0 & newCol < len(board[0]))):
			if (board[newRow][newCol] == position):
				if(blockCount == 0):
					if count < 3:
						window.append(board[newRow][newCol])
						count += 1
					else:
						window.append(board[newRow][newCol])
						break
				else:
					break
			elif (board[newRow][newCol] != position) & (board[newRow][newCol] != 0):
				if count > 1:
					window.append(board[newRow][newCol])
					break
				else:
					window.append(board[newRow][newCol])
					blockCount += 1
			else:
				if(blockCount == 0):
					if count == 3:
						window.append(board[newRow][newCol])
						threatHeight.append(newRow)
						spaceCount += 1
						break
					elif spaceCount == 2:
						window.append(board[newRow][newCol])
						threatHeight.append(newRow)
						spaceCount += 1
						break
					else:
						window.append(board[newRow][newCol])
						threatHeight.append(newRow)
						spaceCount += 1
				else:
					window.append(board[newRow][newCol])
					spaceCount += 1
					break
			newRow += rowIter
			newCol += colIter

		if window[1] == position | window[1] == 0:
			threat = self.edgeCaseEval(count, spaceCount, window, evalType)
		else:
			threat = self.edgeCaseEval(blockCount, spaceCount, window, 4)
		if count == 3:
			if len(window) <= 5 & spaceCount <= 2:
				if position == 1:
					if (threatHeight[0] + 1) % 2 == 0:
						threat = threat - threat/3
				else:
					if (threatHeight[0] + 1) % 2 == 1:
						threat = threat - threat/3
		elif count == 1:
			if spaceCount == 3:
				if position == 1:
					if (threatHeight[2] + 1) % 2 == 0:
						threat = threat - threat/3
				else:
					if (threatHeight[2] + 1) % 2 == 1:
						threat = threat - threat/3
		return threat

	def middleCase(self, board, row, col, rowIter1, colIter1, rowIter2, colIter2, evalType):
		leftRow = row + rowIter1
		leftCol = col + colIter1
		rightRow = row + rowIter2
		rightCol = col + colIter2
		spaceCount = 0
		position = board[row][col]
		x = len(board[0])
		y = len(board)
		if (board[leftRow][leftCol] == position) & (board[rightRow][rightCol] == position):
			leftRow += rowIter1
			leftCol += colIter1
			rightRow += rowIter2
			rightCol += colIter2
			if(leftRow >= 0 & leftRow < y) & (leftCol >= 0 & leftCol < x):
				if(board[row + (rowIter1 * 2)][col + (colIter1 * 2)] == position):
					spaceCount += 1
			if (rightRow >= 0 & rightRow < y) & (rightCol >= 0 & rightCol < x):
				if(board[row + (rowIter2 * 2)][col + (colIter2 * 2)] == position):
					spaceCount += 1
			return 95
		else:
			leftRow = row
			leftCol = col
			rightRow = row
			rightCol = col
			while(leftRow >= 0 & leftRow < y) & (leftCol >= 0 & leftCol < x):
				if (board[leftRow][leftCol] != position):
					break
				leftRow += rowIter1
				leftCol += colIter1
			while(rightRow >= 0 & rightRow < y) & (rightCol >= 0 & rightCol < x):
				if(board[rightRow][rightCol] != position):
					break
				rightRow += rowIter2
				rightCol += colIter2
			
			left =  self.edgeCase(board, (leftRow - rowIter1), (leftCol - colIter1), rowIter1, colIter1, evalType)
			right = self.edgeCase(board, (rightRow - rowIter2), (rightCol - colIter2), rowIter2, colIter2, evalType)
			return max(left, right)

	def vertThreat(self, board, row, col):
		if row == 0:
			threat = self.edgeCase(board, row, col, -1, 0, 1)
		else:
			threat = self.middleCase(board, row, col, -1, 0, 1, 0, 1)
		return threat
			
	def horThreat(self, board, row, col):
		if col == 0:
			threat = self.edgeCase(board, row, col, 0, 1, 2)
		elif col == (len(board[0]) - 1):
			threat = self.edgeCase(board, row, col, 0, -1, 2)
		else:
			threat = self.middleCase(board, row, col, 0, -1, 0, 1, 2)
		return threat

	def leftDiagThreat(self, board, row, col):
		if(col == 0):
			if(row < 3):
				threat = self.edgeCase(board, row, col, 1, 1, 3)
			else:
				return 0
		elif((col == len(board[0]) - 1)):
			if (row >=  3):
				threat = self.edgeCase(board,row,col, -1, -1, 3)
			else:
				return 0	
		elif(row == 0):
			if(col < 4):
				threat = self.edgeCase(board,row,col, 1, 1, 3)
			else:
				return 0
		elif(row == len(board) - 1):
			if col >= 3:
				threat = self.edgeCase(board,row,col, -1, -1, 3)
			else:
				return 0
		else:
			if (row == len(board) - 2 & col == 1) | (row == 1 & col == len(board[0]) - 2):
				threat = self.middleCase(board,row,col, -1, -1, 1, 1, 3)
			else:
				return 0
		return threat
		
	def rightDiagThreat(self, board, row, col):
		if(col == 0):
			if(row > 2):
				threat = self.edgeCase(board, row, col, -1, 1, 3)
			else:
				return 0
		elif((col == len(board[0]) - 1)):
			if (row <  3):
				threat = self.edgeCase(board, row, col, 1, -1, 3)
			else:
				return 0
		elif(row == 0):
			if(col >= 3):
				threat = self.edgeCase(board, row, col, 1, -1, 3)
			else:
				return 0
		elif(row == len(board)):
			if col < 4:
				threat = self.edgeCase(board, row, col, -1, 1, 3)
			else:
				return 0
		else:
			if (row == 1 & col == 1) | (row == len(board) - 2 & col == len(board[0]) - 2):
				threat = self.middleCase(board,row,col, 1, -1, -1, 1, 3)
			else:
				return 0
		return threat

	def diagThreat(self, board, row, col):
		left = self.leftDiagThreat(board, row, col)
		right = self.rightDiagThreat(board, row, col)
		if left[2] >= right[2]:
			return left
		else:
			return right

	def threats(self, board, row, col):
		threats = []
		threats.append(self.vertThreat(board, row, col))
		threats.append(self.horThreat(board, row, col))
		threats.append(self.diagThreat(board, row, col))
		return max(threats)

	def evaluateBoard(self, board):
		for row in range(len(board)):
			for col in range(len(board[0])):
				position = board[row][col]
				gameOver = self.isGameOver(board, row, col, position)
				if gameOver != 0:
					return gameOver
				else:
					threats = self.threats(board, row, col)
					return threats
	
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
				move = self.applyMove(board,posMove, position)
				leaves.append(self.minValue(move,depth, curDepth + 1))
			for node in leaves:
				if leaves[node] == max(leaves):
					return node
		elif curDepth == depth:
			for posMove in moves:
				move = self.applyMove(board,posMove, position)
				eval = self.evaluateBoard(move)
				leaves.append(eval)
			return max(abs(leaves))
		else:
			for posMove in moves:
				move = self.applyMove(board,posMove, position)
				leaves.append(self.minValue(move,depth, curDepth + 1))
			return max(abs(leaves))

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
				move = self.applyMove(board, posMove, position)
				eval = self.evaluateBoard(move)
				leaves.append(eval)
			return min(leaves)
		else:
			for posMove in moves:
				move = self.applyMove(board,posMove, position)
				leaves.append(self.maxValue(move,depth, curDepth + 1))
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




