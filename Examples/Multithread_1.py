from bmc import *
from z3 import *
bmchecker = bmc()

#list of state variables declared for this model
variables = [('pc_thrd1', 'int'), ('pc_thrd2', 'int'), ('flag1', 'int'), ('flag2', 'int'), ('x', 'int'), ('turn', 'int'), ('pid', 'int')]
variables_enc_0, variables_enc_1 = bmchecker.add_variables(variables)

#aliases of state variables
pc_thrd1 = variables_enc_0[0]
pc_thrd2 = variables_enc_0[1]
flag1 = variables_enc_0[2]
flag2 = variables_enc_0[3]
x = variables_enc_0[4]
turn = variables_enc_0[5]
pid = variables_enc_0[6]
pc_thrd1_x = variables_enc_1[0]
pc_thrd2_x = variables_enc_1[1]
flag1_x = variables_enc_1[2]
flag2_x = variables_enc_1[3]
x_x = variables_enc_1[4]
turn_x = variables_enc_1[5]

state0_enc = And((x == 0), (flag1 == 0), (flag2 == 0), (turn == 0), (pc_thrd1 == 0), (pc_thrd2 == 0), (pid == 0))

bmchecker.add_initial_state_enc(state0_enc)

#listed out State Transitions


#thread 1
thr1 = Or(And(pc_thrd1 == 0, flag1 == 1, Not(flag2 < 1), flag1_x == 1, pc_thrd1_x == 1),
        And(pc_thrd1 == 0, flag1 == 1, flag2 < 1, flag1_x == flag1, turn_x == turn, pc_thrd1 == 3),
        And(pc_thrd1 == 1, flag1 == 1, Not(flag2 < 1), Not(turn == 0), pc_thrd1_x == 2),
        And(pc_thrd1 == 1, flag1 == 1, Not(flag2 < 1), turn == 0, flag1_x == flag1, pc_thrd1_x == 3),
        And(pc_thrd1 == 2, flag1 == 1, Not(flag2 < 1), Not(turn == 0), flag1_x == 0, turn_x == turn, pc_thrd1_x == 2),
        And(pc_thrd1 == 2, flag1 == 0, Not(flag2 < 1), turn == 0, flag1_x == 1, turn_x == turn, pc_thrd1_x == 3),
        And(pc_thrd1 == 3, flag1 == 1, x == 0, x_x <= 0, turn == 0, flag1_x == 0, turn_x == 1, pc_thrd1_x == 0))


#thread 2
thr2 = Or(And(pc_thrd2 == 0, flag2 == 1, Not(flag1 < 1), flag2_x == 1, pc_thrd2_x == 1),
        And(pc_thrd2 == 0, flag2 == 1, flag1 < 1, flag2_x == flag2, turn_x == turn, pc_thrd2 == 3),
        And(pc_thrd2 == 1, flag2 == 1, Not(flag1 < 1), Not(turn == 1), pc_thrd2_x == 2),
        And(pc_thrd2 == 1, flag2 == 1, Not(flag1 < 1), turn == 1, flag2_x == flag2, pc_thrd2_x == 3),
        And(pc_thrd2 == 2, flag2 == 1, Not(flag1 < 1), Not(turn == 1), flag2_x == 0, turn_x == turn, pc_thrd2_x == 2),
        And(pc_thrd2 == 2, flag2 == 0, Not(flag1 < 1), turn == 1, flag2_x == 1, turn_x == turn, pc_thrd2_x == 3),
        And(pc_thrd2 == 3, flag2 == 1, x == 1, x_x >= 1, turn == 1, flag2_x == 0, turn_x == 1, pc_thrd2_x == 0))






all_thrds = And((And(0<=pid, pid<=1),
            Or(And(0<=turn, turn<=1),
            And(pid == 0, turn == 1, thr1, pc_thrd2 == pc_thrd2_x),
            And(pid == 1, turn == 0, thr2, pc_thrd1 == pc_thrd1_x))))



bmchecker.add_transition_enc(all_thrds)

bmchecker.add_property_enc(Not(And(0>=x, x<=1)))

status, step = bmchecker.run(100)
if status is sat:
    trace = bmchecker.get_trace(step)
    print('Error trace is printed below:')
    bmchecker.print_trace()