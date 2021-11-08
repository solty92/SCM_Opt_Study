import gurobipy as gp
from gurobipy import GRB, quicksum
import pandas as pd
from IPython.display import display

try:

    # Create a new model
    m = gp.Model("truck")

    # Create variables: 일반변수
    # 부품별 인덱스
    COMP_ARR = {'wheel': 0
              , 'steel bar': 1
              , 'bumper': 2
              , 'chassis': 3
              , 'cabin': 4
              , 'door window': 5
              , 'windscreen': 6
              , 'blue container': 7
              , 'red tank': 8
              , 'blue motor': 9
              , 'red motor': 10
              , 'headlight': 11}

    # 부품별 가격
    PRICE_ARR = (0.3, 1, 0.2, 0.8, 2.75, 0.1, 0.29, 2.6, 3, 1.65, 1.65, 0.15)

    # 고정 조립 비용 (3000개씩)
    BLUE_LORRY_COST = 2.2 * 3000
    RED_LORRY_COST = 2.6 * 3000

    # 고정 부품 비용
    BLUE_CONTAINER_COST = COMP_ARR['blue container'] * 3000
    RED_TANK_COST = COMP_ARR['red tank'] * 3000
    BLUE_MOTOR_COST = COMP_ARR['blue motor'] * 3000
    RED_MOTOR_COST = COMP_ARR['red motor'] * 3000
    HEADLIGHT_COST = COMP_ARR['headlight'] * 6000

    # 부품별 필요 갯수 (색깔 구분없이 1대당)
    COMP_COUNT_ARR = (4, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2)

    # 제품별 필요 부품 인덱스값
    PROD_BLUE = (0, 1, 2, 3, 4, 5, 6, 7, 9, 11)
    PROD_RED = (0, 1, 2, 3, 4, 5, 6, 8, 10, 11)

    # Create variables: 의사결정변수
    axle = m.addVar(lb=0, ub=600, vtype=GRB.CONTINUOUS, name="axle")                        # axle 조립 횟수 (최저 0, 최고 3000)
    assem_chassis = m.addVar(lb=0, ub=4000, vtype=GRB.CONTINUOUS, name="assem_chassis")     # assembled chassis 조립 횟수 (최저 0, 최고 4000)
    assem_cabin = m.addVar(lb=0, ub=3000, vtype=GRB.CONTINUOUS, name="assem_cabin")         # assembled cabin 조립 횟수 (최저 0, 최고 3000)

    # Create variables: 일반변수 (외주 조립 갯수)
    SUB_AXLE = 12000 - axle
    SUB_ASSEM_CHASSIS = 6000 - assem_chassis
    SUB_ASSEM_CABIN = 6000 - assem_cabin

    SUB_PRICE_ARR = (12.75, 30, 3)  # Axle, Assembled chassis, Assembled cabin 외주비용

    # 부품별 자체조립 비용
    MINORETTE_PRICE_ARR = (6.8 + (PRICE_ARR[COMP_ARR["wheel"]] * 2) + PRICE_ARR[COMP_ARR["steel bar"]]
                           , 3.55 + (PRICE_ARR[COMP_ARR["bumper"]] * 2) + PRICE_ARR[COMP_ARR["chassis"]]
                           , 3.2 + PRICE_ARR[COMP_ARR["cabin"]] + (PRICE_ARR[COMP_ARR["door window"]] * 2) + PRICE_ARR[COMP_ARR["windscreen"]])

    # Add constraint: Axle 조립가능 갯수 제약
    m.addConstr(axle <= 2 * assem_chassis, name="ca")

    # Set objective: 목적함수(Minimize 총비용 = 자체조립비용 + 부품비용 + 외주비용)
    m.setObjective(
        axle * MINORETTE_PRICE_ARR[0] + assem_chassis * MINORETTE_PRICE_ARR[1] + assem_cabin * MINORETTE_PRICE_ARR[2]
        + BLUE_LORRY_COST + RED_LORRY_COST + BLUE_CONTAINER_COST + RED_TANK_COST + BLUE_MOTOR_COST + RED_MOTOR_COST + HEADLIGHT_COST
        + SUB_AXLE * SUB_PRICE_ARR[0] + SUB_ASSEM_CHASSIS * SUB_PRICE_ARR[1] + SUB_ASSEM_CABIN * SUB_PRICE_ARR[2]
        , GRB.MINIMIZE)


    # Optimize model
    m.optimize()

    # DataFrame 만들기(생산량)
    print('--------------------------------------------------------------------------')
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('--------------------------------------------------------------------------')

    # 결과(최적해)
    print('Objective Value : € %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
