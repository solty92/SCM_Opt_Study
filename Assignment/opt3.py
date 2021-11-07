import gurobipy as gp
from gurobipy import GRB, quicksum
import pandas as pd
from IPython.display import display

try:

    # Create a new model
    m = gp.Model("glasses")

    # Create variables: 일반변수
    COMP_ARR = {'wheel': 0, 'steel bar': 1, 'bumper': 2, 'chassis': 3, 'cabin': 4, 'door window': 5, 'windscreen': 6, 'blue container': 7, 'red tank': 8, 'blue motor': 9, 'red motor': 10, 'headlight': 11}
    PRICE_ARR = (0.3, 1, 0.2, 0.8, 2.75, 0.1, 0.29, 2.6, 3, 1.65, 1.65, 0.15)

    # Create variables: 의사결정변수

    # Add constraint: 재고수량 제약 (당월 재고수량 = 전월 or 기초 재고수량 + 당월 생산량 - 당월 수요량)

    # Add constraint: 작업시간 제약 (sum(제품 유형별 주별 생산량 * 제품 유형별 작업시간) <= 주당 최대 작업시간)

    # Set objective: 목적함수(Minimize 총비용 = 생산비용 + 재고비용)

    # Optimize model
    m.optimize()

    # 결정변수 값들 배열에 담기 (DataFrame)
    # 제품생산량
    # 재고수량

    # DataFrame 만들기(생산량)
    print('--------------------------------------------------------------------------')
    print('< Production for the planning period (batches of 1000 glasses) >')

    # DataFrame 만들기(재고수량)
    print('--------------------------------------------------------------------------')
    print('< Stock for the planning period (batches of 1000 glasses) >')

    print('--------------------------------------------------------------------------')

    # 결과(최적해)
    print('Objective Value : € %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
