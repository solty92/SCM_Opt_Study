import gurobipy as gp
from gurobipy import GRB

try:

    # Create a new model
    m = gp.Model("lorry")

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
    PRICE = {'wheel': 0.3
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

    # 외주 가능한 조립품
    SUB_POSSIBLE_COMPONET = ('axle', 'assembled chassis', 'assembled cabin')

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
    BLUE_CONTAINER_COST = BLUEPRINT[bl]['blue container'] * PRICE['blue container']
    RED_TANK_COST = BLUEPRINT[rl]['red tank'] * PRICE['red tank']

    BLUE_MOTOR_COST = BLUEPRINT[bl]['blue motor'] * PRICE['blue motor']
    RED_MOTOR_COST = BLUEPRINT[rl]['red motor'] * PRICE['red motor']

    BLUE_HEADLIGHT_COST = BLUEPRINT[bl]['headlight'] * PRICE['headlight']

    RED_HEADLIGHT_COST = BLUEPRINT[rl]['headlight'] * PRICE['headlight']

    # 부품별 자체조립 비용
    MINORETTE_PRICE = {
          'axle': ASSEM_COST['axle']
                  + BLUEPRINT['axle']['wheel'] * PRICE['wheel']
                  + BLUEPRINT['axle']['steel bar'] * PRICE['steel bar']
        , 'assembled chassis': ASSEM_COST['assembled chassis']
                               + BLUEPRINT['assembled chassis']['bumper'] * PRICE['bumper']
                               + BLUEPRINT['assembled chassis']['chassis'] * PRICE['chassis']
        , 'assembled cabin': ASSEM_COST['assembled cabin']
                             + BLUEPRINT['assembled cabin']['cabin'] * PRICE['cabin']
                             + BLUEPRINT['assembled cabin']['door window'] * PRICE['door window']
                             + BLUEPRINT['assembled cabin']['windscreen'] * PRICE['windscreen']
    }

    # Create variables: 의사결정변수
    assem = m.addVars(len(SUB_POSSIBLE_COMPONET), lb=0, vtype=GRB.CONTINUOUS, name='assem')                  # 조립부품의 각 자체 조립 개수 (axle, assembled chassis, assembled cabin)
    subcontract = m.addVars(len(SUB_POSSIBLE_COMPONET), lb=0, vtype=GRB.CONTINUOUS, name='subcontract')      # 조립부품의 구매 개수 (axle, asssembled chassis, assembled cabin)

    # Add constraint: 조립 Capa 제약
    m.addConstr(assem[0] <= ASSEM_CAPA['axle'], name='')
    m.addConstr(assem[1] <= ASSEM_CAPA['assembled chassis'], name='')
    m.addConstr(assem[2] <= ASSEM_CAPA['assembled cabin'], name='')

    # Add constraint: 조립, 구매 상관관계 제약
    m.addConstr(assem[0] + subcontract[0] >= assem[1] * BLUEPRINT['assembled chassis']['axle'], name='')
    m.addConstr(assem[1] + subcontract[1] >= SF[bl] + SF[rl], name='')
    m.addConstr(assem[2] + subcontract[2] >= SF[bl] + SF[rl], name='')

    # Set objective: Minimize 생산cost (부품비용, 조립비용, 구매비용)
    obj = 0

    # 자체조립비용
    obj += assem[0] * MINORETTE_PRICE['axle']
    obj += assem[1] * MINORETTE_PRICE['assembled chassis']
    obj += assem[2] * MINORETTE_PRICE['assembled cabin']

    obj += ASSEM_COST[bl] * SF[bl]
    obj += ASSEM_COST[rl] * SF[rl]

    # 외주비용
    obj += subcontract[0] * PRICE['axle']
    obj += subcontract[1] * PRICE['assembled chassis']
    obj += subcontract[2] * PRICE['assembled cabin']

    # 부품 비용
    obj += (BLUE_CONTAINER_COST + BLUE_MOTOR_COST + BLUE_HEADLIGHT_COST) * SF[bl]
    obj += (RED_TANK_COST + RED_MOTOR_COST + RED_HEADLIGHT_COST) * SF[rl]

    m.setObjective(obj, GRB.MINIMIZE)

    # Optimize model
    m.optimize()

    # 결정변수 값들 배열에 담기
    assemResult = []
    subResult = []
    idx = 0
    for v in m.getVars():
        # print('%s : %g' % (v.varName, v.x))
        if idx < 3:
            assemResult.append(v.x)
        else:
            subResult.append(v.x)
        idx += 1

    # DataFrame 만들기
    print('--------------------------------------------------------------------------')
    print('- assem count')
    for i in range(len(assemResult)):
        print(SUB_POSSIBLE_COMPONET[i], ': ', assemResult[i])

    print('- subcontracting count')
    for i in range(len(subResult)):
        print(SUB_POSSIBLE_COMPONET[i], ': ', subResult[i])
    print('--------------------------------------------------------------------------')

    # 결과
    print('Objective Value : € %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
