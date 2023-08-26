def greet():  # экран приветствия
    print(" _________________________________________ ", "______6666_66666__6666_6666________")
    print("|                                         |", "______66666_66666___66666666_______")
    print("|       Приветствую Вас в программе       |", "________6666__66666___66666666_____")
    print("|          'Крестики - нолики'            |", "_________66666__66666___66666_666__")
    print("|                                         |", "___________66666__66666___6666___66")
    print("| Программа написана в качестве выполнения|", "____________66666__66666____6666___")
    print("|          задания модуля B5.6            |", "______________66666_66666_6___66___")
    print("|        Участника группы FPW-131         |", "______________666666_66666_66__66__")
    print("|     Борового Константина Сергеевича     |", "______________6666666__666_666_____")
    print("|                                         |", "__________66666666666__666__666____")
    print("|       Формат ввода координат: х у       |", "_______666666666666666__666_666____")
    print("|           х - номмер строки             |", "______66666_______66666__66__666___")
    print("|           у - номер столбца             |", "_____66666_________66666__6__6666__")
    print("|  Как в морском бое, только поле 3х3 :-) |", "____66666__6________66666_6_66666__")
    print("|_________________________________________|", "____66666_66________66666___66666__")


def show():  # Создаём поле вывода на экран консоли, которое будет выводиться после ввода
    print()
    print("      0   1   2   ")
    print("    ------------- ")
    for i, row in enumerate(field): # функция хранения координат и распаковки их на переменные внутри функции, как сказали на вебинаре
        row_str = f"  {i} | {' | '.join(row)} | " # Форматирование через "|" и склейку этим же символом 
        print(row_str)
        print("    ------------- ")
    print()


def ask():  # Опрос координат пользователя и проверки ввода
    while True:
        cords = input("       Ваш ход: ").split() # разделение пробелом

        if len(cords) != 2: # проверка длинны координат
            print("Введите две координаты ")
            print("     через пробел!     ")
            continue

        x, y = cords # создание списка координат

        if not (x.isdigit()) or not (y.isdigit()): #  проверка, что координаты состоят из чисел
            print(" Введите числа через пробел! ")
            continue

        x, y = int(x), int(y) # преобразование к целочисленному типу данных

        if 0 > x or x > 2 or 0 > y or y > 2: # Проверка присутствия координат в допустимом диапазоне
            print(" Координаты вне диапазона! ")
            continue

        if field[x][y] != " ": # проверка - не занята ли клетка другим символом
            print(" Клетка занята! ")
            continue

    # continue каждый раз перезапускает цикл
        return x, y # в случае True возвращает координаты в переменные и останавливает цикл


def check_win(): # проверка выигрышных комбинаций
    for i in range(3): # строки для Х
        symbols = [] # временная переменная
        for j in range(3):
            symbols.append(field[i][j])
        if symbols == ["X", "X", "X"]:
            print("Выиграл крестик!")
            return True

    for i in range(3): # столбцы для Х
        symbols = []
        for j in range(3):
            symbols.append(field[j][i])
        if symbols == ["X", "X", "X"]:
            print("Выиграл крестик!")
            return True

    # Диагонали для Х
    
    symbols = []
    for i in range(3):
        symbols.append(field[i][i])
    if symbols == ["X", "X", "X"]:
        print("Выиграл крестик!")
        return True

    symbols = []
    for i in range(3):
        symbols.append(field[i][2 - i])
    if symbols == ["X", "X", "X"]:
        print("Выиграл крестик!")
        return True

    # Тоже самое для оси ординат
    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(field[i][j])
        if symbols == ["O", "O", "O"]:
            print("Выиграл нолик!")
            return True

    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(field[j][i])
        if symbols == ["O", "O", "O"]:
            print("Выиграл нолик!")
            return True

    symbols = []
    for i in range(3):
        symbols.append(field[i][i])
    if symbols == ["O", "O", "O"]:
        print("Выиграл нолик!")
        return True

    symbols = []
    for i in range(3):
        symbols.append(field[i][2 - i])
    if symbols == ["O", "O", "O"]:
        print("Выиграл нолик!")
        return True
    return False


greet() # запуск логики программы (бетонируем всё)
field = [[" "] * 3 for i in range(3)]  # создаём рабочую пустую зону игры через список списков
count = 0 # создаём счётчик ходов для проверки состояния "Ничья"
while True:
    count += 1 # и в данном случае увеличение счётчика должно происходить как определение номера хода, а не после выполнения
    show()
    if count % 2 == 1:
        print(" Ходит крестик ")
    else:
        print(" Ходит нолик ")

    x, y = ask()

    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "O"

    if check_win():
        print(show())
        break

    if count == 9:
        print(show())
        print("Ничья!")
        break
