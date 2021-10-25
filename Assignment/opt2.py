import gurobipy as gp
from gurobipy import GRB, quicksum
import pandas as pd
from IPython.display import display

try:

    # Create a new model
    m = gp.Model("glasses")

    # Create variables: 일반변수
    BATCHES = 1000                                                      # 생산 묶음 단위
    TYPE = 6                                                            # 유형 갯수
    WEEK_ARR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]                  # 12주 배열
    DEMAND_ARR = [[20, 22, 18, 35, 17, 19, 23, 20, 29, 30, 28, 32],
                  [17, 19, 23, 20, 11, 10, 12, 34, 21, 23, 30, 12],
                  [18, 35, 17, 10, 9, 21, 23, 15, 10, 0, 13, 17],
                  [31, 45, 24, 38, 41, 20, 19, 37, 28, 12, 30, 37],
                  [23, 20, 23, 15, 10, 22, 18, 30, 28, 7, 15, 10],
                  [22, 18, 20, 19, 18, 35, 0, 28, 12, 30, 21, 23]]      # 수요 계획수량 배열

    PROD_COST_ARR = [100, 80, 110, 90, 200, 140]                        # 유형별 생산 비용 (묶음단위 당)
    STORE_COST_ARR = [25, 28, 25, 27, 10, 20]                           # 유형별 보관 비용 (묶음단위 당)

    INIT_STOCK_ARR = [50, 20, 0, 15, 0, 10]                             # 유형별 기초 재고수량
    FINAL_STOCK_ARR = [10, 10, 10, 10, 10, 10]                          # 유형별 기말 재고수량

    WORKER_TIME_ARR = [3, 3, 3, 2, 4, 4]                                # 유형별 필요 근무시간 (묶음단위 당)
    MACHINE_TIME_ARR = [2, 1, 4, 8, 11, 9]                              # 유형별 필요 작동시간 (묶음단위 당)
    WORKER_TIME_MAX = 390                                               # 근로자 최대 근무시간 (주당)
    MACHINE_TIME_MAX = 850                                              # 기계 최대 작동시간 (주당)

    STORAGE_SPACE_ARR = [4, 5, 5, 6, 4, 9]                              # 유형별 필요 보관공간 (묶음단위 당)
    STORAGE_SPACE_MAX = 1000                                            # 최대 보관공간 크기

    # Create variables: 의사결정변수
    prod_type_week = m.addVars(TYPE, len(WEEK_ARR), vtype=GRB.INTEGER, lb=0, name='prod_type_week')     # 유형, 주별 생산량
    stock_type_week = m.addVars(TYPE, len(WEEK_ARR), vtype=GRB.INTEGER, lb=0, name='stock_type_week')   # 유형, 주별 재고수량

    # Add constraint: 재고수량 제약 (당월 재고수량 = 전월 or 기초 재고수량 + 당월 생산량 - 당월 수요량)
    m.addConstrs(
        (stock_type_week[i, 0] == INIT_STOCK_ARR[i] + prod_type_week[i, 0] - DEMAND_ARR[i][0]
         for i in range(TYPE)), name='ca')                                                              # 1월 재고수량 제약

    m.addConstrs(
        (stock_type_week[i, j] == stock_type_week[i, j - 1] + prod_type_week[i, j] - DEMAND_ARR[i][j]
         for i in range(TYPE) for j in range(1, len(WEEK_ARR))), name='cb')                             # 2~12월 재고수량 제약

    m.addConstrs(
        (stock_type_week[i, len(WEEK_ARR) - 1] >= FINAL_STOCK_ARR[i]
         for i in range(TYPE)), name='cc')                                                              # 기말 재고수량 제약

    # Add constraint: 작업시간 제약 (sum(제품 유형별 주별 생산량 * 제품 유형별 작업시간) <= 주당 최대 작업시간)
    m.addConstrs(
        ((quicksum(prod_type_week[i, j] * WORKER_TIME_ARR[i] for i in range(TYPE)) <= WORKER_TIME_MAX)
         for j in range(len(WEEK_ARR))), name='cd')                                                     # 근로자 근무시간 제약 (주당)

    m.addConstrs(
        ((quicksum(prod_type_week[i, j] * MACHINE_TIME_ARR[i] for i in range(TYPE)) <= MACHINE_TIME_MAX)
         for j in range(len(WEEK_ARR))), name='ce')                                                     # 기계 작동시간 제약 (주당)

    # Add constraint: 보관공간 제약 (sum(제품 유형별 주별 보관량 * 제품 유형별 보관공간) <= 최대 보관공간 크기)
    m.addConstrs(
        ((quicksum(stock_type_week[i, j] * STORAGE_SPACE_ARR[i] for i in range(TYPE)) <= STORAGE_SPACE_MAX)
         for j in range(len(WEEK_ARR))), name='cf')

    # Set objective: 목적함수(Minimize 총비용 = 생산비용 + 재고비용)
    m.setObjective(
        (quicksum(prod_type_week[i, j] * PROD_COST_ARR[i] + stock_type_week[i, j] * STORE_COST_ARR[i]
                  for i in range(TYPE) for j in range(len(WEEK_ARR)))) * BATCHES, GRB.MINIMIZE)

    # Optimize model
    m.optimize()

    # 결정변수 값들 배열에 담기 (DataFrame)
    # 제품생산량
    prod_type_week_arr = [[0 for col in range(len(WEEK_ARR))] for row in range(TYPE)]
    count = 0
    for v in prod_type_week.values():
        i = count // len(WEEK_ARR)      # 유형
        j = count % len(WEEK_ARR)       # 주
        prod_type_week_arr[i][j] = int(v.X)
        count += 1

    # 재고수량
    stock_type_week_arr = [[0 for col in range(len(WEEK_ARR))] for row in range(TYPE)]
    count = 0
    for v in stock_type_week.values():
        i = count // len(WEEK_ARR)      # 유형
        j = count % len(WEEK_ARR)       # 주
        stock_type_week_arr[i][j] = int(v.X)
        count += 1

    # DataFrame 만들기(생산량)
    print('--------------------------------------------------------------------------')
    print('< Production for the planning period (batches of 1000 glasses) >')
    df_prod = pd.DataFrame({'V1': prod_type_week_arr[0],
                            'V2': prod_type_week_arr[1],
                            'V3': prod_type_week_arr[2],
                            'V4': prod_type_week_arr[3],
                            'V5': prod_type_week_arr[4],
                            'V6': prod_type_week_arr[5]})
    df_prod.index = WEEK_ARR        # Dataframe 인덱스
    df_prod = df_prod.transpose()   # Dataframe 축 변환
    display(df_prod)

    # DataFrame 만들기(재고수량)
    print('--------------------------------------------------------------------------')
    print('< Stock for the planning period (batches of 1000 glasses) >')
    df_stock = pd.DataFrame({'V1': stock_type_week_arr[0],
                             'V2': stock_type_week_arr[1],
                             'V3': stock_type_week_arr[2],
                             'V4': stock_type_week_arr[3],
                             'V5': stock_type_week_arr[4],
                             'V6': stock_type_week_arr[5]})
    df_stock.index = WEEK_ARR           # Dataframe 인덱스
    df_stock = df_stock.transpose()     # Dataframe 축 변환
    display(df_stock)

    print('--------------------------------------------------------------------------')

    # 결과(최적해)
    print('Objective Value : € %i' % m.objVal)
    print('--------------------------------------------------------------------------')


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')