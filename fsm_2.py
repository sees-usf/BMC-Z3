
from bmc import *
import random
bmchecker = bmc()

#list of state variables declared for this model

variables = [('pc_inc', 'int'), ('pc_dec', 'int'), ('pc_reset', 'int'), ('x', 'int'), ('pid', 'int')]

#variables_enc_0: current state variables
#variables_enc_1: next state variables
#they are lists in the same order of variabls.
variables_enc_0, variables_enc_1 = bmchecker.add_variables(variables)

#aliases of state variables
pc_inc = variables_enc_0[0]
pc_dec = variables_enc_0[1]
pc_reset = variables_enc_0[2]
x = variables_enc_0[3]
pid = variables_enc_0[4]
pc_inc_x = variables_enc_1[0]
pc_dec_x = variables_enc_1[1]
pc_reset_x = variables_enc_1[2]
x_x = variables_enc_1[3]

state0_enc = And((x == 0), (pc_inc == 0), (pc_dec == 0), (pc_reset == 0), (pid == 0))
bmchecker.add_initial_state_enc(state0_enc)

#listed out State Transitions
"""
for inc:
    pc==0 -> pc_x==1
    pc==1 && x<200 -> pc_x==2
    pc==1 && !(x<200) -> pc_x==0
    pc==2 -> x_x := x+1 && pc_x==0
"""
#inc_enc is created by anding together the necessary state transitions to make the inc function satisfiable
inc_enc = Or(And(pc_inc==0, x_x==x, pc_inc_x==1),
            And(pc_inc==1, x<200, x_x==x, pc_inc_x==2),
            And(pc_inc==1, Not(x<200), x_x==x, pc_inc_x==0),
            And(pc_inc==2, x_x==x+1, pc_inc_x==0))
"""
 for dec:
    pc==0 -> pc_x==1
    pc==1 && x>0 -> pc_x==2
    pc==1 && !(x>0) -> pc_x==0
    pc==2 -> x_x==x-1 && pc_x==0
"""
#dec_enc is created by anding together the necessary state transitions to make the dec function satisfiable
dec_enc = Or(And(pc_dec==0, x_x==x, pc_dec_x==1),
            And(pc_dec==1, x>0, x_x==x, pc_dec_x==2),
            And(pc_dec==1, Not(x>0), x_x==x, pc_dec_x==0),
            And(pc_dec==2, x_x==x-1, pc_dec_x==0))

"""
for reset:
    pc==0 -> pc_x==1
    pc==1 && x==200 -> pc_x==2
    pc==1 && !(x==200) -> pc_x==0
    pc==2 -> x_x==0 && pc_x==0
"""
#reset_enc is created by anding together the necessary state transitions to make the reset function satisfiable
reset_enc = Or(And(pc_reset==0, x_x==x, pc_reset_x==1),
                And(pc_reset==1, x==200, x_x==x, pc_reset_x==2),
                And(pc_reset==1, Not(x==200), x_x==x, pc_reset_x==0),
                And(pc_reset==2, x_x==0, pc_reset_x==0))

total_tr = And(And(0<=pid, pid<=2,),
                Or(And(pid==0, inc_enc, pc_dec==pc_dec_x, pc_reset==pc_reset_x),
                    And(pid==1, dec_enc, pc_inc==pc_inc_x, pc_reset==pc_reset_x),
                    And(pid==2, reset_enc, pc_inc==pc_inc_x, pc_dec==pc_dec_x)))

bmchecker.add_transition_enc(total_tr)

bmchecker.add_property_enc(Not(And(0 <= x, x <= 200)))

status, step = bmchecker.run(210)
if status is sat:
    trace = bmchecker.get_trace(step)
    print('Error trace is printed below:')
    bmchecker.print_trace()
 
