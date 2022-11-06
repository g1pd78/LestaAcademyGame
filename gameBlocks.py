import pygame
from colors import *
from parameters import *

MovingBlock = False
MovableBlock = None
currentSprites = all_sprites

class Border(pygame.sprite.Sprite):
	def __init__(self, objType: str, gameFieldX=None, gameFieldY=None):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 50))
		Block.setColor(self, objType)
		self.rect = self.image.get_rect()
		self.rect.center = (FieldXs + gameFieldX * 50, FieldYs + gameFieldY * 50)


class Block(pygame.sprite.Sprite):
	def __init__(self, objType: str, gameFieldX=None, gameFieldY=None, isCurrent = False):
		self.gameFieldX = gameFieldX
		self.gameFieldY = gameFieldY
		self.isCurrent = isCurrent
		self.gonnaBeMoved = False
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((40, 40))
		self.type = objType
		self.setColor(self.type)
		self.rect = self.image.get_rect()
		self.rect.center = (FieldXs + self.gameFieldX * 50, FieldYs + self.gameFieldY * 50)
		self.border = []
		if isCurrent:
			self.addBorder('SELECTED', self.gameFieldX, self.gameFieldY)


	def addBorder(self, typeOfBorder, gameFieldX, gameFieldY):
		self.border.append(Border(typeOfBorder, gameFieldX, gameFieldY))
		currentSprites.add(self.border)
		currentSprites.remove(self)
		currentSprites.add(self)


	def removeBorder(self):
		currentSprites.remove(self.border)


	# лучше было бы сделать обработку вне класса блок 0_о
	def update(self, key, GameList, GameField = None):
		if key == 'DOWN':
			if self.gameFieldY + 1 < 5:
				for i in GameList:
					if i.gameFieldY == self.gameFieldY + 1 and i.gameFieldX == self.gameFieldX:
						self.changeSelected(i)
		elif key == 'UP':
			if self.gameFieldY - 1 >= 0:
				for i in GameList:
					if i.gameFieldY == self.gameFieldY - 1 and i.gameFieldX == self.gameFieldX:
						self.changeSelected(i)
		elif key == 'LEFT':
			if self.gameFieldX - 1 >= 0:
				for i in GameList:
					if i.gameFieldY == self.gameFieldY and i.gameFieldX == self.gameFieldX - 1:
						self.changeSelected(i)
		elif key == 'RIGHT':
			if self.gameFieldX + 1 < 5:
				for i in GameList:
					if i.gameFieldY == self.gameFieldY and i.gameFieldX == self.gameFieldX + 1:
						self.changeSelected(i)
		elif key == 'RETURN':
			global MovingBlock, MovableBlock
			if self is not MovableBlock:
				self.gonnaBeMoved = True
				if MovingBlock:
					if ((abs(MovableBlock.gameFieldX - self.gameFieldX) <= 1  and\
					 	abs(MovableBlock.gameFieldY - self.gameFieldY) == 0)   or\
					 	(abs(MovableBlock.gameFieldX - self.gameFieldX) == 0  and\
					 	abs(MovableBlock.gameFieldY - self.gameFieldY) <= 1)) and\
					 	GameField[self.gameFieldY][self.gameFieldX] == 'FREE_SPACE' and \
					 	GameField[MovableBlock.gameFieldY][MovableBlock.gameFieldX] in ['GREEN', 'BLUE', 'ORANGE']:

						self.swapBlocks(MovableBlock, GameField)
						MovingBlock = False
						self.addBorder('SELECTED', self.gameFieldX, self.gameFieldY)
					else:
						self.removeBorder()
						self.gonnaBeMoved = False
				else:
					MovingBlock = True
					MovableBlock = self
		elif key == 'RSHIFT':
			if MovableBlock:
				MovableBlock.removeBorder()
				MovableBlock.gonnaBeMoved = False
				MovableBlock = None
				MovingBlock = False
				self.removeBorder()
				self.gonnaBeMoved = False
				self.addBorder('SELECTED', self.gameFieldX, self.gameFieldY)


	def swapBlocks(self, firstBlock, GameField):
		GameField[self.gameFieldY][self.gameFieldX], GameField[firstBlock.gameFieldY][firstBlock.gameFieldX] \
		= GameField[firstBlock.gameFieldY][firstBlock.gameFieldX], GameField[self.gameFieldY][self.gameFieldX]
		firstBlock.type, self.type = self.type, firstBlock.type
		firstBlock.setColor(firstBlock.type)
		self.setColor(self.type)
		self.removeBorder()
		firstBlock.removeBorder()
		firstBlock.gonnaBeMoved = False
		self.gonnaBeMoved = False
		MovableBlock = None


	def changeSelected(self, anotherBlock):
		color = None
		if MovingBlock and not anotherBlock.gonnaBeMoved:
			color = 'RED'
		else:
			color = 'SELECTED'

		anotherBlock.addBorder(color, anotherBlock.gameFieldX, anotherBlock.gameFieldY)
		anotherBlock.isCurrent = True
		anotherBlock.image = pygame.Surface((40, 40))
		anotherBlock.setColor(anotherBlock.type)
		anotherBlock.rect = anotherBlock.image.get_rect()
		anotherBlock.rect.center = (FieldXs + anotherBlock.gameFieldX * 50, FieldYs + anotherBlock.gameFieldY * 50)
		self.isCurrent = False
		
		if not self.gonnaBeMoved:
			self.removeBorder()

		self.image = pygame.Surface((40, 40))
		self.setColor(self.type)
		self.rect = self.image.get_rect()
		self.rect.center = (FieldXs + self.gameFieldX * 50, FieldYs + self.gameFieldY * 50)


	def setColor(self, objType: str):
		if objType == 'GREEN':
			self.image.fill(GREEN)
		elif objType == 'BLUE':
			self.image.fill(BLUE)
		elif objType == 'ORANGE':
			self.image.fill(ORANGE)
		elif objType == 'BLOCK':
			self.image.fill(GRAY)
		elif objType == 'FREE_SPACE':
			self.image.fill(LIGHT_GRAY)
		elif objType == 'RED':
			self.image.fill(RED)
		elif objType == 'SELECTED':
			self.image.fill(SELECTED)