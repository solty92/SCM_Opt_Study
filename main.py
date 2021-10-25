import gurobipy as gp
from gurobipy import GRB


# 변수들의 값을 더해주는 함수
def func_sum(a):
    sum_a = 0
    for i in range(12):
        sum_a += a[i]
    return sum_a


try:

    # Create a new model
    m = gp.Model("bicycle")

    # Create variables: 일반변수
    MONTH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # 1~12월 배열
    SALE_ARR = [30000, 15000, 15000, 25000, 33000, 40000, 45000, 45000, 26000, 14000, 25000, 30000]  # 월별 수요예측량

    NORM_COST = 32  # 기본생산비용
    OVER_COST = 40  # 초과생산비용
    STOCK_COST = 5  # 재고비용
    NORM_PROD_CAPA = 30000  # 최대 기본생산량
    OVER_PROD_RATE = 0.5  # 기본생산량 대비 가능한 초과근무생산량 비율
    INIT_STOCK = 2000  # 기초재고

    # Create variables: 의사결정변수
    x = m.addVars(12, vtype=GRB.INTEGER, lb=0, name='x')  # 월별 기본생산량

    y = m.addVars(12, vtype=GRB.INTEGER, lb=0, name='y')  # 월별 초과생산량

    s = m.addVars(12, vtype=GRB.INTEGER, lb=0, name='s')  # 월별 재고량

    saleArr = [30000, 15000, 15000, 25000, 33000, 40000, 45000, 45000, 26000, 14000, 25000, 30000]

    # Add constraint: 당월재고량 = 전월재고량 + 당월기본생산량 + 당월초과생산량 - 당월수요량
    m.addConstr(s[0] == 2000 + x[0] + y[0] - saleArr[0], name='ca')  # 1월 재고량

    m.addConstrs((s[i] == s[i - 1] + x[i] + y[i] - saleArr[i] for i in range(1, 12)), name="cb")  # 2~12월 재고량

    # Add constraint: 생산량 제약조건
    m.addConstrs((x[i] <= 30000 for i in range(12)), name='cc')  # 월 기본생산량 범위

    m.addConstrs((y[i] <= 15000 for i in range(12)), name='cd')  # 월 초과생산량 범위

    # Set objective: 목적함수(Minimize Z = x + y + s)
    m.setObjective(32 * (func_sum(x)) + 40 * (func_sum(y)) + 5 * (func_sum(s)), GRB.MINIMIZE)

    # Optimize model
    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: €%i' % m.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
