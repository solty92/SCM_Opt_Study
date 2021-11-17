import gurobipy as gp
from gurobipy import GRB, quicksum

try:

    # Create a new model
    m = gp.Model("wagon")

    # Create variables: 일반변수
    BOX_WEIGHT = (34, 6, 8, 17, 16, 5, 13, 21, 25, 31, 14, 13, 33, 9, 25, 25)       # 박스당 무게

    MAX_WAGON_CNT = 3       # 화물 기차 수
    MAX_CAPA = 100          # 화물 기차 당 최대 가용 중량
    WAGON_WEIGHT_AVG = 0    # 화물 기차 평균 중량 선언

    # Create variables: 의사결정변수
    wagon_load = m.addVars(MAX_WAGON_CNT, len(BOX_WEIGHT), vtype=GRB.BINARY, lb=0, ub=1, name='wagon_load')      # 각 화물이 어떤 박스를 실을지 말지 결정 (1: 싣는다, 0: No)


    # Add constraint: 각 화물 기차에 실은 무게 <= MAX_CAPA(100)
    m.addConstrs( quicksum( wagon_load[i, j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ) <= MAX_CAPA for i in range(MAX_WAGON_CNT) )

    # Add constraint: 각 박스는 1개씩만 존재 (중복해서 싣거나, 안 실을 수 없다)
    m.addConstrs( quicksum( wagon_load[i, j] for i in range(MAX_WAGON_CNT) ) == 1 for j in range(len(BOX_WEIGHT)) )


    # Set objective: 목적함수(Minimize 표준편차)
    WAGON_WEIGHT = [0 for i in range(MAX_WAGON_CNT)]        # 각 WAGON의 무게를 담는 리스트 선언

    # 각 WAGON의 무게를 배열에 담는다
    for i in range(len(WAGON_WEIGHT)):
        WAGON_WEIGHT[i] = quicksum( wagon_load[i, j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) )

    # WAGON 무게 평균
    WAGON_WEIGHT_AVG = sum(WAGON_WEIGHT) / len(WAGON_WEIGHT)

    # 편차를 구한다
    for i in range(len(WAGON_WEIGHT)):
        WAGON_WEIGHT[i] -= WAGON_WEIGHT_AVG

    # 편차의 제곱을 구한다
    for i in range(len(WAGON_WEIGHT)):
        WAGON_WEIGHT[i] **= 2

    # 분산을 구한다
    VARIANCE = sum(WAGON_WEIGHT) / MAX_WAGON_CNT

    # 표준편차를 구한다
    # STANDARD_DEVIATION = math.sqrt(VARIANCE)

    m.setObjective( VARIANCE, GRB.MINIMIZE )

    # Optimize model
    m.optimize()

    print('Result -------------------------------------------------------------------')

    # 결정변수 값들 배열에 담기
    tmpList = [[0 for i in range(16)] for j in range(3)]
    idx = 0
    for v in m.getVars():
        aa = int(idx / 16)
        # print('%s : %g' % (v.varName, v.x))
        tmpList[aa][idx % 16] = v.x
        idx += 1

    WAGON1 = []
    WAGON2 = []
    WAGON3 = []

    print('WAGON 1 --------------------')
    for i in range(len(BOX_WEIGHT)):
        if tmpList[0][i] == 1.0:
            WAGON1.append(i + 1)
    print('Box number :', WAGON1)
    print('Weight :', sum( tmpList[0][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ), 'quintals' )
    print()

    print('WAGON 2 --------------------')
    for i in range(len(BOX_WEIGHT)):
        if tmpList[1][i] == 1.0:
            WAGON2.append(i + 1)
    print('Box number :', WAGON2)
    print('Weight :', sum( tmpList[1][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ), 'quintals' )
    print()

    print('WAGON 3 --------------------')
    for i in range(len(BOX_WEIGHT)):
        if tmpList[2][i] == 1.0:
            WAGON3.append(i + 1)
    print('Box number :', WAGON3)
    print('Weight :', sum( tmpList[2][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ), 'quintals' )

    # 결과
    print('--------------------------------------------------------------------------')
    print('Objective Value : %f' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
