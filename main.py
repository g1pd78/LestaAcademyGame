import pygame
import random

WIDTH = 800
HEIGHT = 650
FPS = 30

SELECTED = (144, 23, 32)
BACKGROUND = (167, 181, 32)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (195, 85, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128,128,128)
LIGHT_GRAY = (211,211,211)
FieldXs = 300
FieldYs = HEIGHT / 2 - 100

MovingBlock = False
MovableBlock = None
# TODO: class to store movable block

class Border(pygame.sprite.Sprite):
	def __init__(self, objType: str, gameFieldX=None, gameFieldY=None, isCurrent = False):
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
		all_sprites.add(self.border)
		all_sprites.remove(self)
		all_sprites.add(self)


	def removeBorder(self):
		all_sprites.remove(self.border)


	def update(self, key):
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
					if abs(MovableBlock.gameFieldY - self.gameFieldY) <= 1 and \
					abs(MovableBlock.gameFieldX - self.gameFieldX) <= 1 and \
					GameField[self.gameFieldY][self.gameFieldX] == 'FREE_SPACE':
						self.swapBlocks(MovableBlock)
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


	def swapBlocks(self, firstBlock):
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


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


RuleList = ['GREEN', 'BLUE', 'ORANGE']
random.shuffle(RuleList)

RuleBlock1 = Block(RuleList[0], 0, -3)
RuleBlock2 = Block(RuleList[1], 2, -3)
RuleBlock3 = Block(RuleList[2], 4, -3)

MovebleBlockList = ['GREEN'] * 5 + ['BLUE'] * 5 + ['ORANGE'] * 5
random.shuffle(MovebleBlockList)

GameField = [
['MAYBE_USED', 'BLOCK', 'MAYBE_USED', 'BLOCK', 'MAYBE_USED'],
['MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED'],
['MAYBE_USED', 'BLOCK', 'MAYBE_USED', 'BLOCK', 'MAYBE_USED'],
['MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED', 'FREE_SPACE', 'MAYBE_USED'],
['MAYBE_USED', 'BLOCK', 'MAYBE_USED', 'BLOCK', 'MAYBE_USED'],
]


for y in range(len(GameField)):
	for x in range(len(GameField[0])):
		if GameField[y][x] == 'MAYBE_USED':
			GameField[y][x] = MovebleBlockList[-1]
			MovebleBlockList.pop()

del MovebleBlockList

GameList = []
CurrentCoords = (0, 0)

def drawField():
	for y in range(len(GameField)):
		for x in range(len(GameField[0])):
			isCurrent = False
			if (x, y) == CurrentCoords:
				isCurrent = True
			PlayableBlock = Block(GameField[y][x], x, y, isCurrent)
			GameList.append(PlayableBlock)

drawField()

all_sprites.add([RuleBlock1, RuleBlock2, RuleBlock3] + GameList)

def checkForWinCondition():
	GameOver = True
	for i in range(5):
		if GameField[i][0] != RuleList[0] or GameField[i][1] != RuleList[1] or GameField[i][2] != RuleList[2]:
			GameOver = False
	return GameOver



running = True
while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN: 
				for i in GameList:
					if i.isCurrent:
						i.update('DOWN')
						break
			elif event.key == pygame.K_UP: 
				for i in GameList:
					if i.isCurrent:
						i.update('UP')
						break
			elif event.key == pygame.K_LEFT: 
				for i in GameList:
					if i.isCurrent:
						i.update('LEFT')
						break
			elif event.key == pygame.K_RIGHT: 
				for i in GameList:
					if i.isCurrent:
						i.update('RIGHT')
						break
			elif event.key == pygame.K_RETURN: 
				for i in GameList:
					if i.isCurrent:
						i.update('RETURN')
						break
			elif event.key == pygame.K_RSHIFT: 
				for i in GameList:
					if i.isCurrent:
						i.update('RSHIFT')
						break

	running = not checkForWinCondition()
	
	screen.fill(BACKGROUND)
	all_sprites.draw(screen)
	pygame.display.flip()

print('Game Over!')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Game Over!', True, green)
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)
pygame.display.update()
# test it 