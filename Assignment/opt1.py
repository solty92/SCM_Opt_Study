import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from IPython.display import display


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
    norm_prod = m.addVars(len(MONTH), vtype=GRB.INTEGER, lb=0, name='norm_prod')  # 월별 기본생산량

    over_prod = m.addVars(len(MONTH), vtype=GRB.INTEGER, lb=0, name='over_prod')  # 월별 초과생산량

    stock = m.addVars(len(MONTH), vtype=GRB.INTEGER, lb=0, name='stock')  # 월별 재고량

    # Add constraint: 당월재고량 = 전월재고량 + 당월기본생산량 + 당월초과생산량 - 당월수요량
    m.addConstr(stock[0] == INIT_STOCK + norm_prod[0] + over_prod[0] - SALE_ARR[0], name='ca')  # 1월 재고량
    m.addConstrs((stock[i] == stock[i - 1] + norm_prod[i] + over_prod[i] - SALE_ARR[i] for i in range(1, len(MONTH))),
                 name="cb")  # 2~12월 재고량

    # Add constraint: 생산량 제약조건
    m.addConstrs((norm_prod[i] <= NORM_PROD_CAPA for i in range(len(MONTH))), name='cc')  # 월 기본생산량 범위

    m.addConstrs((over_prod[i] <= NORM_PROD_CAPA * OVER_PROD_RATE for i in range(len(MONTH))), name='cd')  # 월 초과생산량 범위

    # Set objective: 목적함수(Minimize 총비용 = 기본생산비용 + 초과생산비용 + 재고비용)
    m.setObjective(
        NORM_COST * (func_sum(norm_prod)) + OVER_COST * (func_sum(over_prod)) + STOCK_COST * (func_sum(stock)),
        GRB.MINIMIZE)

    # Optimize model
    m.optimize()

    # 결정변수 값들 배열에 담기 (DataFrame 용도)
    norm_prod_arr = []
    for v in norm_prod.values():
        norm_prod_arr.append(int(v.X))

    over_prod_arr = []
    for v in over_prod.values():
        over_prod_arr.append(int(v.X))

    stock_arr = []
    for v in stock.values():
        stock_arr.append(int(v.X))

    # DataFrame 만들기
    print('--------------------------------------------------------------------------')
    df = pd.DataFrame({'norm_prod': norm_prod_arr,
                       'over_prod': over_prod_arr,
                       'stock': stock_arr})
    df.index = MONTH
    display(df)
    print('--------------------------------------------------------------------------')

    # 결과
    print('Objective Value : %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
