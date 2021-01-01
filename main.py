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
        self.fon = pygame.transform.scale(load_image('Battle.jpg'), (width, height))
        self.clock = pygame.time.Clock()

    def draw(self):
        intro_text = ["Игра", "",  # пока написал так, потом можно поправить
                      "Морской бой",
                      "классический"]

        screen.blit(self.fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(FPS)


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


# классы полей игрока и бота
# игрока:

class Board_Player:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top,
                                 self.cell_size, self.cell_size), 1)
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                pygame.draw.rect(screen, pygame.Color('blue'),
                                 (x * self.cell_size + self.left + self.cell_size,
                                  y * self.cell_size + self.top + self.cell_size,
                                  self.cell_size, self.cell_size), 1)


class Board_Bot:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top,
                                 self.cell_size, self.cell_size), 1)
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                pygame.draw.rect(screen, pygame.Color('blue'),
                                 (x * self.cell_size + self.left + self.cell_size,
                                  y * self.cell_size + self.top + self.cell_size,
                                  self.cell_size, self.cell_size), 1)


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
size = width, height = 720, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')

all_sprites = pygame.sprite.Group()
start_screen = StartScreen()
start_screen.draw()

board_player = Board_Player(10, 10)  # потом этот шаг надо оптимизировать
board_player.set_view(20, 40, 30)

board_bot = Board_Bot(10, 10)
board_bot.set_view(400, 40, 30)

clock = pygame.time.Clock()
# таймер использовать будем при ходе ИИ
TIMER = pygame.USEREVENT + 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    screen.fill(pygame.Color('white'))
    board_player.render()
    board_bot.render()
    pygame.display.flip()
    clock.tick(FPS)
