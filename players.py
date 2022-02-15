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

	def rowOfMove(self, board, move, position):
		topPosition = len(board)
		# print(topPosition)
		# print("move = ", move)
		# print("position = ", position)
		for i in range(topPosition):
			# print("i = ", i)
			# print("board[i][move] = ", board[i][move])
			# print(board)
			if board[i][move] == position:
				rowOfMove = i
				return rowOfMove

	def horWin(self, board, move, position):
		inARow = 0
		rowOfMove = self.rowOfMove(board, move, position)
		for col in range(len(board[0])):
			if board[rowOfMove][col] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False

	def vertWin(self, board, move, position):
		inARow = 0
		for row in range(len(board)):
			if board[row][move] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False

	def leftDiagWin(self, board, move, position):
		inARow = 0
		rowOfMove = self.rowOfMove(board, move, position)
		diff = min(rowOfMove, move)
		x = move - diff
		y = rowOfMove - diff
		for i in range(len(board) - y):
			if board[y + i][x + i] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False
	
	def rightDiagWin(self, board, move, position):
		inARow = 0
		rowOfMove = self.rowOfMove(board, move, position)
		diff = min(rowOfMove, move)
		x = move + diff
		y = rowOfMove - diff
		for i in range(len(board) - y):
			if board[y + i][x - i] == position:
				inARow += 1
				if inARow == 4:
					return True
			else:
				inARow = 0
		return False

	def diagWin(self,board, move, position):
		return (self.leftDiagWin(board, move, position) | self.rightDiagWin(board, move, position))

	def isGameOver(self,board, move, position):
		if self.horWin(board,move,position) | self.vertWin(board,move,position) | self.diagWin(board,move,position):
			if position == self.position:
				return 100
			else:
				return -100
		else:
			return 0

	def evalByCountAndType(self, count, numThreats, type):
		if numThreats == 0:
				eval = 0
		else:
			if type == 1:
				if count == 1:
					eval = 5
				elif count == 2:
					eval = 10
				else:
					count = 20
			if type == 2:
				if count == 1:
					eval = 5
				elif count == 2:
					eval = 15
				else:
					count = 30
			if type == 3:
				if count == 1:
					eval = 5
				elif count == 2:
					eval = 15
				else:
					count = 30
		return eval

	def edgeCase(self, board, row, col, rowIter, colIter, type):
		newRow = row
		newCol = col
		count = 0
		blockCount = 0
		spaceCount = 0
		position = board[row][col]
		while ((newRow >= 0 & newRow < len(board)) | (newCol >= 0 & newCol < len(board[0]))):
			if (board[newRow][newCol] == position):
				if(blockCount == 0):
					if (spaceCount < 3):
						if (count < 3):
							count += 1
						else:
							break
					else:
						break
				else:
					break
			elif (board[newRow][newCol] != position) & (board[newRow][newCol] != 0):
				if (abs(newRow - row + blockCount) == 1) | (abs(newCol - col + blockCount) == 1):
					blockCount += 1
				else:
					break
			else:
				if(blockCount == 0):
					spaceCount += 1
				else:
					break
			newRow += rowIter
			newCol += colIter
		if count > blockCount:
			threat = self.evalByCountAndType(count, spaceCount, type)
		else:
			threat = self.evalByCountAndType(blockCount, 0, 4)
		return threat

	def middleCase(self, board, row, col, rowIter1, colIter1, rowIter2, colIter2):
		newRow = row
		newCol = col
		count = 0
		blockCount = 0
		spaceCount = 0
		position = board[row][col]
		while ((newRow >= 0 & newRow < len(board)) | (newCol >= 0 & newCol < len(board[0]))):
			if (board[newRow][newCol] == position):
				if(blockCount == 0):
					if (spaceCount < 3):
						if (count < 3):
							count += 1
						else:
							break
					else:
						break
				else:
					break
			elif (board[newRow][newCol] != position) & (board[newRow][newCol] != 0):
				if (abs(newRow - row + blockCount) == 1) | (abs(newCol - col + blockCount) == 1):
					blockCount += 1
				else:
					break
			else:
				if(blockCount == 0):
					spaceCount += 1
				else:
					break
			newRow += rowIter
			newCol += colIter
		if count > blockCount:
			threat = self.evalByCountAndType(count, spaceCount, type)
		else:
			threat = self.evalByCountAndType(blockCount, 0, 4)
		return threat

	def vertThreat(self, board, row, col):
		if row == 0:
			threatList = self.edgeCase(board, row, col, 1, 0)
			threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 1)
		return threatList
			
	def horThreat(self, board, row, col):
		if col == 0:
			threatList = self.edgeCase(board, row, col, 0, 1)
			threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 2)
		else:
			threatList = self.middleCase(board, row, col, 0, -1, 0, 1)
			threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 2)
		return threatList

	def leftDiagThreat(self, board, row, col):
		threatList = []
		if(col == 0):
			if(row >= 3):
				threatList = self.edgeCase(board,row,col, -1, 1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		elif((col == len(board[0]))):
			if (row <=  (len(board) - 4)):
				threatList = self.edgeCase(board,row,col, 1, -1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)	
		elif(row == len(board) - 1):
			if col <= 3:
				threatList = self.edgeCase(board,row,col, -1, 1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		else:
			if (row + col >= 3) & (row + col < 9):
				threatList = self.middleCase(board,row,col, 1, -1, -1, 1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		return threatList
		
	def rightDiagThreat(self, board, row, col):
		threatList = []
		if(col == 0):
			if(row < len(board) - 3):
				threatList = self.edgeCase(board,row,col, 1, 1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		elif((col == len(board[0]))):
			if (row >=  3):
				threatList = self.edgeCase(board,row,col, -1, -1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		elif(row == len(board)):
			if col > 3:
				threatList = self.edgeCase(board,row,col, 1, 1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		else:
			if (row + col >= 3) & (row + col < 9):
				threatList = self.middleCase(board,row,col, -1, -1)
				threatList[0] = self.evalByCountAndType(threatList[0], len(threatList) - 1, 3)
			else:
				threatList.append(0)
		return threatList

	def diagThreat(self, board, row, col):
		left = self.leftDiagThreat(board, row, col)
		right = self.rightDiagThreat(board, row, col)
		if left[2] >= right[2]:
			return left
		else:
			return right

	def checklist(self, board, row, col):
		numThreats = 0
		checklist = []
		threatList = []
		l = []
		threatList.append(self.vertThreat(board, row, col))
		threatList.append(self.horThreat(board, row, col))
		threatList.append(self.diagThreat(board, row, col))
		for threat in threatList:
			if abs(threat[0]) == 30:
				numThreats += 1
				if len(checklist) == 0:
					checklist.append(1)
					for i in range(len(threat)):
						if i > 1:
							l.append(threat[i])
		if len(checklist) == 0:
			checklist.append(0)
		checklist.append(board[row][col])
		checklist.append(max(abs(threatList[0][0]), abs(threatList[1][0]), abs(threatList[2][0])))
		checklist.append(numThreats)
		for i in l:
			checklist.append(i)
		return checklist
			

	def sameThreat(threats):
		for x in range(len(threats)):
			for y in range(len(threats)):
				if x != y:
					if (threats[x][0] != threats[y][0]) & (threats[x][1] != threats[y][1]):
						return True
		return False

	def threats(self,board, position):
		l = []
		p1Threats = []
		p2Threats = []
		maxThreat = 0
		for col in range(len(board[0])):
			for row in range(len(board)):
				if board[row][col] != 0:
					checklist = self.checklist(board, row, col)
					if checklist[0] == 1: # whether theres threats or not
						if checklist[1] == 1: # player
							for i in range(checklist[3]):# number of threats
								l.append(checklist[4 + (2 * i)])
								l.append(checklist[5 + (2 * i)])
								p1Threats.append(l)
								l.clear()
						else:
							for i in range(checklist[3]): # number of threats
								l.append(checklist[4 + (2 * i)])
								l.append(checklist[5 + (2 * i)])
								p2Threats.append(l)
								l.clear()
					if abs(checklist[2]) > maxThreat: # eval
						maxThreat = checklist[2]
		if len(p1Threats) > 1:
			if not self.sameThreat(p1Threats):
				maxThreat = 95
		if len(p2Threats) > 2:
			if not self.sameThreat(p2Threats):
				if abs(maxThreat) < 95:
					maxThreat = -95
		return maxThreat

	def evaluateBoard(self,board, move, position):
		gameOver = self.isGameOver(board, move, position)
		if gameOver != 0:
			return gameOver
		else:
			threats = self.threats(board, position)
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
				eval = self.evaluateBoard(move, posMove, position)
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
				eval = self.evaluateBoard(move, posMove, position)
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




