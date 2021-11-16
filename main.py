BOX_WEIGHT = [34, 6, 8, 17, 16, 5, 13, 21, 25, 31, 14, 13, 33, 9, 25, 25]

wagon_load = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    , [1, 1, 1, 1]
    , [1, 1, 1, 1]
]

print(sum( wagon_load[0][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ) )

print(wagon_load[0][0])
print(wagon_load[0][1])
print(wagon_load[0][2])
print(wagon_load[0][3])
print(wagon_load[0][4])
print(wagon_load[0][5])
print(wagon_load[0][6])
print(wagon_load[0][7])
print(wagon_load[0][8])