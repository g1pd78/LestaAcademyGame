import pygame
import time
from colors import *
from parameters import *
import fieldClass

 
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

field = fieldClass.Field
field.generateField(field)
all_sprites.add(field.GameList)


running = True
while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN: 
				for i in field.GameList:
					if i.isCurrent:
						i.update('DOWN', field.GameList)
						break
			elif event.key == pygame.K_UP: 
				for i in field.GameList:
					if i.isCurrent:
						i.update('UP', field.GameList)
						break
			elif event.key == pygame.K_LEFT: 
				for i in field.GameList:
					if i.isCurrent:
						i.update('LEFT', field.GameList)
						break
			elif event.key == pygame.K_RIGHT: 
				for i in field.GameList:
					if i.isCurrent:
						i.update('RIGHT', field.GameList)
						break
			elif event.key == pygame.K_RETURN: 
				for i in field.GameList:
					if i.isCurrent:
						i.update('RETURN', field.GameList, field.GameField)
						break
			elif event.key == pygame.K_RSHIFT: 
				for i in field.GameList:
					if i.isCurrent:
						i.update('RSHIFT', field.GameList)
						break

	running = not field.checkForWinCondition(field)
	screen.fill(BACKGROUND)
	all_sprites.draw(screen)
	k = 0
	for i in gameRulesMessage.split('\n'):
		k+=1
		text_surface = my_font.render(i, False, TEXT)
		screen.blit(text_surface, (0, k * 30 + 400))
	pygame.display.flip()

if not running:
	text_surface = my_font.render(gameOverMessage, False, TEXT)
	screen.blit(text_surface, (0, 450))
	pygame.display.flip()
	time.sleep(2)

#todo: правила слева выписать
#чуть изменить гейм овер