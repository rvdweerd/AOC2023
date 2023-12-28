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


def step(currnodes,graph,instruction):
    i = 0 if instruction == 'L' else 1
    finished = True
    nextnodes = []
    for node in currnodes:
        nextnodes.append(graph[node][i])
        if nextnodes[-1][-1] != 'Z':
            finished = False
    return nextnodes, finished

import math
def solve_day8():
    with open('/home/rvdw/AOC23/day8_input.txt', 'r') as file:
    # Read the contents of the file
        text = file.readlines()
    instructions = text[0].replace('\n','')
    startnode = 'AAA'#text[2][:3]
    endnode = 'ZZZ'
    graph={}
    for line in text[2:]:
        line=line.replace('\n','').split(' ')
        graph[line[0]] = [line[2][1:4],line[3][:3]]
    currnode = startnode
    count=0
    while True:
        if currnode == endnode:
            break
        for ch in instructions:
            if ch == 'L':
                currnode = graph[currnode][0]
            if ch == 'R':
                currnode = graph[currnode][1]
            count+=1
    print(count)

    startnodes = []
    for k,v in graph.items():
        if k[-1] == 'A':
            startnodes.append(k)
    countsall = []
    res=1
    finished = False
    for currnode in startnodes:
        countall=[]
        count=0
        i=0
        while len(countall)<1:
            ch = instructions[i%len(instructions)]
            if ch == 'L':
                currnode = graph[currnode][0]
            elif ch == 'R':
                currnode = graph[currnode][1]
            count+=1
            i+=1
            if currnode[-1] == 'Z':
                countall.append(count)
                #count=0
        countsall.append(countall[0])
        res*=countall[0]
    print(math.lcm(*countsall))


import numpy as np

class Day13:
    def __init__(self):
        self.hor_seqs=[]
        self.hor_strs=[]
        self.ver_seqs=[]
        self.ver_strs=[]
        self.get_data()

    def get_data(self):
        with open('day13_input.txt', 'r') as file:
        # Read the contents of the file
            data = file.readlines()

        line_ints=[]
        line_strs=[]
        line_bins=[]
        vert_str2=[]
        for line in data:
            if line.strip() == "":
                self.hor_seqs.append(line_ints)
                matrix=np.array(line_bins)
                matrix=matrix.transpose()
                line_bins=[]
                vert_str2=[]
                for row in matrix:
                    strrow = ""
                    for num in row:
                        strrow += str(int(num))
                    line_bins.append(int(strrow,2))
                    vert_str2.append(strrow)
                self.ver_seqs.append(line_bins)
                self.ver_strs.append(vert_str2)
                line_bins=[]
                line_ints=[]
            else:
                str_=line.strip().replace('#','1').replace('.','0')
                line_ints.append(int(str_,2))
                line_strs.append(str_)
                line_bins.append([int(i) for i in str_])

        self.hor_seqs.append(line_ints)
        self.hor_strs.append(line_strs)
        
        matrix=np.array(line_bins)
        matrix=matrix.transpose()
        vert_binstring=[]
        vert_str2=[]
        for row in matrix:
            strrow = ""
            for num in row:
                strrow += str(int(num))
            vert_binstring.append(int(strrow,2))
            vert_str2.append(strrow)
        self.ver_seqs.append(vert_binstring)
        self.ver_strs.append(vert_str2)

    def find_ranges(self, seq):
        l=0
        r=0
        gap=1
        patterns=[]
        while r+1<len(seq):
            r+=1
            if seq[r]==seq[r-gap]:
                l=r-gap
                gap+=2
                if l<=0:
                    patterns.append([l,r])
                    l=(r+l)//2+1#l=r-1 #-1?
                    r=l
                    gap=1
            else:
                if gap>1:
                    patterns.append([l,r-1])
                    l=(r+l)//2+1
                    r=l
                if r>0 and seq[r]==seq[r-1]:
                    l=r-1
                    gap=3
                else:
                    gap=1
        if gap>1:
            patterns.append([l,r])

        return patterns
    def get_score(self, seq):
        patterns=self.find_ranges(seq)
        validpatterns = []
        ans=[]
        maxpat=None
        maxans=0
        for pat in patterns:
            if pat[0]==0 or pat[-1]==len(seq)-1:
                a = (pat[1]-pat[0]+1)//2 + pat[0]
                ans.append(a)
                validpatterns.append(pat)
                if a > maxans:
                    maxans=a
                    maxpat=pat
        if len(ans)==0:
            ans=[0]
        return ans, validpatterns, maxpat

    def num_diff_bits(self, A,  B):
    
        count = 0
    
        # since, the numbers are less than 2^31
        # run the loop from '0' to '31' only
        for i in range(0,64):
    
            # right shift both the numbers by 'i' and
            # check if the bit at the 0th position is different
            if ((( A >>  i) & 1) != (( B >>  i) & 1)): 
                count=count+1
        return count
    
    def solve(self):
        count=0
        count2=0
        for i in range(len(self.ver_seqs)):
            vert_seq=self.ver_seqs[i]
            hori_seq=self.hor_seqs[i]
            vscores, vranges, vmaxrange = self.get_score(vert_seq)
            hscores, hranges, hmaxrange = self.get_score(hori_seq)
            if len(vscores)>0:
                count += max(vscores)
            if len(hscores)>0:
                count += max(hscores) * 100
            
            compset = [ [max(hscores), hori_seq, hmaxrange, 100], [max(vscores), vert_seq, vmaxrange, 1] ]

            brk=False
            for compscore, compseq, comprange, mp in compset:
                maxcount=0
                loccount = 0
                if brk: break
                for i in range(len(compseq)):
                    if brk: break
                    for j in range(len(compseq)):
                        if brk: break
                        if j<=i:
                            continue
                        if self.num_diff_bits(compseq[i],compseq[j]) == 1:
                            l=compseq.copy()[i]
                            r=compseq.copy()[j]
                            compseq[j] = l
                            cs,cr,cm = self.get_score(compseq)
                            for k in range(len(cr)):
                                if brk: break
                                if cr[k] != comprange and cs[k] > 0:# cs != compscore and cs > 0 and 
                                    # if len(cr)>1:
                                    #     k=0
                                    compseq[j] = r
                                    loccount = cs[k] * mp
                                    if loccount > maxcount:
                                        maxcount = loccount
                                    brk = True
                                    break
                            compseq[i] = r
                            compseq[j] = r
                            cs,cr,cm = self.get_score(compseq)
                            for k in range(len(cr)):
                                if brk: break
                                if cr[k] != comprange and cs[k] > 0:#cs != compscore and cs > 0 and 
                                    # if len(cr)>1:
                                    #     k=0
                                    compseq[i] = l
                                    loccount = cs[k] * mp
                                    if loccount > maxcount:
                                        maxcount = loccount
                                    brk = True
                                    break                        
                            compseq[i] = l
                count2 += maxcount
        print(count)
        print(count2)


class Pawn:
    def __init__(self, data):
        self.grid=data
        self.pos = (0,0)
        self.width = len(data[0])
        self.height = len(data)
        self.tail = ""
        self.moves = ['N','E','S','W']
        self.directions = {
            'S':(1,0),
            'N':(-1,0),
            'E':(0,1),
            'W':(0,-1)
        }
        self.opposite = {
            'S':'N',
            'N':'S',
            'E':'W',
            'W':'E'
        }

    def in_bounds(self, coord):
        return coord[0] >= 0 and coord[0] < self.height and coord[1] >= 0 and coord[1] < self.width

    def add_coords(self, coord1, coord2):
        return (coord1[0]+coord2[0], coord1[1]+coord2[1])

    def get_reachable_coords(self):
        coords=[]
        possible_moves=[]
        costs=[]
        for move in self.moves:
            if move not in self.tail:
                if len(self.tail)>0:
                    if self.tail[-1] == self.opposite[move]:
                        continue
                new_coord = self.add_coords(self.pos, self.directions[move])
                if self.in_bounds(new_coord):
                    coords.append(new_coord)
                    possible_moves.append(move)
                    costs.append(int(self.grid[new_coord[0]][new_coord[1]]))
            elif len(self.tail) < 3:
                new_coord = self.add_coords(self.pos, self.directions[move])
                if self.in_bounds(new_coord):
                    coords.append(new_coord)
                    possible_moves.append(move)
                    costs.append(int(self.grid[new_coord[0]][new_coord[1]]))
        return coords, possible_moves, costs
    
    def get_reachable_coords_alt(self):
        coords=[]
        possible_moves=[]
        costs=[]
        for move in self.moves:
            if move not in self.tail:
                if len(self.tail)>0:
                    if self.tail[-1] == self.opposite[move]:
                        continue
                    if len(self.tail)<4:
                        continue
                new_coord = self.add_coords(self.pos, self.directions[move])
                if self.in_bounds(new_coord):
                    coords.append(new_coord)
                    possible_moves.append(move)
                    costs.append(int(self.grid[new_coord[0]][new_coord[1]]))
            elif len(self.tail) < 10:
                new_coord = self.add_coords(self.pos, self.directions[move])
                if self.in_bounds(new_coord):
                    coords.append(new_coord)
                    possible_moves.append(move)
                    costs.append(int(self.grid[new_coord[0]][new_coord[1]]))
        return coords, possible_moves, costs

    def step(self, move):
        if move not in self.tail:
            new_coord = self.add_coords(self.pos, self.directions[move])
            if self.in_bounds(new_coord):
                self.tail = move
                self.pos = new_coord
        elif len(self.tail) < 3:
            new_coord = self.add_coords(self.pos, self.directions[move])
            if self.in_bounds(new_coord):
                self.tail += move
                self.pos = new_coord

    def virtual_step(self, move):
        if move not in self.tail:
            new_coord = self.add_coords(self.pos, self.directions[move])
            if self.in_bounds(new_coord):
                return move
        elif len(self.tail) < 3:
            new_coord = self.add_coords(self.pos, self.directions[move])
            if self.in_bounds(new_coord):
                return self.tail + move

    def virtual_step_alt(self, move):
        if move not in self.tail:
            new_coord = self.add_coords(self.pos, self.directions[move])
            if self.in_bounds(new_coord):
                return move
        elif len(self.tail) < 10:
            new_coord = self.add_coords(self.pos, self.directions[move])
            if self.in_bounds(new_coord):
                return self.tail + move

from queue import PriorityQueue
class qItem:
    def __init__(self, tail, cost, coord, path):
        self.tail = tail
        self.cost = cost
        self.coord = coord
        self.path = path

    def __lt__(self, other):
        return len(self.tail) < len(other.tail)

class Day17:
    def __init__(self):
        self.pawn = None
        self.get_data()

    def get_data(self):
        with open('day17_input.txt', 'r') as file:
            data = file.readlines()
            grid = []
            for d in data:
                grid.append(d.replace('\n',''))
        self.pawn = Pawn(grid)

    def solve_part1(self):
        # PART 1
        # We use Dijkstra's shortes path algorithm
        visited = {}
        pqueue = PriorityQueue()
        cost_all_routes=[]
        all_routes=[]
        pqueue.put((0, qItem("", 0, (0,0), "")))

        while not pqueue.empty():
            queuetop = pqueue.get()
            acc_cost = queuetop[0]
            path = queuetop[1].path
            self.pawn.tail = queuetop[1].tail
            self.pawn.pos = queuetop[1].coord
            newcoords, moves, cost = self.pawn.get_reachable_coords()
            for i, coord in enumerate(newcoords):
                new_tail = self.pawn.virtual_step(moves[i])
                new_cost = acc_cost+cost[i]
                mapkey = (coord[0],coord[1],len(new_tail),new_tail[-1])
                if mapkey not in visited:
                    pqueue.put( (new_cost, qItem(new_tail, new_cost, coord, path+moves[i])) )
                    visited[mapkey] = new_cost
                elif acc_cost+cost[i] < visited[mapkey]:
                    pqueue.put( (new_cost, qItem(new_tail, new_cost, coord, path+moves[i] )) )
                    visited[mapkey] = new_cost

                # Check terminal condition
                if coord == (self.pawn.height-1,self.pawn.width-1):
                    cost_all_routes.append(acc_cost+cost[i])
                    all_routes.append(path+moves[i])
                    print('total cost',cost_all_routes[-1], 'route length',len(all_routes[-1]), all_routes[-1], flush=True)
                    return

    def solve_part2(self):
        # PART 2
        # We use Dijkstra's shortes path algorithm
        visited = {}
        pqueue = PriorityQueue()
        cost_all_routes=[]
        all_routes=[]
        pqueue.put((0, qItem("", 0, (0,0), "")))

        while not pqueue.empty():
            queuetop = pqueue.get()
            acc_cost = queuetop[0]
            path = queuetop[1].path
            self.pawn.tail = queuetop[1].tail
            self.pawn.pos = queuetop[1].coord
            newcoords, moves, cost = self.pawn.get_reachable_coords_alt()
            for i, coord in enumerate(newcoords):
                new_tail = self.pawn.virtual_step_alt(moves[i])
                new_cost = acc_cost+cost[i]
                mapkey = (coord[0],coord[1],len(new_tail),new_tail[-1])
                if mapkey not in visited:
                    pqueue.put( (new_cost, qItem(new_tail, new_cost, coord, path+moves[i])) )
                    visited[mapkey] = new_cost
                elif acc_cost+cost[i] < visited[mapkey]:
                    pqueue.put( (new_cost, qItem(new_tail, new_cost, coord, path+moves[i] )) )
                    visited[mapkey] = new_cost

                # Check terminal condition
                if coord == (self.pawn.height-1,self.pawn.width-1) and len(new_tail) >= 4:
                    cost_all_routes.append(acc_cost+cost[i])
                    all_routes.append(path+moves[i])
                    print('total cost',cost_all_routes[-1], 'route length',len(all_routes[-1]), all_routes[-1], flush=True)
                    return
class Day23b:
    def __init__(self):
        self.get_data()
        self.path_lengths=[]
        self.max_path_length=0
        self.timer = time.time()
        self.counter=0
    def get_data(self):
        self.grid = open("day23_input.txt").read().splitlines()
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.startnode = (1,0)
        self.endnode = (self.width-2, self.height-1)
        self.g = {} # graph with nodes (intersections in the grid)
        self.lastnode = (-1,-1)
        self.visited = set()
        self.previous_paths_to_node_map = {}
        self.oneway = False
    def GetNeighbors(self,x,y, enable_oneway=True):
        numfree=0
        neighbors=[]
        if x>0: # check left
            if self.grid[y][x-1] != '#':
                numfree+=1
                if not enable_oneway or self.grid[y][x-1] != '>':
                    neighbors.append((x-1,y))
        if x<self.width-1: # check right
            if self.grid[y][x+1] != '#':
                numfree+=1
                if not enable_oneway or self.grid[y][x+1] != '<':
                    neighbors.append((x+1,y))
        if y>0: # check up
            if self.grid[y-1][x] != '#':
                numfree+=1
                if not enable_oneway or self.grid[y-1][x] != 'v':
                    neighbors.append((x,y-1))
        if y<self.height-1: # check down
            if self.grid[y+1][x] != '#':
                numfree+=1
                if not enable_oneway or self.grid[y+1][x] != '^':
                    neighbors.append((x,y+1))

        return neighbors, numfree
    def CreateGraph_(self,x,y,n, enable_oneway=True):
        if (x,y) == self.startnode:
            self.g[(x,y)]=[]
            self.lastnode = (x,y)
            self.visited.add((x,y))
        if enable_oneway and self.grid[y][x] in ['<','>','^','v']:
            self.oneway=True
            if self.grid[y][x] == '<' and x>0:
                neighbors = [(x-1,y)]
            elif self.grid[y][x] == '>' and x<self.width-1:
                neighbors = [(x+1,y)]
            elif self.grid[y][x] == '^' and y>0:
                neighbors = [(x,y-1)]
            elif y<self.height-1:
                neighbors = [(x,y+1)]
            numfree=1
        else:
            neighbors, numfree = self.GetNeighbors(x,y, enable_oneway)
        if numfree > 2 or (x,y) == self.endnode: # We are at an (end)node
            if (x,y)==self.endnode:
                k=0

            if (x,y) not in self.previous_paths_to_node_map: # we haven't encountered this node yet
                self.previous_paths_to_node_map[(x, y)]=set()
            self.previous_paths_to_node_map[(x, y)] = self.previous_paths_to_node_map[(x, y)].union(self.visited) # add current path to all previous paths that led to current node
            if (x,y) not in self.g:
                self.g[(x,y)]=[]
            if [self.lastnode,n] not in self.g[(x,y)] and not self.oneway:
                self.g[(x,y)].append([self.lastnode,n])
                self.g[(x,y)].sort(key = lambda a: -a[1])
            if [(x,y),n] not in self.g[self.lastnode]:
                self.g[self.lastnode].append([(x,y),n])
                self.g[(x,y)].sort(key = lambda a: -a[1])
            self.lastnode = (x,y)
            n=0
            self.oneway=False
        for neighbor in neighbors:
            if (x,y) in self.previous_paths_to_node_map:
                if neighbor in self.previous_paths_to_node_map[(x, y)]:
                    continue
            if neighbor not in self.visited:
                self.visited.add((neighbor[0],neighbor[1]))
                temp=self.lastnode
                self.CreateGraph_(neighbor[0],neighbor[1],n+1,enable_oneway)
                self.lastnode=temp
                self.visited.remove((neighbor[0],neighbor[1]))
        return

    def FindPathsToExit_(self,coord,n):
        if coord == self.endnode:
            self.path_lengths.append(n)
            self.counter+=1
            if n>self.max_path_length:
                self.max_path_length=n
                self.max_path=self.path
                print('  [Timer %.2f s] [Routecount %d] New max path length: ' %(self.Timer(), self.counter),self.max_path_length,'Nodes visited:',len(self.max_path),self.max_path,flush=True)
        else:
            for nc,d in self.g[coord]:
                if nc not in self.visited:
                    self.visited.add(nc)
                    self.path.append(nc)
                    self.FindPathsToExit_(nc,n+d)
                    self.visited.remove(nc)
                    self.path=self.path[:-1]
            if len(self.path_lengths) > 0:
                pass
    def CreateGraph(self,x,y,n,enable_oneway=True):
        self.g={}
        self.visited=set()
        self.path=[self.startnode]
        self.max_path=[]
        self.lastnode = (-1,-1)
        self.previous_paths_to_node_map = {}
        self.oneway = False
        self.CreateGraph_(x,y,n,enable_oneway)
    def FindPathsToExit(self,coord,n):
        self.visited=set()
        self.path=[self.startnode]
        self.max_path=[]
        self.path_lengths=[]
        self.max_path_length=0
        self.counter = 0
        self.FindPathsToExit_(coord,n)

    def Mark(self):
        t = time.time()
        elapsed = t - self.timer
        self.timer = t
        return max(0.,elapsed)

    def Timer(self):
        return max(0., time.time() - self.timer)
    def Solve_(self, enable_oneway=True):
        self.CreateGraph(1,0,0, enable_oneway)
        print("Graph created in %.1f s, num_nodes=" %self.Mark(),len(self.g.keys()),'num_edges=',sum([len(i) for i in self.g.values()]))
        self.FindPathsToExit(self.startnode,0)
        print('MAX PATH LENGTH:',self.max_path_length,'Total routecount:',self.counter)

    def Solve(self):
        print('.'*3)
        print('#'*40+'\n### PART 1 - one-way enabled\n'+'#'*40)
        self.Solve_(enable_oneway=True)
        print('\n'+'#'*40+'\n### PART 2 - one-way disabled\n'+'#'*40)
        self.Solve_(enable_oneway=False)

class Day12:
    def __init__(self):
        self.rawinput = open("day12_input.txt").read().splitlines()
        self.input=[]
        for e in self.rawinput:
            line_orig, broken = e.split(' ')
            chunks_orig=list(map(int,broken.split(',')))
            self.input.append((line_orig,chunks_orig))
        self.count=0
        self.cache = {}
    def Scan(self,i,j,filled, segment):
        key = (i,j,segment)
        if key in self.cache:
            return self.cache[key]

        if len(segment) > self.chunks[j]: return 0# [ ..### 2 ]
        if len(segment) == self.chunks[j]:
            j+=1
            if i<=len(self.line)-1:
                if (self.line[i]) == '#':
                    return 0
                else:
                    filled+='.'
                    i+=1
        if i==len(self.line):
            if j==len(self.chunks):
                self.count+=1
                return 1
            return 0
        if j==len(self.chunks):
            if '#' not in self.line[i:]:
                self.count+=1
                return 1
            return 0

        total = 0
        if i+self.chunks[j] > len(self.line): return total
        if self.line[i] == '.':
            total += self.Scan(i+1,j,filled+'.',"")
        else:
            if self.line[i] == '?':
                total += self.Scan(i+1,j,filled+'.',"")
            if '.' in self.line[i:i+self.chunks[j]]: return total
            else:
                total += self.Scan(i+self.chunks[j],j,filled+'#'*self.chunks[j],'#'*self.chunks[j])
        self.cache[key]=total
        return total
    def SolvePart1(self):
        total=0
        for self.line, self.chunks in self.input:
            ans = self.Scan(0,0, "", "")
            total+=ans
            self.cache={}
        print("Part 1. total count:",total)
    def SolvePart2(self):
        total=0
        for self.line, self.chunks in self.input:
            self.line = (self.line+'?')*4 + self.line
            self.chunks = self.chunks * 5
            ans = self.Scan(0,0, "", "")
            total+=ans
            self.cache={}
        print("Part 2. total count:",total)

    def Solve(self):
        self.SolvePart1()
        self.SolvePart2()

class Day6:
    def __init__(self):
        self.data = open("day6_input.txt").read().splitlines()

    def Iterate(self, time, distance):
        count=0
        for i in range(time):
            d = (time-i)*i
            #print(d)
            if d>distance: count+=1
        #print("---------")
        return count;
    def SolveUsingIteration(self, inputvec):
        total=1
        for (t,d) in inputvec:
            total*=self.Iterate(t,d)
        print('Part 1. Total score:',total,'\n')
    def SolveUsingMath(self, t, d):
        x1 = (t/2 - 1/2*math.sqrt(t**2-4*d))
        print('x1: ',x1)
        x2 = (t/2 + 1/2*math.sqrt(t**2-4*d))
        print('x2: ',x2)

        m = t/2
        print('m: ',int(m))

        nsol = 1 + (m-math.floor(x1)-1)*2
        print('Part 2. Total score: ',int(nsol))

    def Solve(self):
        self.SolveUsingIteration([(54,302),(94,1476),(65,1029),(92,1404)])
        self.SolveUsingMath(54946592, 302147610291404)

import time
if __name__ == '__main__':
    #import sys
    #print(sys.getrecursionlimit())
    #sys.setrecursionlimit(15000)

    Day6().Solve()
