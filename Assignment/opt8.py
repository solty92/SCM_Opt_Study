import gurobipy as gp
from gurobipy import GRB, quicksum
# GRB = gp.GRB

try:

    # Create a new model
    m = gp.Model("Barge loading")

    # Create variables: 일반변수
    CLIENT_CNT = 7      # 고객 수
    AVAILABLE_QUANTITY  = (12, 31, 20, 25, 50, 40, 60)              # 가용 운반 개수
    LOT_SIZE            = (10, 8, 6, 9, 15, 10, 12)                 # lot 크기
    PRICE               = (1000, 600, 600, 800, 1200, 800, 1100)    # lot 당 가격
    COST                = (80, 70, 85, 80, 73, 70, 80)              # 운반 비용 (m^3 당)
    MAX_CAPA            = 1500                                      # 최대 선적량 (m^3)
    PROFIT              = [0 for i in range(CLIENT_CNT)]            # lot 당 이익

    # 고객별 운반하는 lot당 이익
    for i in range(CLIENT_CNT):
        PROFIT[i] = PRICE[i] - ( LOT_SIZE[i] * COST[i] )

    # Q1 ##############################################################################################################

    # Create variables: 의사결정변수
    shipping = m.addVars(CLIENT_CNT, vtype=GRB.CONTINUOUS, name='shipping')     # 고객 별 선적량 (lot)

    # Add constraint: 배의 최대선적량 제약
    m.addConstr((quicksum(shipping[i] * LOT_SIZE[i] for i in range(CLIENT_CNT)) <= MAX_CAPA), name="MAX_CAPA")

    # Set objective: 목적함수
    obj = sum( shipping[i] * PROFIT[i] for i in range(CLIENT_CNT))

    m.setObjective(obj, GRB.MAXIMIZE)
    m.optimize()

    # 결과
    print('--------------------------------------------------------------------------')
    print('Objective Value : %f' % m.objVal)
    print('--------------------------------------------------------------------------')

    # for v in m.getVars():
    #     print('%s : %g' % (v.varName, v.x))

    # Q1 답
    CLIENT_LIST1 = []
    SHIPPING_CNT1 = []
    for i in range(CLIENT_CNT):
        SHIPPING_CNT1.append(shipping[i].x)
        if shipping[i].x != 0:
            CLIENT_LIST1.append(i+1)

    OBJVAL_LIST = []
    OBJVAL_LIST.append(m.objVal)

    # Q2 ##############################################################################################################

    # Add constraint: 고객 밀의 가용량 제약
    m.addConstrs( ( shipping[i] <= AVAILABLE_QUANTITY[i] for i in range(CLIENT_CNT) ), name='available quantity' )

    m.optimize()

    # 결과
    print('--------------------------------------------------------------------------')
    print('Objective Value : %f' % m.objVal)
    print('--------------------------------------------------------------------------')

    # for v in m.getVars():
    #     print('%s : %g' % (v.varName, v.x))

    # Q2 답
    CLIENT_LIST2 = []
    SHIPPING_CNT2 = []
    for i in range(CLIENT_CNT):
        SHIPPING_CNT2.append(shipping[i].x)
        if shipping[i].x != 0:
            CLIENT_LIST2.append(i + 1)

    OBJVAL_LIST.append(m.objVal)


    # Q3 ##############################################################################################################

    # 의사결정변수의 타입을 INTEGER로 변경
    for i in range(CLIENT_CNT):
        shipping[i].vtype=GRB.INTEGER

    m.optimize()

    # 결과
    print('--------------------------------------------------------------------------')
    print('Objective Value : %f' % m.objVal)
    print('--------------------------------------------------------------------------')

    # for v in m.getVars():
    #     print('%s : %g' % (v.varName, v.x))

    # Q3 답
    CLIENT_LIST3 = []
    SHIPPING_CNT3 = []
    for i in range(CLIENT_CNT):
        SHIPPING_CNT3.append(shipping[i].x)
        if shipping[i].x != 0:
            CLIENT_LIST3.append(i + 1)

    OBJVAL_LIST.append(m.objVal)

    print('--------------------------------------------------------------------------')
    print('Q1 Client list         : ', CLIENT_LIST1)
    print('Q1 Shipping Count list : ', SHIPPING_CNT1)
    print('Q1 objective value     : ', OBJVAL_LIST[0])
    print('--------------------------------------------------------------------------')

    print('Q2 Client list         : ', CLIENT_LIST2)
    print('Q2 Shipping Count list : ', SHIPPING_CNT2)
    print('Q2 objective value     : ', OBJVAL_LIST[1])
    print('--------------------------------------------------------------------------')

    print('Q3 Client list         : ', CLIENT_LIST3)
    print('Q3 Shipping Count list : ', SHIPPING_CNT3)
    print('Q3 objective value     : ', OBJVAL_LIST[2])
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
