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
        self.intro_text = []
        self.btns = []

    def draw(self):
        # выводим фон на окно
        screen.blit(self.fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in self.intro_text:
            # выводим текст
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
                    for btn in self.btns:
                        if btn.x <= event.pos[0] <= btn.x + btn.w and \
                                btn.y <= event.pos[1] <= btn.y + btn.h:
                            result = btn.run()
                            if not (result is None):
                                if 'Вы' in self.intro_text[-1]:
                                    del self.intro_text[-1]
                                return
            for btn in self.btns:
                screen.blit(btn.text, (btn.x, btn.y))
            pygame.display.flip()
            self.clock.tick(FPS)


class StartScreen(Screens):
    def __init__(self):
        super().__init__()
        self.fon = pygame.transform.scale(load_image('Battle.jpg'),
                                          (width, height))
        self.intro_text = ["Игра", "",
                           "Морской бой"]
        self.btns.append(ClassicButton('классический', 10, 180))


# на случай ошибок
class ErrorScreen(Screens):
    def __init__(self):
        super().__init__()
        self.fon = pygame.Surface((width, height))
        pygame.draw.rect(self.fon, (255, 0, 0), (0, 0, width, height), 0)
        self.intro_text = ['Возникла ошибка:', '',
                           'На данный момент играть невозможно!']


# класс для всех кнопок в игре (пока только как надписи)
class Buttons:
    def __init__(self, text_btn, x, y):
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(text_btn, 1, (0, 0, 255))
        self.x = x
        self.y = y
        self.w = self.text.get_width()
        self.h = self.text.get_height()

    def run(self):
        pass


class StartButton(Buttons):
    def run(self):
        for ship in game.player_ships:
            if ship.condition == CONDITIONS[0]:
                return
        game.game = True
        game.start_battle()


class ClassicButton(Buttons):
    def run(self):
        return 0


class Game_Bot:  # весь класс пока примерно накидал
    def __init__(self, player_map):
        self.status = None  # статус предыдущего хода на момент текущего
        self.was_damaged = []  # для записи данных предыдущего хода при попадании
        self.player_map = player_map  # нужно составить карту игрока по началу игры

    def shot(self):
        global y, x
        direction = ['left', 'right', 'up', 'down']  # для выбора направления стрельбы при попадании
        hit = True
        while hit:  # поиск незадействованной клетки
            x, y = random.randrange(0, 9), random.randrange(0, 9)
            if self.player_map[y][x] != 'x':
                # крестиком будет отмечать как-либо использованные клетки
                hit = False
        if self.player_map[y][x] == '.':  # сам ход бота
            self.player_map[y][x] = 'x'
            self.status = None
        elif (self.player_map[y][x] == '2' or  # в разные корабли будет по разному
              self.player_map[y][x] == '3' or
              self.player_map[y][x] == '4'):
            direct = random.choice(direction)
        elif self.player_map[y][x] == '1':
            pass

    def update(self):
        pass


# класс самой игры
class Game:
    def __init__(self):
        pygame.mixer.music.load('data\music\seabattle.mp3')
        pygame.mixer.music.play(-1)
        # создаем начальный экран
        self.error = ErrorScreen()
        self.start_screen = [StartScreen(), False]
        self.start_screen[0].draw()
        self.move = False
        self.rotate = False
        self.pos0 = (0, 0)
        self.game = False
        self.pos_mouse = None
        self.start_btn = [StartButton('Начать игру', 297, 10), False]
        self.buttons = [self.start_btn]
        self.enemy_map = []
        self.start_game()

    def start_battle(self):
        for ship in self.player_ships:
            ship.condition = CONDITIONS[2]
            self.board_player.set_board((ship.x, ship.y), ship)
        self.start_btn[1] = False
        self.enemy_map = self.set_enemy_map()
        self.board_bot.board = self.enemy_map
        self.win = None
        if random.choice(['ai', 'player']) == 'ai':
            self.ai_move()

    def draw(self):
        self.start_btn[1] = True
        screen.fill(pygame.Color('white'))
        # выводим начальный экран
        if self.start_screen[1]:
            self.start_btn[1] = False
            self.start_screen[0].draw()
            self.start_game()
            self.start_screen[1] = False
        # выводим спрайты
        self.group.draw(screen)
        for btn in self.buttons:
            if btn[1]:
                screen.blit(btn[0].text, (btn[0].x, btn[0].y))
        self.board_player.render()
        self.board_bot.render()

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

    def is_win(self):
        ships = 0
        points = 0
        for i in self.board_player.board:
            if '1' not in i and '2' not in i and '3' not in i and '4' not in i:
                ships += 1
            if i == ['.'] * 9:
                points += 1
        if ships == 9 and points != 9:
            self.win = 'Вы проиграли'
        ships = 0
        points = 0
        for i in self.board_bot.board:
            if '1' not in i and '2' not in i and '3' not in i and '4' not in i:
                ships += 1
            if i == ['.'] * 9:
                points += 1
        if ships == 9 and points != 9:
            self.win = 'Вы выиграли'

    def move_player(self, pos_mouse):
        move = self.board_bot.get_click(event.pos)
        self.is_win()
        if self.win:
            self.start_screen[1] = True
            self.start_screen[0].intro_text.append(self.win)
            self.game = False
            self.win = None
            return
        else:
            if move == '*':
                move = self.ai_move()
                while move != '*' and not(self.win):
                    move = self.ai_move()
                    self.is_win()
            if self.win:
                self.start_screen[1] = True
                self.start_screen[0].intro_text.append(self.win)
                self.game = False
                self.win = None
                return

    def ai_move(self):
        for y in range(len(self.board_player.board)):
            for x in range(len(self.board_player.board[y])):
                try:
                    if self.board_player.board[y][x] == 'x':
                        if self.board_player.board[y + 1][x] == '.':
                            self.board_player.board[y + 1][x] = '*'
                            return '*'
                        elif self.board_player.board[y + 1][x] in '1234':
                            self.board_player.check(x, y + 1)
                            return 'x'
                        elif self.board_player.board[y - 1][x] == '.':
                            self.board_player.board[y - 1][x] = '*'
                            return '*'
                        elif self.board_player.board[y - 1][x] in '1234':
                            self.board_player.check(x, y - 1)
                            return 'x'
                        elif self.board_player.board[y][x + 1] == '.':
                            self.board_player.board[y][x + 1] = '*'
                            return '*'
                        elif self.board_player.board[y][x + 1] in '1234':
                            self.board_player.check(x + 1, y)
                            return 'x'
                        elif self.board_player.board[y][x - 1] == '.':
                            self.board_player.board[y][x - 1] = '*'
                            return '*'
                        elif self.board_player.board[y][x - 1] in '1234':
                            self.board_player.check(x - 1, y)
                            return 'x'
                except IndexError:
                    pass
        x, y = random.randrange(9), random.randrange(9)
        while self.board_player.board[y][x] in 'x#':
            x, y = random.randrange(9), random.randrange(9)
        if self.board_player.board[y][x] in '1234':
            self.board_player.check(x, y)
            return 'x'
        elif self.board_player.board[y][x] == '.':
            self.board_player.board[y][x] = '*'
            return '*'

    def add_ships(self):
        x = 10
        y = 380
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

    def set_enemy_map(self):
        direction = ['down', 'right']
        # расстановка вражеских кораблей
        while True:
            col = 0  # количество выставленных кораблей
            map = [['.' for _ in range(9)] for _ in range(9)]
            # первые
            while col != 4:
                try:
                    x, y = random.randrange(0, 9), random.randrange(0, 9)
                    if (map[y][x] == '.' and map[y - 1][x - 1] == '.' and map[y - 1][x] == '.' and
                            map[y - 1][x + 1] == '.' and map[y][x + 1] == '.' and
                            map[y + 1][x + 1] == '.' and map[y + 1][x] == '.' and
                            map[y + 1][x - 1] == '.' and map[y][x - 1] == '.'):
                        map[y][x] = '1'
                        col += 1
                except IndexError:
                    pass
            # вторые
            col = 0
            while col != 3:
                try:
                    direct = random.choice(direction)
                    x, y = random.randrange(0, 8), random.randrange(0, 8)
                    if map[y][x] == '.':
                        if direct == 'right':
                            if (map[y - 1][x] == '.' and map[y + 1][x] == '.' and
                                    map[y][x - 1] == '.' and map[y][x + 1] == '.'
                                    and map[y - 1][x + 1] == '.' and map[y + 1][x + 1] == '.' and
                                    map[y][x + 2] == '.'
                                    and map[y - 1][x - 1] == '.' and map[y + 1][x - 1] == '.'
                                    and map[y + 1][x + 2] == '.' and map[y - 1][x + 2] == '.'):
                                map[y][x], map[y][x + 1] = '2', '2'
                                col += 1
                        elif direct == 'down':
                            if (map[y - 1][x] == '.' and map[y][x - 1] == '.' and map[y][
                                x + 1] == '.'
                                    and map[y + 1][x + 1] == '.' and map[y + 1][x - 1] == '.' and
                                    map[y + 2][x] == '.'
                                    and map[y - 1][x - 1] == '.' and map[y - 1][x + 1] == '.'
                                    and map[y + 2][x - 1] == '.' and map[y + 2][x + 1] == '.' and
                                    map[y + 1][x] == '.'):
                                map[y][x], map[y + 1][x] = '2', '2'
                                col += 1
                except IndexError:
                    pass
            # третьи
            col = 0
            i = 0
            while col != 2 and i <= 50:
                try:
                    direct = random.choice(direction)
                    x, y = random.randrange(0, 7), random.randrange(0, 7)
                    if map[y][x] == '.':
                        if direct == 'right':
                            if (map[y - 1][x] == '.' and map[y + 1][x] == '.' and map[y][
                                x - 1] == '.' and map[y - 1][x + 1] == '.' and map[y + 1][
                                x + 1] == '.'
                                    and map[y - 1][x + 2] == '.' and map[y + 1][x + 2] == '.' and
                                    map[y][x + 3] == '.'
                                    and map[y - 1][x - 1] == '.' and map[y + 1][x - 1] == '.'
                                    and map[y + 1][x + 3] == '.' and map[y - 1][x + 3] == '.'
                                    and map[y][x + 1] == '.' and map[y][x + 2] == '.'):
                                map[y][x], map[y][x + 1], map[y][x + 2] = '3', '3', '3'
                                col += 1
                        elif direct == 'down':
                            if (map[y + 1][x] == '.' and map[y][x + 1] == '.' and
                                    map[y][x - 1] == '.'
                                    and map[y + 1][x + 1] == '.' and map[y + 1][x - 1] == '.'
                                    and map[y + 2][x - 1] == '.' and map[y + 2][x + 1] == '.' and
                                    map[y + 3][x] == '.'
                                    and map[y - 1][x - 1] == '.' and map[y - 1][x + 1] == '.'
                                    and map[y + 3][x - 1] == '.' and map[y + 3][x + 1] == '.'
                                    and map[y - 1][x] == '.' and map[y + 2][x] == '.'):
                                map[y][x], map[y + 1][x], map[y + 2][x] = '3', '3', '3'
                                col += 1
                except IndexError:
                    pass
                i += 1
            if i >= 50:
                continue
            col = 0
            # четвёртый
            for x in range(9):
                for y in range(9):
                    try:
                        if (map[y][x] == '.' and map[y][x - 1] == '.' and map[y][x + 1] == '.' and
                                map[y][x + 2] == '.' and map[y][x + 3] == '.' and
                                map[y][x + 4] == '.' and
                                map[y - 1][x] == '.' and map[y - 1][x - 1] == '.' and
                                map[y - 1][x + 1] == '.' and
                                map[y - 1][x + 2] == '.' and map[y - 1][x + 3] == '.' and
                                map[y - 1][x + 4] == '.' and map[y + 1][x] == '.' and
                                map[y + 1][x - 1] == '.' and map[y + 1][x + 1] == '.' and
                                map[y + 1][x + 2] == '.' and map[y + 1][x + 3] == '.' and
                                map[y + 1][x + 4] == '.'):
                            map[y][x], map[y][x + 1], map[y][x + 2], \
                            map[y][x + 3] = '4', '4', '4', '4'
                            return map
                        elif (map[y][x] == '.' and map[y - 1][x] == '.' and map[y + 1][x] == '.' and
                              map[y + 2][x] == '.' and map[y + 3][x] == '.' and
                              map[y + 4][x] == '.' and
                              map[y][x - 1] == '.' and map[y - 1][x - 1] == '.' and
                              map[y + 1][x - 1] == '.' and map[y + 2][x - 1] == '.' and
                              map[y + 3][x - 1] == '.' and map[y + 4][x - 1] == '.' and
                              map[y][x + 1] == '.' and map[y - 1][x + 1] == '.' and
                              map[y + 1][x + 1] == '.' and map[y + 2][x + 1] == '.' and
                              map[y + 3][x + 1] == '.' and map[y + 4][x + 1] == '.'):
                            map[y][x], map[y + 1][x], map[y + 2][x], \
                            map[y + 3][x] = '4', '4', '4', '4'
                            return map
                    except IndexError:
                        pass


# классы полей игрока и бота
# игрока:
class BoardPlayer:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['.'] * 9 for _ in range(9)]
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
                if self.board[y][x] == '*':
                    pygame.draw.ellipse(screen,
                                        (0, 0, 0),
                                        (self.left + self.cell_size * (x + 1) + 3,
                                         self.top + self.cell_size * (y + 1) + 3,
                                         self.cell_size - 6,
                                         self.cell_size - 6), 0)
                if self.board[y][x] == 'x':
                    pygame.draw.rect(screen, pygame.Color('black'),
                                     (x * self.cell_size + self.left + self.cell_size + 5,
                                      y * self.cell_size + self.top + self.cell_size + 5,
                                      self.cell_size - 10, self.cell_size - 10), 3)
                if self.board[y][x] == '#':
                    pygame.draw.rect(screen, pygame.Color('black'),
                                     (x * self.cell_size + self.left + self.cell_size,
                                      y * self.cell_size + self.top + self.cell_size,
                                      self.cell_size, self.cell_size), 0)

    def get_cell(self, pos):
        x, y = pos
        if (self.left + self.cell_size < x < self.left + (self.width) * self.cell_size and
                self.top + self.cell_size < y < self.top + (self.height) * self.cell_size):
            x = (x - self.left) // self.cell_size - 1
            y = (y - self.top) // self.cell_size - 1
            return x, y

    def get_cell_set(self, pos):
        x, y = pos
        x = (x - self.left) // self.cell_size - 1
        y = (y - self.top) // self.cell_size - 1
        return x, y

    def set_board(self, pos, ship):
        cell = self.get_cell_set(pos)
        if ship.__class__.__name__ == 'Ship1':
            self.board[cell[1]][cell[0]] = '1'
        elif ship.__class__.__name__ == 'Ship2':
            self.board[cell[1]][cell[0]] = '2'
            if ship.direct == 'down':
                self.board[cell[1] + 1][cell[0]] = '2'
            elif ship.direct == 'right':
                self.board[cell[1]][cell[0] + 1] = '2'
        elif ship.__class__.__name__ == 'Ship3':
            self.board[cell[1]][cell[0]] = '3'
            if ship.direct == 'down':
                self.board[cell[1] + 1][cell[0]], self.board[cell[1] + 2][cell[0]] = '3', '3'
            elif ship.direct == 'right':
                self.board[cell[1]][cell[0] + 1], self.board[cell[1]][cell[0] + 2] = '3', '3'
        elif ship.__class__.__name__ == 'Ship4':
            self.board[cell[1]][cell[0]] = '4'
            if ship.direct == 'down':
                self.board[cell[1] + 1][cell[0]], self.board[cell[1] + 2][cell[0]], \
                self.board[cell[1] + 3][cell[0]] = '4', '4', '4'
            elif ship.direct == 'right':
                self.board[cell[1]][cell[0] + 1], self.board[cell[1]][cell[0] + 2], \
                self.board[cell[1]][cell[0] + 3] = '4', '4', '4'

    def check(self, x, y):
        if self.board[y][x] == '1' or \
                self.board[y][x] in '234' and \
                self.board[y][x + 1] not in '234' and \
                self.board[y][x - 1] not in '234' and \
                self.board[y + 1][x] not in '234' and \
                self.board[y - 1][x] not in '234':
            self.board[y][x] = '#'
            for i in range(1, 4):
                end = 0
                if y + i < len(self.board[0]):
                    if self.board[y][x + i] == 'x':
                        self.board[y][x + i] = '#'
                        end = 1
                if y - i >= 0:
                    if self.board[y][x - i] == 'x':
                        self.board[y][x - i] = '#'
                        end = 1
                if y + i < len(self.board):
                    if self.board[y + i][x] == 'x':
                        self.board[y + i][x] = '#'
                        end = 1
                if y - i >= 0:
                    if self.board[y - i][x] == 'x':
                        self.board[y - i][x] = '#'
                        end = 1
                if end == 0:
                    break
        else:
            self.board[y][x] = 'x'


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
                if self.board[y][x] == '*':
                    pygame.draw.ellipse(screen,
                                        (0, 0, 0),
                                        (self.left + self.cell_size * (x + 1) + 3,
                                         self.top + self.cell_size * (y + 1) + 3,
                                         self.cell_size - 6,
                                         self.cell_size - 6), 0)
                if self.board[y][x] == 'x':
                    pygame.draw.rect(screen, pygame.Color('black'),
                                     (x * self.cell_size + self.left + self.cell_size + 5,
                                      y * self.cell_size + self.top + self.cell_size + 5,
                                      self.cell_size - 10, self.cell_size - 10), 3)
                if self.board[y][x] == '#':
                    pygame.draw.rect(screen, pygame.Color('black'),
                                     (x * self.cell_size + self.left + self.cell_size,
                                      y * self.cell_size + self.top + self.cell_size,
                                      self.cell_size, self.cell_size), 0)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (self.left + self.cell_size < x < self.left + (self.width - 1) * self.cell_size and
                self.top + self.cell_size < y < self.top + (self.height - 1) * self.cell_size):
            x = (x - self.left) // self.cell_size - 1
            y = (y - self.top) // self.cell_size - 1
            return x, y

    def on_click(self, cell_coords):
        if self.board[cell_coords[1]][cell_coords[0]] == '.':
            self.board[cell_coords[1]][cell_coords[0]] = '*'
            return '*'
        if self.board[cell_coords[1]][cell_coords[0]] == '1' or \
                self.board[cell_coords[1]][cell_coords[0]] in '234' and \
                self.board[cell_coords[1]][cell_coords[0] + 1] not in '234' and \
                self.board[cell_coords[1]][cell_coords[0] - 1] not in '234' and \
                self.board[cell_coords[1] + 1][cell_coords[0]] not in '234' and \
                self.board[cell_coords[1] - 1][cell_coords[0]] not in '234':
            self.board[cell_coords[1]][cell_coords[0]] = '#'
            for x in range(1, 4):
                end = 0
                if cell_coords[0] + x < len(self.board[0]):
                    if self.board[cell_coords[1]][cell_coords[0] + x] == 'x':
                        self.board[cell_coords[1]][cell_coords[0] + x] = '#'
                        end = 1
                if cell_coords[0] - x >= 0:
                    if self.board[cell_coords[1]][cell_coords[0] - x] == 'x':
                        self.board[cell_coords[1]][cell_coords[0] - x] = '#'
                        end = 1
                if cell_coords[1] + x < len(self.board):
                    if self.board[cell_coords[1] + x][cell_coords[0]] == 'x':
                        self.board[cell_coords[1] + x][cell_coords[0]] = '#'
                        end = 1
                if cell_coords[1] - x >= 0:
                    if self.board[cell_coords[1] - x][cell_coords[0]] == 'x':
                        self.board[cell_coords[1] - x][cell_coords[0]] = '#'
                        end = 1
                if end == 0:
                    return '#'
        if self.board[cell_coords[1]][cell_coords[0]] in '234':
            self.board[cell_coords[1]][cell_coords[0]] = 'x'
            return 'x'

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if not (cell is None):
            res = self.on_click(cell)
            return res


# основной класс для всех кораблей
class Ships(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, size, group, direct='right'):
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
        self.direct = direct
        # перенос корабля
        self.mouse = False

    def update(self, event):
        if event == 'rotate':
            # поворачиваем прямоугольник спрайта
            self.rect.width, self.rect.height = self.rect.height, self.rect.width
            self.size[0], self.size[1] = self.size[1], self.size[0]
            if self.direct == 'right':
                self.direct = 'down'
            else:
                self.direct = 'right'
        elif event == 'move':
            if game.pos_mouse:
                new_x = game.board_player.left + game.board_player.cell_size * \
                        (game.pos_mouse[0] + 1)
                new_y = game.board_player.top + game.board_player.cell_size * \
                        (game.pos_mouse[1] + 1)
                self.rect.x = new_x - 30
                self.rect.y = new_y - 30
                self.rect.width += 60
                self.rect.height += 60
                if pygame.sprite.spritecollide(self, self.group, False) == [self]:
                    self.rect.x += 30
                    self.rect.y += 30
                    self.rect.width -= 60
                    self.rect.height -= 60
                    if game.board_player.get_cell((self.rect.x + self.rect.width,
                                                   self.rect.y + self.rect.height)):
                        self.condition = CONDITIONS[1]
                        self.x = new_x
                        self.y = new_y
                        return 0
                self.rect.x = self.x
                self.rect.y = self.y
                self.rect.width = self.size[0]
                self.rect.height = self.size[1]
                self.condition = CONDITIONS[0]

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
        self.lives = 1  # жизни, будут учитываться при попадании

    def is_destroid(self):
        if self.lives <= 0:
            self.destroid()

    def destroid(self):
        pass


class Ship2(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (60, 30), group)
        self.lives = 2


class Ship3(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (90, 30), group)
        self.lives = 3


class Ship4(Ships):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, (120, 30), group)
        self.lives = 4


# инициализация и игроковй цикл
pygame.init()
size = width, height = 720, 530
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
game = Game()
try:
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and \
                event.key == pygame.K_ESCAPE and not (game.start_screen[1]):
                # Вновь рисуем стартовое окно в случае, если нажат Esc
                game.start_screen[1] = True
            # поворачиваем
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game.rotate_ships()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.start_of_the_transport_ships()
                if game.game:
                    game.move_player(event.pos)
                else:
                    if game.start_btn[0].x <= event.pos[0] <= \
                            game.start_btn[0].x + game.start_btn[0].w and \
                            game.start_btn[0].y <= event.pos[1] <= \
                            game.start_btn[0].y + game.start_btn[0].h:
                        game.start_btn[0].run()
            if event.type == pygame.MOUSEBUTTONUP and not (game.rotate):
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
