import gurobipy as gb
from gurobipy import GRB

m = gb.Model('gurobiTest')

#############################
# Set the Data Set
#############################

# set the BOM Rate
REQ = {
        ("axle","wheel"):2
        ,("axle","steel bar"):1
        ,("assembled chassis",  "bumper"):2
        ,("assembled chassis",  "axle"):2
        ,("assembled chassis",  "chassis"):1
        ,("assembled cabin",  "cabin"):1
        ,("assembled cabin",  "door window"):2
        ,("assembled cabin",  "windscreen"):1
        ,("blue lorry",  "assembled chassis"):1
        ,("blue lorry",  "container"):1
        ,("blue lorry",  "assembled cabin"):1
        ,("blue lorry",  "blue motor"):1
        ,("blue lorry",  "headlight"):2
        ,("red lorry",  "assembled chassis"):1
        ,("red lorry",  "tank"):1
        ,("red lorry",  "assembled cabin"):1
        ,("red lorry",  "red motor"):1
        ,("red lorry",  "headlight"):2
    }

CBUY = {     "wheel":0.30
            ,"steel bar":1
            ,"bumper":0.2
            ,"axle":12.75
            ,"chassis":0.8
            ,"cabin":2.75
            ,"door window":0.1
            ,"windscreen":0.29
            ,"assembled chassis":30
            ,"container":2.60
            ,"tank":3
            ,"assembled cabin":3
            ,"blue motor":1.65
            ,"red motor":1.65
            ,"headlight":0.15
        }


CASSEMBLY = {
             "axle": 6.80
            ,"assembled chassis":3.55
            ,"assembled cabin":3.20
            ,"blue lorry":2.20
            ,"red lorry":2.60
            }

ASSEMBLYCAP = {
             "axle": 600
            ,"assembled chassis":4000
            ,"assembled cabin":3000
            ,"blue lorry":4000
            ,"red lorry":5000
            }

DEM = {
          "blue lorry":3000
        , "red lorry":3000
        }


# All item
tmpITEM = []
for i, j in REQ:
    tmpITEM.append(i)
    tmpITEM.append(j)

# ì¤‘ë³µì œê±°
tmp_set = set(tmpITEM)
ITEM = list(tmp_set)

# Final
FINAL = []
for i in DEM:
    FINAL.append(i)

# ASMBL
ASMBL = []
for i in CASSEMBLY:
    ASMBL.append(i)

# BUY
PREPROD = []
for i in CBUY:
    PREPROD.append(i)


# set the decision variables.
# PROD    = m.addVars(tPROD, name = 'prod')
# BUY     = m.addVars(tBUY, name = 'buy')

PROD    = m.addVars(ASMBL, name = 'prod')
BUY     = m.addVars(PREPROD, name = 'buy')


######################################
# set Objective function
######################################
obj = 0

for i in PREPROD:
    obj += CBUY[i] * BUY[i]

for i in ASMBL:
    obj += CASSEMBLY[i] * PROD[i]


######################################
# set Constraint
######################################
# demand constraint
for i in  FINAL:
    m.addConstr(PROD[i] >= DEM[i], "Demand_Con"+i)

# assembly capa constraint
for i in ASMBL:
    m.addConstr(PROD[i] <= ASSEMBLYCAP[i], "capacity_Con"+i)
print(PREPROD)
print(ASMBL)
# BOM rate constraint
for i in PREPROD:
    if i in ASMBL:
        m.addConstr(BUY[i] + PROD[i] >= sum(REQ[j, i] * PROD[j] for j in ASMBL if (j,i) in REQ), "assemble_con"+j+i)
    else :
        m.addConstr(BUY[i] >= sum(REQ[j, i] * PROD[j] for j in ASMBL if (j,i) in REQ), "buy_con"+j+i)

######################################
# optimize
######################################
m.setObjective(obj, GRB.MINIMIZE)
m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))