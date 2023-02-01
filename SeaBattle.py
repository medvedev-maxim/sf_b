from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)


class Ship:
    def __init__(self, nose, ln, ori):
        self.nose = nose
        self.ln = ln
        self.ori = ori
        self.lives = ln

    @property
    def dots(self):
        x = self.nose.x
        y = self.nose.y
        ship_d = [Dot(x, y)]

        for i in range(self.ln - 1):
            if self.ori == 0:
                x += 1
            elif self.ori == 1:
                y += 1
            ship_d.append(Dot(x, y))

        return ship_d

    def hit(self, shot):
        return shot in self.dots


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["О"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
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

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def lose(self):
        return self.count == 7

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, enemy):
        self.enemy = enemy  # Убрал хранение второго поля
        self.near = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        self.last_dot = None

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

    def ask_near(self, center):
        for dt in self.near:
            d = Dot(center.x + dt[0], center.y + dt[1])
            if not (self.enemy.out(d)) and d not in self.enemy.busy:
                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                return d
        return None

    def move(self):  # Переопределение функции для AI c учетом "обстрела" точки где ранили корабль
        while True:
            try:
                if self.last_dot is None:
                    target = self.ask()
                else:
                    target = self.ask_near(self.last_dot)
                    if target is None:
                        target = self.ask()
                        self.last_dot = None

                repeat = self.enemy.shot(target)
                if repeat:
                    self.last_dot = target

                return repeat
            except BoardException as e:
                print(e)


class User(Player):
    def ask(self):
        while True:
            # Для ускорения тестирования добавил возможность ввода без пробела
            text = input("Ваш ход: ").replace(" ", "")

            if not (text.isdigit()):
                print(" Введите числа! ")
                continue
            else:
                cords = int(text)

            if not 0 <= cords // 10 <= 9:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords // 10, cords % 10

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()

        self.ai = AI(co)
        self.us = User(pl)
        self.move_ai = 0
        self.move_us = 0

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
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
        board.begin()
        return board

    @staticmethod
    def greet():
        print("░██████╗███████╗░█████╗░  ██████╗░░█████╗░████████╗████████╗██╗░░░░░███████╗")
        print("██╔════╝██╔════╝██╔══██╗  ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║░░░░░██╔════╝")
        print("╚█████╗░█████╗░░███████║  ██████╦╝███████║░░░██║░░░░░░██║░░░██║░░░░░█████╗░░")
        print("░╚═══██╗██╔══╝░░██╔══██║  ██╔══██╗██╔══██║░░░██║░░░░░░██║░░░██║░░░░░██╔══╝░░")
        print("██████╔╝███████╗██║░░██║  ██████╦╝██║░░██║░░░██║░░░░░░██║░░░███████╗███████╗")
        print("╚═════╝░╚══════╝╚═╝░░╚═╝  ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚══════╝")
        print("-" * 60)
        print(" формат ввода: x y или xy ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def print_boards(self, hid=True):  # Вывод 2х досок сразу
        i = 0
        cel = "О" if hid is True else "■"
        brd = "\nПоле игрока:                   Поле компьютера:\n" \
              "  | 1 | 2 | 3 | 4 | 5 | 6 |      | 1 | 2 | 3 | 4 | 5 | 6 |\n"
        for a, b in zip(self.ai.enemy.field, self.us.enemy.field):
            brd += f"{i + 1} | " + " | ".join(a) + f" |    {i + 1} | " + " | ".join(b).replace("■", cel) + " |\n"
            i += 1
        return print(brd)

    def loop(self):
        num = 0
        while True:
            self.print_boards()

            if num % 2 == 0:
                print("-" * 60)
                print(f"Ходит пользователь! Ход {self.move_us + self.move_ai + 1}")
                repeat = self.us.move()
                self.move_us += 1
            else:
                print("-" * 60)
                print(f"Ходит компьютер! Ход {self.move_us + self.move_ai + 1}")
                repeat = self.ai.move()
                self.move_ai += 1

            if repeat:
                num -= 1

            if self.ai.enemy.lose():
                print("-" * 20)
                print(f"Компьютер выиграл за {self.move_ai} ходов!")
                break

            if self.us.enemy.lose():
                print("-" * 20)
                print(f"Игрок выиграл за {self.move_us} ходов!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
