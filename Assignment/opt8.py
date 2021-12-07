import gurobipy as gp
from gurobipy import GRB, quicksum

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

    for i in range(CLIENT_CNT):
        PROFIT[i] = PRICE[i] - ( LOT_SIZE[i] * COST[i] )

    # Q1 ##############################################################################################################

    # Create variables: 의사결정변수
    client = m.addVars(CLIENT_CNT, vtype=GRB.BINARY, name='client')      # 어떤 고객의 밀을 운반해야 하는 지
    shipping = m.addVars(CLIENT_CNT, vtype=GRB.INTEGER, name='shipping')     # 고객 별 선적량 (lot)

    # Add constraint: 각 고객은 최대 선적량을 초과해 실을 수 없다
    m.addConstrs( ( shipping[i] * LOT_SIZE[i] <= MAX_CAPA for i in range(CLIENT_CNT) ), name="MAX_CAPA")

    # Add constraint: 한 고객만 싣는다
    m.addConstr( sum( client[i] for i in range(CLIENT_CNT) ) == 1, name="kipper")

    # Set objective: 목적함수
    obj = sum( shipping[i] * PROFIT[i] * client[i] for i in range(CLIENT_CNT) )

    m.setObjective(obj, GRB.MAXIMIZE)
    m.optimize()

    # 결과
    print('--------------------------------------------------------------------------')
    print('Objective Value : %f' % m.objVal)
    print('--------------------------------------------------------------------------')

    for v in m.getVars():
        print('%s : %g' % (v.varName, v.x))

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
