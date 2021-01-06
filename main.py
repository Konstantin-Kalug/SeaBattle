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
        self.fon = pygame.Surface((width, height))
        pygame.draw.rect(self.fon, (255, 0, 0), (0, 0, width, height), 0)
        self.intro_text = ['Возникла ошибка:', '',
                           'На данный момент играть невозможно!']


# класс самой игры
class Game:
    def __init__(self):
        # создаем начальный экран
        self.error = ErrorScreen()
        self.start_screen = [StartScreen(), False]
        self.start_screen[0].draw()
        self.move = False
        self.rotate = False
        self.pos0 = (0, 0)
        self.pos_mouse = None
        self.start_game()

    def draw(self):
        screen.fill(pygame.Color('white'))
        # выводим начальный экран
        if self.start_screen[1]:
            self.start_screen[0].draw()
            self.start_game()
            self.start_screen[1] = False
        # выводим поля
        self.board_player.render()
        self.board_bot.render()
        # выводим спрайты
        self.group.draw(screen)

    def draw_error(self):
        # Указываем ошибку
        self.error.intro_text[1] = str(ex)
        screen.fill(pygame.Color('red'))
        self.error.draw()

    def start_game(self):
        # перезапуск игры
        self.group = pygame.sprite.Group()
        self.player_ships = []
        self.add_ships()
        self.board_bot = BoardBot(11, 11)
        self.board_bot.set_view(400, 40, 30)
        self.board_player = BoardPlayer(11, 11)
        self.board_player.set_view(20, 40, 30)

    def rotate_ships(self):
        for ship in game.player_ships:
            if ship.mouse and game.move:
                ship.image = pygame.transform.rotate(ship.image, 90)
                ship.update('rotate')
                game.rotate = True

    def start_of_the_transport_ships(self):
        # запоминаем начальные координаты
        self.pos0 = event.pos
        # разрешаем переносить корабли
        for ship in self.player_ships:
            if ship.x <= self.pos0[0] <= ship.x + ship.size[0] and \
                    ship.y <= self.pos0[1] <= ship.y + ship.size[1] and \
                    (ship.condition == 'free' or
                     ship.condition == 'fixed'):
                ship.mouse = True
                self.move = True
                ship.condition = CONDITIONS[0]

    def no_move_ships(self):
        # запрещаем кораблям перемещаться
        for ship in self.player_ships:
            if ship.mouse:
                ship.mouse = False
                ship.update('move')
                self.move = False

    def fixing_ships(self, pos):
        # считаем изменение координат
        pos = (pos[0] - self.pos0[0], pos[1] - self.pos0[1])
        # переносим координаты
        for ship in self.player_ships:
            if ship.mouse:
                ship.move((ship.x + pos[0], ship.y + pos[1]))
        # запоминаем новые координаты
        self.pos0 = event.pos
        self.rotate = False


    def ai_move(self):
        pass

    def add_ships(self):
        x = 10
        y = 350
        # первые
        for _ in range(4):
            self.player_ships.append(Ship1('ship1.png', x, y, self.group))
            x += 35
        x = 10
        y += 35
        # вторые
        for _ in range(3):
            self.player_ships.append(Ship2('ship2.png', x, y, self.group))
            x += 65
        x = 10
        y += 35
        # третьи
        for _ in range(2):
            self.player_ships.append(Ship3('ship3.png', x, y, self.group))
            x += 95
        x = 10
        y += 35
        # четвертые
        for _ in range(1):
            self.player_ships.append(Ship4('ship4.png', x, y, self.group))
            x += 125


# классы полей игрока и бота
# игрока:
class BoardPlayer():
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
    def __init__(self, image, x_pos, y_pos, size, group):
        super().__init__(group)
        # добавляем спрайт
        self.add(group)
        self.group = group
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
        elif event == 'move':
            if game.pos_mouse:
                new_x = game.board_player.left + game.board_player.cell_size *\
                        (game.pos_mouse[0] + 1)
                new_y = game.board_player.top + game.board_player.cell_size *\
                        (game.pos_mouse[1] + 1)
                self.rect.x = new_x
                self.rect.y = new_y
                if pygame.sprite.spritecollideany(self, self.group) and\
                        game.board_player.get_cell((self.rect.x + self.rect.width,
                                                self.rect.y + self.rect.height)):
                    self.condition = CONDITIONS[1]
                    self.x = new_x
                    self.y = new_y
                else:
                    self.rect.x = self.x
                    self.rect.y = self.y

    def move(self, pos):
        # переносим спрайт
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x = pos[0]
        self.y = pos[1]


# отдельные классы для каждого типа кораблей
class Ship1(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (30, 30), group)


class Ship2(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (60, 30), group)


class Ship3(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (90, 30), group)


class Ship4(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (120, 30), group)


# инициализация и игроковй цикл
pygame.init()
size = width, height = 720, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
game = Game()
try:
    clock = pygame.time.Clock()
    # таймер использовать будем при ходе ИИ
    TIMER = pygame.USEREVENT + 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and\
                event.key == pygame.K_ESCAPE and not(game.start_screen[1]):
                # Вновь рисуем стартовое окно в случае, если нажат Esc
                game.start_screen[1] = True
            # поворачиваем
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game.rotate_ships()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.start_of_the_transport_ships()
                game.board_bot.get_click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP and not(game.rotate):
                game.pos_mouse = game.board_player.get_cell(event.pos)
                game.no_move_ships()
            if event.type == pygame.MOUSEMOTION and game.move:
                game.fixing_ships(event.pos)
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
except Exception as ex:
    clock = pygame.time.Clock()
    running = True
    # цикл выводит ошибку на экран
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        game.draw_error()
        pygame.display.flip()
        clock.tick(FPS)
