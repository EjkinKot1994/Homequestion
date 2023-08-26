# По сути вся игра, в расчётном смысле этого слова - "сравнёр")
# Слово игровая ДОСКА окончательно достало. Буду его избегать
from random import randint

# Конструктор точки (аргументы - координаты), после этого можно будет сравнивать точки.
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr(self):
        return f"Dot({self.x}, {self.y})"

# Собственные исключения
class BoardException(Exception): # Класс - босс исключений, батя исключений
    pass

class BoardOutException(BoardException): # выстрел за доску
    def __str__(self):
        return "Вообще не туда!"

class BoardUsedException(BoardException): # выстрел в уже стреляную точку
    def __str__(self):
        return "Где-то я уже видел этот выстрел..."

class BoardWrongShipException(BoardException): # исключения для нормального размещения кораблей
    pass

# Класс этих сраных Bullship
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property # Так надо! (Вычисление свойств кораблей)
    def dots(self): # описание самих кораблей от носа
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot): # Проверка на попадание в корабль
        return shot in self.dots


# клас гипсокартона (Gipsum cardBOARD)
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["0"] * size for _ in range(size)]
        self.busy = []  # список занятых точек
        self.ships = []  # список кораблей

    def add_ship(self, ship):  # Проверка границ картона, или занятость точки соседними кораблями
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Контур этих же сраных Bullship и добавление их же на наш гипсокартон
    def contour(self, ship, verb=False):  # сдвиги точек, понятия не имею, как это работает.
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):  # Вывод доски - по сути упращения вызова игрового поля
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, d):  # Находиться ли точка за пределами доски
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):  # Логика выстрела
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен, добивать будешь?")
                    return True

        self.field[d.x][d.y] = "T"
        print("Не туда!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)

# Перекур...

# В качестве аргументов будет принимать две картонины игровые
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask() # Просим координаты
                repeat = self.enemy.shot(target) # Выполняем выстрел
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        print("Смотри, чё он выпалил:")
        return d

class User(Player):
    def ask(self):
        while True:
            print("Твоя очередь тащить!")
            cords = input("Ваш ход: ").split()
        # Проверки правильности ввода
            if len(cords) != 2:
                print(" Ну ты две-то координаты введи! ")
                print("   Зачем больше, или меньше?    ")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print("  Ну а числа-то где?  ")
                print(" Таковы правила игры! ")
                print(" Таков путь, прикинь! ")
                print("Два числа введи и всё!")
                print("       Давай!         ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


# Логика игры
class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True


        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):  # Расстановка кораблей
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()  # Подготовка картона к тгре (Ну, там грунтовка, покраска и прочая дичь)
        return board

    def greet(self):
        print("------------------------")
        print("    Приветсвуют вас     ")
        print("в игре 'морское побоище'")
        print("       сил тьмы         ")
        print("  дабы Вам было хорошо. ")
        print("------------------------")
        print("    формат ввода: x y   ")
        print("    x - номер строки    ")
        print("    y - номер столбца   ")

    def print_boards(self):
        print("-" * 30)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 30)
        print("Доска компьютера:")
        print(self.ai.board)

    def loop(self):
        num = 0
        while True:
            self.print_boards()

            if num % 2 == 0:
                print("-" * 30)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 30)
                print("Ходит компудахтер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 30)
                # зкште("------------------------------")
                print("Так, нужен утюг, клей, и паяльник")
                print("будем компудахтер откачивать")
                print("-" * 30)
                print("Ты победил!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 30)
                print("Ну, таков путь самурая. Неповезло")
                print("Зализывайте раны, оба!")
                print("Но ты сегодня проиграл,")
                print("как пользователь-самурай.")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()