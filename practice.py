# 부품별 인덱스
COMP_ARR = {'wheel': 0, 'steel bar': 1, 'bumper': 2, 'chassis': 3, 'cabin': 4, 'door window': 5, 'windscreen': 6, 'blue container': 7, 'red tank': 8, 'blue motor': 9, 'red motor': 10, 'headlight': 11}

# 부품별 가격
PRICE_ARR = (0.3, 1, 0.2, 0.8, 2.75, 0.1, 0.29, 2.6, 3, 1.65, 1.65, 0.15)

# 부품별 필요 갯수 (1대당)
COMP_COUNT_ARR = (4, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2)

# 제품별 필요 부품 인덱스값
PROD_BLUE = (0, 1, 2, 3, 4, 5, 6, 7, 9, 11)
PROD_RED = (0, 1, 2, 3, 4, 5, 6, 8, 10, 11)

print('*BLUE PROD COST(without assembling cost)*')
cost = 0
for i in PROD_BLUE:
    cost += PRICE_ARR[i] * COMP_COUNT_ARR[i]

BLUE_COMP_COST_TOTAL = cost * 3000
print('BLUE PROD COST : €', BLUE_COMP_COST_TOTAL)

print('*************************************************')

print('*RED PROD COST(without assembling cost)*')
cost = 0
for i in PROD_RED:
    cost += PRICE_ARR[i] * COMP_COUNT_ARR[i]

RED_COMP_COST_TOTAL = cost * 3000
print('RED PROD COST : €', RED_COMP_COST_TOTAL)