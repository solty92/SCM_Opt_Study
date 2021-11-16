import gurobipy as gp
from gurobipy import GRB

try:

    # Create a new model
    m = gp.Model("wagon")

    # Create variables: 일반변수
    BOX_WEIGHT = [34, 6, 8, 17, 16, 5, 13, 21, 25, 31, 14, 13, 33, 9, 25, 25]       # 박스당 무게

    WAGON_COUNT = 3     # 화물 기차 수
    MAX_CAPA = 100

    # Create variables: 의사결정변수
    wagon_load = m.addVars(len(BOX_WEIGHT), WAGON_COUNT, vtype=GRB.INTEGER, lb=0, ub=1, name='wagon_load')      # 각 화물이 어떤 박스를 실을지 말지 결정

    # Add constraint: 당월재고량 = 전월재고량 + 당월기본생산량 + 당월초과생산량 - 당월수요량
    m.addConstrs( sum( wagon_load[i][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) ) <= MAX_CAPA for i in range(WAGON_COUNT) )

    # Set objective: 목적함수(Minimize 총비용 = 기본생산비용 + 초과생산비용 + 재고비용)
    WAGON1_SUM = sum( wagon_load[0][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) )
    WAGON2_SUM = sum( wagon_load[1][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) )
    WAGON3_SUM = sum( wagon_load[2][j] * BOX_WEIGHT[j] for j in range(len(BOX_WEIGHT)) )

    m.setObjective( abs( WAGON1_SUM - (sum(BOX_WEIGHT) / 3) ) + abs( WAGON2_SUM - (sum(BOX_WEIGHT) / 3) ) + abs( WAGON1_SUM - (sum(BOX_WEIGHT) / 3) )
        ,
        GRB.MINIMIZE)

    # Optimize model
    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('----------------------')

    # 결정변수 값들 배열에 담기 (DataFrame 용도)
    norm_prod_arr = []
    for v in wagon_load.values():
        norm_prod_arr.append(int(v.X))

    # DataFrame 만들기
    # print('--------------------------------------------------------------------------')
    # df = pd.DataFrame({'norm_prod': norm_prod_arr,
    #                    'over_prod': over_prod_arr,
    #                    'stock': stock_arr})
    # df.index = MONTH
    # display(df)
    # print('--------------------------------------------------------------------------')

    # 결과
    print('Objective Value : %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
