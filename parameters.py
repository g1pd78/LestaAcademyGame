import pygame

WIDTH = 800
HEIGHT = 650
FPS = 30
FieldXs = 300
FieldYs = HEIGHT / 2 - 100

all_sprites = pygame.sprite.Group()

gameOverMessage = '''
Game Over!
Игра закончена, условие выполнено!
'''
gameRulesMessage = '''
Управление:
Стрелочки - передвижение
ENTER - выбрать фишку
SHIFT(правый) - отменить выбор
Коричневая метка - управляемая фишка
Красная метка - выбор фишки для замены
'''