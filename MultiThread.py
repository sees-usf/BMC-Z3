from bmc import *
from z3 import *
bmchecker = bmc()

#list of state variables declared for this model
variables = [('thr1', 'int'),('thr2', 'int'),('flag_1', 'bool'), ('flag_2', 'bool'), ('x', 'int'), ('turn', 'int')]
variables_enc_0, variables_enc_1 = bmchecker.add_variables(variables)

#aliases of state variables
thr1 = variables_enc_0[0]
thr2 = variables_enc_0[1]
flag1 = variables_enc_0[2]
flag2 = variables_enc_0[3]
x = variables_enc_0[4]
turn = variables_enc_0[5]
thr1_x = variables_enc_1[0]
thr2_x = variables_enc_1[1]
flag1_x = variables_enc_1[2]
flag2_x = variables_enc_1[3]
x_x = variables_enc_1[4]
turn_x = variables_enc_1[5]

state0_enc = And((x == 0), (flag1 == False), (flag2 == False), (turn == 0))

bmchecker.add_initial_state_enc(state0_enc)

#listed out State Transitions

#thread 1
"""thr1 = Or(And(flag_1==True, flag_2==False, turn == 0, x_x==x),
            And(flag_1_x==True, flag_2_x==False, x_x==x, turn_x==1))
#thread 2
thr2 = Or(And(flag_1==True, flag_2==False, turn == 1),
            And(flag_1_x==False, flag_2_x==True, x_x==x+1, turn_x==0))"""

thr1 = Or(And(flag1 == False, turn == 0, x_x == x, flag1_x == True, turn_x == 1),
        And(flag1 == True, Not(flag2 == True), Not(turn == 0), flag1_x == True),
        And(flag1 == True, flag2 == False, turn == 0, flag1_x == False, flag2_x == True, turn_x == 1),
        And(flag1 == True, x == 0, turn == 0, flag1_x == False, flag2_x == True, turn_x == 1, x_x == x))
#thread 2
thr2 = Or(And(flag2 == False, turn == 1, x_x == x, flag2_x == True, turn_x == 0),
        And(flag2 == True, Not(flag1 == True), Not(turn == 1), flag2_x == True),
        And(flag2 == True, flag1 == False, turn == 1, flag2_x == False, flag1_x == True, turn_x == 0),
        And(flag2 == True, x >= 1, turn == 1, flag2_x == False, flag1_x == True, turn_x == 0, x_x == x+1))

all_thrds = Or(And(0<=x, x<=1),
            And(x==0, thr1, thr2==thr2_x), 
            And(x==1, thr2, thr1==thr1_x))

bmchecker.add_transition_enc(all_thrds)

bmchecker.add_property_enc(Not(And(0<=turn, turn<=1)))

status, step = bmchecker.run(100)
if status is sat:
    trace = bmchecker.get_trace(step)
    print('Error trace is printed below:')
    bmchecker.print_trace()
"""
thr1 = Or(And(flag1 == False, turn == 0, x_x == x, flag1_x == True, turn_x == 1),
        And(flag1 == True, Not(flag2 == True), Not(turn == 0), flag1_x == True),
        And(flag1 == True, flag2 == False, turn == 0, flag1_x == False, flag2_x == True, turn_x == 1),
        And(flag1 == True, x == 0, turn == 0, flag1_x == False, flag2_x == True, turn_x == 1, x_x == x))
#thread 2
thr2 = Or(And(flag2 == False, turn == 1, x_x == x, flag2_x == True, turn_x == 0),
        And(flag2 == True, Not(flag1 == True), Not(turn == 1), flag2_x == True),
        And(flag2 == True, flag1 == 0, turn == 1, flag2_x == False, flag1_x == True, turn_x == 0),
        And(flag2 == True, x >= 1, turn == 1, flag2_x == False, flag1_x == True, turn_x == 0, x_x == x+1))

"""