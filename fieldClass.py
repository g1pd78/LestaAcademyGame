import random
from gameBlocks import Block

class Field():
	def __init__(self):
		self.GameField = []
		self.GameList = []
		self.RuleList = []


	def generateField(self):
		self.RuleList = ['GREEN', 'BLUE', 'ORANGE']
		random.shuffle(self.RuleList)

		RuleBlock1 = Block(self.RuleList[0], 0, -3)
		RuleBlock2 = Block(self.RuleList[1], 2, -3)
		RuleBlock3 = Block(self.RuleList[2], 4, -3)

		MovebleBlockList = ['GREEN'] * 5 + ['BLUE'] * 5 + ['ORANGE'] * 5
		random.shuffle(MovebleBlockList)

		self.GameField = [
		['MAYBE_USED', 'BLOCK', 'MAYBE_USED', 'BLOCK', 'MAYBE_USED'],
		['MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED'],
		['MAYBE_USED', 'BLOCK', 'MAYBE_USED', 'BLOCK', 'MAYBE_USED'],
		['MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED'],
		['MAYBE_USED', 'BLOCK', 'MAYBE_USED', 'BLOCK', 'MAYBE_USED'],
		]

		# Разметка цветами
		CurrentCoords = (0, 0)
		self.GameList = [RuleBlock1, RuleBlock2, RuleBlock3]
		for y in range(len(self.GameField)):
			for x in range(len(self.GameField[0])):
				isCurrent = False
				if self.GameField[y][x] == 'MAYBE_USED':
					self.GameField[y][x] = MovebleBlockList[-1]
					if (x, y) == CurrentCoords: # можно добавить (0, 0) до цикла, будет быстрее, 
						isCurrent = True # но вдруг я захочу начинать игру в случайной позиции
					MovebleBlockList.pop()

				PlayableBlock = Block(self.GameField[y][x], x, y, isCurrent)
				self.GameList.append(PlayableBlock)


	def checkForWinCondition(self):
		GameOver = True
		for i in range(5):
			if self.GameField[i][0] != self.RuleList[0] or\
			 self.GameField[i][2] != self.RuleList[1] or\
			 self.GameField[i][4] != self.RuleList[2]:
				GameOver = False
		return GameOver


# return RuleBlock1, RuleBlock2, RuleBlock3] + GameList