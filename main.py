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

def solve_day4():
    data = list(open("day4_input.txt","r"))
    count = 0
    cards = []
    draws = []
    wins = []
    for line in data:
        line = line.replace('\n','')
        card,mynums = line.split('|')
        mynums = [int(x) for x in mynums.split()]
        card = card.split(':')[1]
        card = set([int(num) for num in card.split()])
        cards.append(card)
        draws.append(mynums)
        #print(card)
        #print(mynums)
        n=0
        w=0
        for num in mynums:
            if num in card:
                w+=1
                if n==0: n=1
                else: n*=2
        count+=n
        wins.append(w)
    print(count)

    # Part2
    card_counter = [1]*len(cards)
    k=0
    for i in range(len(wins)):
        num_cards = card_counter[i]
        for j in range(wins[i]):
            if (i+j+1) < len(card_counter):
                card_counter[i+j+1] += num_cards
    print(sum(card_counter))
    k=0

def code_lookup(value, ranges):
    left, right = 0, len(ranges)

    while left != right - 1:
        mid = left + (right - left) // 2

        if value <= ranges[mid - 1][1]:  # Check left split max
            right = mid
        elif value >= ranges[mid][0]:    # Check right split min
            left = mid
        else:                            # We are in a gap
            return 0

    if ranges[left][0] <= value <= ranges[left][1]:
        # Return the code
        return ranges[left][2]
    else:
        return 0

def code_lookup2(value, ranges):
    for r in ranges:
        if value >= r[0] and value <= r[1]:
            return r[2]
    return 0

def disect_range(seedrange, maps):
    left_tracker=seedrange[0]
    right_tracker=seedrange[1]
    returnranges = []
    append = False
    assert(left_tracker <= right_tracker)
    mapmin=-999999999999999
    for map in maps:
        assert(map[0] <= map[1])
        assert(map[0] >= mapmin)
        mapmin = map[1]
        if right_tracker < map[0]: 
            #
            #      mmmmmmmmm
            #  ttt 
            returnranges.append((left_tracker,right_tracker))
            print("case 1")
            append=False
            break 
        if left_tracker < map[0] and right_tracker >= map[0] and right_tracker <= map[1]:
            #
            #     mmmmmmmmm
            #   tttttttt
            returnranges.append((left_tracker,map[0]-1))
            returnranges.append((map[0]+map[2],right_tracker+map[2]))
            #left_tracker = map[1]+1
            append=False
            print("case 2")
            break
        if left_tracker >= map[0] and right_tracker <= map[1]:
            #
            #     mmmmmmmmm
            #       ttttt
            returnranges.append((left_tracker+map[2],right_tracker+map[2]))
            #left_tracker = map[1]+1
            print("case 3")
            append=False
            break
        if left_tracker >= map[0] and left_tracker <= map[1] and right_tracker > map[1]:
            #
            #     mmmmmmmmm
            #           tttttt
            returnranges.append((left_tracker+map[2],map[1]+map[2]))
            left_tracker = map[1]+1
            print("case 4")
            append=True
            continue
        if left_tracker > map[1]:
            #
            #     mmmmmmmmm
            #                 ttttt
            append=True
            continue
        if left_tracker < map[0] and right_tracker > map[1]:
            #
            #     mmmmmmmmm
            #  ttttttttttttttttt
            returnranges.append((left_tracker,map[0]-1))
            returnranges.append((map[0]+map[2],map[1]+map[2]))
            left_tracker = map[1]+1
            append=True
            continue
    if returnranges == [] or append:
        print("case 5")
        returnranges.append((left_tracker,right_tracker))
    return returnranges

def solve_day5():
    data = list(open("day5_input.txt","r"))

    with open('/home/rvdw/AOC23/day5_input.txt', 'r') as file:
        # Read the contents of the file
        text = file.readlines()
    maps = [[] for i in range(7)]
    #seeds= []
    mapnumber=-1
    for line in text:
        if line.startswith("seeds:"):
            line=line.split(":")[1]
            line=line[1:-1]
            seeds=list(int(i) for i in (line.split(' ')))
            continue
        if line.startswith('\n'):
            if mapnumber >= 0:
                maps[mapnumber].sort(key=lambda tup:tup[1])
            mapnumber+=1
            continue
        if not line[0].isdigit():
            continue
        input = list(int(i) for i in line.split(' '))
        range_=(input[1], input[1]+input[2]-1, input[0]-input[1])
        maps[mapnumber].append(range_)
    maps[-1].sort(key=lambda tup:tup[1])
    # min_location = 9999999999999
    # for seed in seeds:
    #     for range_ in maps:
    #         print(seed,',',end="")
    #         cl1 = code_lookup(seed,range_)
    #         cl2 = code_lookup2(seed,range_)
    #         if cl1 != cl2:
    #             print("ERROR")
    #         seed = seed + cl2
    #     print("\n")
    #     if seed < min_location:
    #         min_location = seed
    # print(min_location)


    min_location = 9999999999999
    disected_input=list(zip(*[iter(seeds)]*2))
    disected_ranges=[]
    for i in disected_input:
        disected_ranges.append((i[0],i[0]+i[1]-1))
    for map in maps:
        disected_ranges_new=[]
        for p in disected_ranges:
            disected_ranges_new += disect_range(p,map)
        disected_ranges = disected_ranges_new    
    min_location = min(a[0] for a in disected_ranges)
    print(min_location)
    k=0

if __name__ == '__main__':
    solve_day5()