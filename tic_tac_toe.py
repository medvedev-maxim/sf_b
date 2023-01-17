def draw_field(l_c):
    print("\n  0 1 2")
    for j in range(3):
        print(j, *l_c[j * 3:j * 3 + 3])


def check_winner(res, t):
    s = "O" if t % 2 == 0 else "X"

    if res[0] == res[1] == res[2] == s or res[3] == res[4] == res[5] == s or res[6] == res[7] == res[8] == s or \
            res[6] == res[7] == res[8] == s or res[0] == res[3] == res[6] == s or res[1] == res[4] == res[7] == s or \
            res[2] == res[5] == res[8] == s or res[0] == res[4] == res[8] == s or res[2] == res[4] == res[6] == s:
        if s == "X":
            return 1  # Выйграл первый игрок
        else:
            return 2  # Выйграл второй игрок
    else:
        return False


def game():
    cells = ["_" for _ in range(9)]
    turn = 1
    verif = {"0", "1", "2"}
    draw_field(cells)

    while True:

        print(f"\nХод {2 - turn % 2} игрока.")

        while True:
            move = list(input("Введите номер строки и столбца двузначным числом: ").replace(" ", ""))
            if not set(move).difference(verif) and len(move) == 2:
                move = list(map(int, move))
                if cells[move[0] * 3 + move[1]] == "_":
                    break
                else:
                    print("Ячейка не пустая. Попробуйте еще раз!\n")
            else:
                print("Ввели неправильное значение. Попробуйте еще раз!\n")

        cells[move[0] * 3 + move[1]] = "O" if turn % 2 == 0 else "X"

        draw_field(cells)
        winner = check_winner(cells, turn)

        if winner:
            print(f"\nПобедил {winner} игрок!!!\n")
            break

        if winner is False and turn == 9:
            print(f"\nНичья!!!")
            break

        turn += 1


print("""\
████████╗██╗░█████╗░  ████████╗░█████╗░░█████╗░  ████████╗░█████╗░███████╗\n\
╚══██╔══╝██║██╔══██╗  ╚══██╔══╝██╔══██╗██╔══██╗  ╚══██╔══╝██╔══██╗██╔════╝\n\
░░░██║░░░██║██║░░╚═╝  ░░░██║░░░███████║██║░░╚═╝  ░░░██║░░░██║░░██║█████╗░░\n\
░░░██║░░░██║██║░░██╗  ░░░██║░░░██╔══██║██║░░██╗  ░░░██║░░░██║░░██║██╔══╝░░\n\
░░░██║░░░██║╚█████╔╝  ░░░██║░░░██║░░██║╚█████╔╝  ░░░██║░░░╚█████╔╝███████╗\n\
░░░╚═╝░░░╚═╝░╚════╝░  ░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░  ░░░╚═╝░░░░╚════╝░╚══════╝\n\n\
Игра "Крестики нолики" для 2-х игроков (каждый ходит поочередно)\n""")

while True:
    game()
    if input("Введите Y для повторной игры или любой символ для прекращения: ").lower() != "y":
        break
