list1 = [[' ',' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ',' '],
         [' ',' ','x',' ',' ',' '],
         [' ','x','x','x',' ',' '],
         ['x',' ','x','x','x',' '],
         ['x',' ','x','x',' ',' '],
         ['x','x','x','x','x',' '],
         ['x','x','x','x','x',' '],
         ['x','x','x','x','x',' '],
         ['x','x','x','x','x',' ']]

aggHeight = []
for i in range(0, 6):
    ctr = 0
    for j in range(len(list1)):
        if list1[j][i] == 'x':
            aggHeight.append(len(list1) - j)
            break
        if j == len(list1) - 1:
            aggHeight.append(0)

print 'Agg Height', aggHeight

bumpness = 0

for i in range(len(aggHeight)):
    if i < len(aggHeight)-1:
        bumpness += abs(aggHeight[i] - aggHeight[i+1])
print 'Bumpness', bumpness

holes = 0

for i in range(0, 6):
    for j in range(len(list1) - aggHeight[i], len(list1)):
        if list1[j][i] == ' ':
            holes += 1

print 'Holes', holes

completeLines = 0

for i in range(len(list1)):
    if list1[i].count(list1[i][0]) == len(list1[i]) and list1[i][0] == 'x':
        completeLines += 1
 
print 'completeLines', completeLines

altitude = max(aggHeight) - min(aggHeight)
print 'altitude', altitude




