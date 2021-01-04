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


def add_ships():
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
        x += 65
    x = 10
    y += 35
    # третьи
    for _ in range(2):
        player_ships.append(Ship3('ship3.png', x, y))
        x += 95
    x = 10
    y += 35
    # четвертые
    for _ in range(1):
        player_ships.append(Ship4('ship4.png', x, y))
        x += 125


# необходимые классы:
# класс начальной заставки
class Screens:
    def __init__(self):
        self.fon = pygame.Surface((720, 400))
        self.clock = pygame.time.Clock()
        self.buttons_pos = []
        self.intro_text = []

    def draw(self):
        # выводим фон на окно
        screen.blit(self.fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in self.intro_text:
            # выводим текст
            self.buttons_pos.append(text_coord)
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        # цикл окна
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
        self.intro_text = ['Возникла ошибка:', '',
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

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (self.left + self.cell_size < x < self.left + self.width * self.cell_size and
                self.top + self.cell_size < y < self.top + self.height * self.cell_size):
            x = (x - self.left) // self.cell_size - 1
            y = (y - self.top) // self.cell_size - 1
            return x, y

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


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
        # добавляем спрайт
        self.add(all_sprites)
        self.size = list(size)
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, size)
        # указываем текущее состояние корабля
        self.condition = CONDITIONS[0]
        # указываем координаты и размеры спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x = x_pos
        self.y = y_pos
        # перенос корабля
        self.mouse = False

    def update(self, event):
        if event == 'rotate':
            # поворачиваем прямоугольник спрайта
            self.rect.width, self.rect.height = self.rect.height, self.rect.width
            self.size[0], self.size[1] = self.size[1], self.size[0]

    def move(self, pos):
        # переносим спрайт
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
        super().__init__(image, x, y, (60, 30))


class Ship3(Ships):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, (90, 30))


class Ship4(Ships):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, (120, 30))


# инициализация и игроковй цикл
pygame.init()
size = width, height = 720, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
# ошибка
error = ErrorScreen()
try:
    # создаем группу спрайтов
    all_sprites = pygame.sprite.Group()
    # создаем начальный экран
    start_screen = [StartScreen(), False]
    start_screen[0].draw()
    # создаем поле игрока
    board_player = BoardPlayer(11, 11)  # потом этот шаг надо оптимизировать
    board_player.set_view(20, 40, 30)
    # создаем поле бота
    board_bot = BoardBot(11, 11)
    board_bot.set_view(400, 40, 30)
    player_ships = []
    add_ships()
    clock = pygame.time.Clock()
    # таймер использовать будем при ходе ИИ
    TIMER = pygame.USEREVENT + 1
    running = True
    # переменная, отвечающая за перенос
    move = False
    rotate = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and\
                event.key == pygame.K_ESCAPE and not(start_screen[1]):
                # Вновь рисуем стартовое окно в случае, если нажат Esc
                start_screen[1] = True
            # поворачиваем
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for ship in player_ships:
                    if ship.mouse and move:
                        ship.image = pygame.transform.rotate(ship.image, 90)
                        ship.update('rotate')
                        rotate = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # запоминаем начальные координаты
                pos0 = event.pos
                # разрешаем переносить корабли
                for ship in player_ships:
                    if ship.x <= pos0[0] <= ship.x + ship.size[0] and\
                            ship.y <= pos0[1] <= ship.y + ship.size[1] and\
                            (ship.condition == 'free' or
                             ship.condition == 'fixed'):
                        ship.mouse = True
                        move = True
                board_bot.get_click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP and not(rotate):
                # запрещаем кораблям перемещаться
                for ship in player_ships:
                    for ship in player_ships:
                        ship.mouse = False
                    move = False
            if event.type == pygame.MOUSEMOTION and move:
                # считаем изменение координат
                pos = (event.pos[0] - pos0[0], event.pos[1] - pos0[1])
                # переносим координаты
                for ship in player_ships:
                    if ship.mouse:
                        ship.move((ship.x + pos[0], ship.y + pos[1]))
                # запоминаем новые координаты
                pos0 = event.pos
                rotate = False
        screen.fill(pygame.Color('white'))
        # выводим начальный экран
        if start_screen[1]:
            start_screen[0].draw()
            start_screen[1] = False
        # выводим поля
        board_player.render()
        board_bot.render()
        # выводим спрайты
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
except Exception as ex:
    # Указываем ошибку
    error.intro_text[1] = str(ex)
    clock = pygame.time.Clock()
    running = True
    # цикл выводит ошибку на экран
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('red'))
        error.draw()
        pygame.display.flip()
        clock.tick(FPS)
