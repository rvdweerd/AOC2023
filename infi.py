import math
with open('infi.txt', 'r') as file:
# Read the contents of the file
    indat = file.readlines()
data=[]
for line in indat:
    word = line.replace('\n','').replace('(','').replace(')','').split(', ')
    word = [int(i) for i in word]
    pairs = list(zip(*[iter(word)]*2))
    data.append(pairs)
    
sumofdistances = 0
for polygon in data:
    distances=[]
    for coord in polygon:
        distance = math.sqrt(coord[0]**2 + coord[1]**2)
        distances.append(distance)
    sumofdistances += max(distances)

print(sumofdistances)

import itertools

def combinantorial(lst):
    count = 0
    index = 1
    pairs = []
    for element1 in lst:
        for element2 in lst[index:]:
            pairs.append((element1, element2))
        index += 1

    return pairs

for polygon in data:
    global_distances=[]
    pair_distances=[]
    for pair in combinantorial(polygon):
        mid = ((pair[0][0]+pair[1][0]) / 2, (pair[0][1]+pair[1][1]) / 2)
        local_distances=[]
        for coord in polygon:
            distance = math.sqrt((coord[0]-mid[0])**2 + (coord[1]-mid[1])**2)
            local_distances.append(distance)
        pair_distances.append(max(local_distances)) 
    global_distances.append(min(pair_distances))    
#for polygon in data:
    print(min(global_distances))