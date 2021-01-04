# необходимые библиотеки:
import os
import sys
import pygame
import random
FPS = 30
# Обозначения клеток
SYMBOLS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# Состояния кораблей в начале, при установки, в ходе игры
CONDITIONS = ['free', 'fixed', 'in the game']


# необходимые функции
def load_image(name):
    fullname = os.path.join('data\images', name)
    image = pygame.image.load(fullname)
    return image


def terminate():
    # ***Сохранение игры***
    pygame.quit()
    sys.exit()


# необходимые классы:
# класс начальной заставки
class Screens:
    def __init__(self):
        self.fon = pygame.Surface((720, 400))
        self.clock = pygame.time.Clock()
        self.buttons_pos = []
        self.intro_text = []

    def draw(self):
        screen.blit(self.fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in self.intro_text:
            self.buttons_pos.append(text_coord)
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            self.clock.tick(FPS)


class StartScreen(Screens):
    def __init__(self):
        super().__init__()
        self.fon = pygame.transform.scale(load_image('Battle.jpg'),
                                          (width, height))
        self.intro_text = ["Игра", "",
                           "Морской бой",
                           "классический"]


# на случай ошибок
class ErrorScreen(Screens):
    def __init__(self):
        super().__init__()
        self.fon = pygame.transform.scale(load_image('error.jpg'),
                                          (width, height))
        self.intro_text = ['Возникла ошибка',
                           'Возможно, не хватает некоторых файлов',
                           'На данный момент играть невозможно!']


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


# классы полей игрока и бота
# игрока:
class BoardPlayer:
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
        for x in range(self.width - 1):
            for y in range(self.height - 1):
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


# бота:
class BoardBot:
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
        for x in range(self.width - 1):
            for y in range(self.height - 1):
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

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (self.left + self.cell_size < x < self.left + self.width * self.cell_size and
                self.top + self.cell_size < y < self.top + self.height * self.cell_size):
            x = (x - self.left) // self.cell_size - 1
            y = (y - self.top) // self.cell_size - 1
            print((x, y))

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


# основной класс для всех кораблей
class Ships(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, size):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.size = size
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, size)
        self.condition = CONDITIONS[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x = x_pos
        self.y = y_pos
        self.mouse = False

    def update(self):
        if self.condition == 'free' or self.condition == 'fixed':
            pass
        else:
            pass

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x = pos[0]
        self.y = pos[1]


# отдельные классы для каждого типа кораблей
class Ship1(Ships):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, (30, 30))


class Ship2(Ships):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, (61, 30))


class Ship3(Ships):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, (92, 30))


class Ship4(Ships):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, (123, 30))


# инициализация и игроковй цикл
pygame.init()
size = width, height = 720, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
error = ErrorScreen()
try:
    all_sprites = pygame.sprite.Group()
    start_screen = [StartScreen(), False]
    start_screen[0].draw()

    board_player = BoardPlayer(11, 11)  # потом этот шаг надо оптимизировать
    board_player.set_view(20, 40, 30)

    board_bot = BoardBot(11, 11)
    board_bot.set_view(400, 40, 30)
    # выводим вначале игры выводим все корабли
    player_ships = []
    x = 10
    y = 350
    # первые
    for _ in range(4):
        player_ships.append(Ship1('ship1.png', x, y))
        x += 35
    x = 10
    y += 35
    # вторые
    for _ in range(3):
        player_ships.append(Ship2('ship2.png', x, y))
        x += 66
    x = 10
    y += 35
    # третьи
    for _ in range(2):
        player_ships.append(Ship3('ship3.png', x, y))
        x += 97
    x = 10
    y += 35
    # четвертые
    for _ in range(1):
        player_ships.append(Ship4('ship4.png', x, y))
        x += 128
    clock = pygame.time.Clock()
    # таймер использовать будем при ходе ИИ
    TIMER = pygame.USEREVENT + 1
    running = True
    move = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and\
                event.key == pygame.K_ESCAPE and not(start_screen[1]):
                # Вновь рисуем стартовое окно в случае, если нажат Esc
                start_screen[1] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos0 = event.pos
                for ship in player_ships:
                    if ship.x <= pos0[0] <= ship.x + ship.size[0] and\
                            ship.y <= pos0[1] <= ship.y + ship.size[1] and\
                            (ship.condition == 'free' or
                             ship.condition == 'fixed'):
                        ship.mouse = True
                        move = True
                board_bot.get_click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                pos0 = event.pos
                for ship in player_ships:
                    for ship in player_ships:
                        ship.mouse = False
                    move = False
            if event.type == pygame.MOUSEMOTION and move:
                pos = (event.pos[0] - pos0[0], event.pos[1] - pos0[1])
                for ship in player_ships:
                    if ship.mouse:
                        ship.move((ship.x + pos[0], ship.y + pos[1]))
                pos0 = event.pos
        screen.fill(pygame.Color('white'))
        if start_screen[1]:
            start_screen[0].draw()
            start_screen[1] = False
        board_player.render()
        board_bot.render()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
except Exception as ex:
    print(ex)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('red'))
        error.draw()
        pygame.display.flip()
        clock.tick(FPS)
