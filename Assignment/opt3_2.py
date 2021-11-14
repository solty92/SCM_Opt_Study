import gurobipy as gp
from gurobipy import GRB, quicksum
import pandas as pd
# from IPython.display import display

try:

    # Create a new model
    m = gp.Model("truck")

    # Create variables: 일반변수
    # 조립 설계도
    BLUEPRINT = {
        'axle': {
            'wheel': 2,
            'steel bar': 1
        },
        'assembled chassis': {
            'bumper': 2,
            'axle': 2,
            'chassis': 1
        },
        'assembled cabin': {
            'cabin': 1,
            'door window': 2,
            'windscreen': 1
        },
        'blue lorry': {
            'assembled chassis': 1,
            'blue container': 1,
            'assembled cabin': 1,
            'blue motor': 1,
            'headlight': 2
        },
        'red lorry': {
            'assembled chassis': 1,
            'red tank': 1,
            'assembled cabin': 1,
            'red motor': 1,
            'headlight': 2
        }
    }

    # 부품, 조립품 구매가격
    COMP_PRICE = {'wheel': 0.3
        , 'steel bar': 1
        , 'bumper': 0.2
        , 'chassis': 0.8
        , 'cabin': 2.75
        , 'door window': 0.1
        , 'windscreen': 0.29
        , 'blue container': 2.6
        , 'red tank': 3
        , 'blue motor': 1.65
        , 'red motor': 1.65
        , 'headlight': 0.15
        , 'axle': 12.75
        , 'assembled chassis': 30
        , 'assembled cabin': 3
                  }

    # 조립비용
    ASSEM_COST = {
        'axle': 6.8
        , 'assembled chassis': 3.55
        , 'assembled cabin': 3.2
        , 'blue lorry': 2.2
        , 'red lorry': 2.6
    }

    # 최대 조립 가능 개수
    ASSEM_CAPA = {
        'axle': 600
        , 'assembled chassis': 4000
        , 'assembled cabin': 3000
        , 'blue lorry': 4000
        , 'red lorry': 5000
    }

    # 예측수요량
    SF = {
        'blue lorry': 3000
        , 'red lorry': 3000
    }

    bl = 'blue lorry'
    rl = 'red lorry'

    # 조립 비용
    BLUE_LORRY_COST = ASSEM_COST[bl]
    RED_LORRY_COST = ASSEM_COST[rl]

    # 비조립 부품 비용 (트럭별 부품 필요개수 * 부품가격)
    BLUE_CONTAINER_COST = BLUEPRINT[bl]['blue container'] * COMP_PRICE['blue container']
    RED_TANK_COST = BLUEPRINT[rl]['red tank'] * COMP_PRICE['red tank']

    BLUE_MOTOR_COST = BLUEPRINT[bl]['blue motor'] * COMP_PRICE['blue motor']
    RED_MOTOR_COST = BLUEPRINT[rl]['red motor'] * COMP_PRICE['red motor']

    BLUE_HEADLIGHT_COST = BLUEPRINT[bl]['headlight'] * COMP_PRICE['headlight']

    RED_HEADLIGHT_COST = BLUEPRINT[rl]['headlight'] * COMP_PRICE['headlight']

    # 부품별 자체조립 비용
    MINORETTE_PRICE = {'axle': ASSEM_COST['axle'] + BLUEPRINT['axle']['wheel'] * COMP_PRICE['wheel'] + BLUEPRINT['axle']['steel bar'] * COMP_PRICE['steel bar']
        , 'assembled chassis': ASSEM_COST['assembled chassis'] + BLUEPRINT['assembled chassis']['bumper'] * COMP_PRICE['bumper'] + BLUEPRINT['assembled chassis']['chassis'] * COMP_PRICE['chassis']
        , 'assembled cabin': ASSEM_COST['assembled cabin'] + BLUEPRINT['assembled cabin']['cabin'] * COMP_PRICE['cabin'] + BLUEPRINT['assembled cabin']['door window'] * COMP_PRICE['door window'] + BLUEPRINT['assembled cabin']['windscreen'] * COMP_PRICE['windscreen']}

    # Axle, Assembled chassis, Assembled cabin 외주비용
    SUB_PRICE = {'axle': 12.75
        , 'assembled chassis': 30
        , 'assembled cabin': 3}

    # Create variables: 의사결정변수
    axle = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="axle")                        # axle 조립 횟수 (최저 0)
    assem_chassis = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="assem_chassis")      # assembled chassis 조립 횟수 (최저 0)
    assem_cabin = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="assem_cabin")          # assembled cabin 조립 횟수 (최저 0)

    sub_axle = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="sub_axle")                    # axle 주문 개수 (최저 0)
    sub_assem_chassis = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="sub_assem_chassis")  # assembled chassis 주문 횟수 (최저 0)
    sub_assem_cabin = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="sub_assem_cabin")      # assembled cabin 주 횟수 (최저 0)

    # Add constraint: 조립 Capacity 제약
    m.addConstr(axle <= 600, name="")
    m.addConstr(assem_chassis <= 4000, name="")
    m.addConstr(assem_cabin <= 3000, name="")
    m.addConstr(SF['blue lorry'] <= ASSEM_CAPA['blue lorry'], name="")
    m.addConstr(SF['red lorry'] <= ASSEM_CAPA['red lorry'], name="")

    # Add constraint: 외주 제약
    m.addConstr(axle + sub_axle == BLUEPRINT['assembled chassis']['axle'] * assem_chassis, name="")
    m.addConstr(assem_chassis + sub_assem_chassis == SF[bl] + SF[rl], name="")
    m.addConstr(assem_cabin + sub_assem_cabin == SF[bl] + SF[rl], name="")

    # Set objective: 목적함수(Minimize 총비용 = 자체조립비용 + 외주비용 + 부품비용)
    obj = 0
    print('1----------------------------------', obj)

    # 자체조립비용
    obj += axle * (BLUEPRINT['axle']['wheel'] * COMP_PRICE['wheel'] + BLUEPRINT['axle']['steel bar'] * COMP_PRICE['steel bar'])
    obj += assem_chassis * (BLUEPRINT['assembled chassis']['bumper'] * COMP_PRICE['bumper'] + BLUEPRINT['assembled chassis']['chassis'] * COMP_PRICE['chassis'])
    obj += assem_cabin * (BLUEPRINT['assembled cabin']['cabin'] * COMP_PRICE['cabin'] + BLUEPRINT['assembled cabin']['door window'] * COMP_PRICE['door window'] + BLUEPRINT['assembled cabin']['windscreen'] * COMP_PRICE['windscreen'])

    obj += ASSEM_COST[bl] * SF[bl]
    obj += ASSEM_COST[rl] * SF[rl]

    # 외주비용
    obj += sub_axle * SUB_PRICE['axle']
    obj += sub_assem_chassis * SUB_PRICE['assembled chassis']
    obj += sub_assem_cabin * SUB_PRICE['assembled cabin']

    # 부품 비용
    obj += (BLUE_CONTAINER_COST + BLUE_MOTOR_COST + BLUE_HEADLIGHT_COST) * SF[bl]
    obj += (RED_TANK_COST + RED_MOTOR_COST + RED_HEADLIGHT_COST) * SF[rl]

    m.setObjective(obj, GRB.MINIMIZE)

    # Optimize model
    m.optimize()

    # 변수 값
    print('--------------------------------------------------------------------------')
    print('- 조립 / 외주 변수 값')
    tmpList = []
    for v in m.getVars():
        print('%s : %g' % (v.varName, v.x))
        tmpList.append(v.x)

    # print(tmpList)
    tmp_axle = tmpList[0]
    tmp_assem_chassis = tmpList[1]
    tmp_assem_cabin = tmpList[2]
    tmp_sub_axle = tmpList[3]
    tmp_sub_assem_chassis = tmpList[4]
    tmp_sub_assem_cabin = tmpList[5]

    print('--------------------------------------------------------------------------')
    print('- 부품별 사용량')
    for i in BLUEPRINT['axle']:
        BLUEPRINT['axle'][i] *= tmp_axle
    print(BLUEPRINT['axle'])

    for i in BLUEPRINT['assembled chassis']:
        BLUEPRINT['assembled chassis'][i] *= tmp_assem_chassis
    BLUEPRINT['assembled chassis']['axle'] -= tmp_sub_axle
    print(BLUEPRINT['assembled chassis'])

    for i in BLUEPRINT['assembled cabin']:
        BLUEPRINT['assembled cabin'][i] *= tmp_assem_cabin
    print(BLUEPRINT['assembled cabin'])

    print('blue container :', BLUEPRINT[bl]['blue container'] * SF[bl])
    print('blue motor :', BLUEPRINT[bl]['blue motor'] * SF[bl])
    print('red tank :', BLUEPRINT[rl]['red tank'] * SF[rl])
    print('red motor :', BLUEPRINT[rl]['red motor'] * SF[rl])
    print('headlight :', BLUEPRINT[bl]['headlight'] * SF[bl] + BLUEPRINT[rl]['headlight'] * SF[rl])

    print('sub_axle :', tmp_sub_axle)
    print('sub_assembled_chassis :', tmp_sub_assem_chassis)
    print('sub_assembled cabin :', tmp_sub_assem_cabin)
    print('--------------------------------------------------------------------------')

    # 결과(최적해)
    print('Objective Value : € %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')


