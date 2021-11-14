# 조립 설계도
ASSEMBLY_BLUEPRINT = {
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

# # 파랑 만들 때 가격 (외주)
# blue_sum = 0
# for i in ASSEMBLY_BLUEPRINT['blue lorry']:
#     print(i)            # assembled chassis, blue container, assembled cabin, blue motor, headlight
#     print('--COMP_PRICE[i] * ASSEMBLY_BLUEPRINT["blue lorry"][i] :', COMP_PRICE[i], '*', ASSEMBLY_BLUEPRINT['blue lorry'][i])
#     blue_sum += COMP_PRICE[i] * ASSEMBLY_BLUEPRINT['blue lorry'][i]
#
# # 최종 조립비용
# blue_sum += ASSEM_COST['blue lorry']
#
# # 3000대
# blue_sum *= SF['blue lorry']
#
# print('blue_sum :', blue_sum)
#
#
# # 빨강 만들 때 가격 (외주)
# red_sum = 0
# for i in ASSEMBLY_BLUEPRINT['red lorry']:
#     print(i)            # assembled chassis, red tank, assembled cabin, red motor, headlight
#     print("--COMP_PRICE[i] * ASSEMBLY_BLUEPRINT['red lorry'][i] :", COMP_PRICE[i], '*', ASSEMBLY_BLUEPRINT['red lorry'][i])
#     red_sum += COMP_PRICE[i] * ASSEMBLY_BLUEPRINT['red lorry'][i]
#
# # 최종 조립비용
# red_sum += ASSEM_COST['red lorry']
#
# # 3000대
# red_sum *= SF['red lorry']
#
# print('red_sum :', red_sum)


# 파랑 만들 때 가격 (조립)
cnt = 1500
# 고정 부품 먼저
blue_assem_sum = COMP_PRICE['blue container'] * ASSEMBLY_BLUEPRINT['blue lorry']['blue container'] \
                 + COMP_PRICE['blue motor'] * ASSEMBLY_BLUEPRINT['blue lorry']['blue motor'] \
                 + COMP_PRICE['headlight'] * ASSEMBLY_BLUEPRINT['blue lorry']['headlight'] \
                 + COMP_PRICE['assembled cabin'] * ASSEMBLY_BLUEPRINT['blue lorry']