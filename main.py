def get_data():
    # Open the file
    with open('/home/rvdw/AOC23/day2_input.txt', 'r') as file:
        # Read the contents of the file
        text = file.read()

    # Define the delimiters
    data_ = []
    # Split the text into tokens using the delimiters
    lines = text.split('\n')
    for line in lines:
        tokens = line.split(':')
        game_id = tokens[0].split(' ')[1]
        print("game: " + game_id)
        draws_ = tokens[1].split(';')
        d = []
        for draw_ in draws_:
            print("  draw: ")
            balls_ = draw_.split(',')
            print("      balls", balls_)
            b = [0, 0, 0]
            for ball_ in balls_:
                count_ = ball_.split(' ')
                if count_[2] == 'red':
                    b[0] = int(count_[1])
                if count_[2] == 'green':
                    b[1] = int(count_[1])
                if count_[2] == 'blue':
                    b[2] = int(count_[1])
            d.append(b)
        data_.append(d)
    return data_


def solve_day1():
    data = get_data()
    max_red = 12
    max_green = 13
    max_blue = 14
    total_power = 0
    count = 0
    for i, draws in enumerate(data):
        valid = True
        min_red = 0
        min_green = 0
        min_blue = 0

        for balls in draws:
            if balls[0] > max_red or balls[1] > max_green or balls[2] > max_blue:
                valid = False
            if balls[0] > min_red:
                min_red = balls[0]
            if balls[1] > min_green:
                min_green = balls[1]
            if balls[2] > min_blue:
                min_blue = balls[2]

        if valid:
            count += i + 1
        power = min_red * min_green * min_blue
        print("Game:", i, "Draw:", draws, "VALID" if valid else "INVALID", ", POWER:", power)
        total_power += power
    print("Total valid points:", count, "Total power:", total_power)

from collections import defaultdict
from math import prod
from re import finditer
def solve_day3():
    parts = defaultdict(list)
    board = list(open('day3_input.txt'))
    chars = {(r, c) for r in range(140)
             for c in range(140)
             if board[r][c] not in '01234566789.'}

    for r, row in enumerate(board):
        for m in finditer(r'\d+', row):
            nexts = {(r+s, c+d) for s in (-1, 0, 1)
                     for d in (-1, 0, 1)
                     for c in range(*m.span())}
            for c in nexts & chars:
                parts[c].append(int(m[0]))

    print(sum(sum(p)  for p in parts.values()),
          sum(prod(p) for p in parts.values() if len(p)==2))

if __name__ == '__main__':
    solve_day3()