# необходимые библиотеки:
import os
import sys
import pygame
import random
FPS = 30


# необходимые функции
def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    # ***Сохранение игры***
    pygame.quit()
    sys.exit()


# необходимые классы:
# класс начальной заставки
class StartScreen:
    def __init__(self):
        pass

    def draw(self):
        pass


class SavesScreen:
    def __init__(self):
        pass


class SettingScreen:
    def __init__(self):
        pass


# класс самой игры
class Game:
    def __init__(self, save=None):
        if save is None:
            pass
        else:
            pass

    def draw(self):
        pass

    def ai_move(self):
        pass


# основной класс для всех кораблей
class Ships(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

    def draw(self):
        pass

    def update(self):
        pass


# отдельные классы для каждого типа кораблей
class Ship1(Ships):
    def init(self):
        pass


class Ship2(Ships):
    def init(self):
        pass


class Ship3(Ships):
    def init(self):
        pass


class Ship4(Ships):
    def init(self):
        pass


# инициализация и игроковй цикл
# !!!Возможно, придется куда-то переносить!!!
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
# таймер использовать будем при ходе ИИ
TIMER = pygame.USEREVENT + 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    clock.tick(FPS)
