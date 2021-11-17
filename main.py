BOX_WEIGHT = [34, 6, 8, 17, 16, 5, 13, 21, 25, 31, 14, 13, 33, 9, 25, 25]

wagon_load = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    , [1, 1, 1, 1]
    , [1, 1, 1, 1]
]

print(sum( wagon_load[0][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ) )

print(wagon_load)