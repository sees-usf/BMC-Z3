"""
int flag1 = 0, flag2 = 0; // N boolean flags
int turn = 0; // integer variable to hold the ID of the thread whose turn is it
int x; // variable to test mutual exclusion
void thr1() {
flag1 = 1;
while (flag2 >= 1) {
if (turn != 0) {
flag1 = 0;
while (turn != 0) {};
flag1 = 1;
}
}
// begin: critical section  ```````
x = 0;
assert(x<=0);
// end: critical section
turn = 1;
flag1 = 0;
}
void thr2() {
flag2 = 1;
while (flag1 >= 1) {
if (turn != 1) {
flag2 = 0;
while (turn != 1) {};
flag2 = 1;
}
}
// begin: critical section
x = 1;
assert(x>=1);
// end: critical section
turn = 1;
flag2 = 0;
}
"""
#multi-threaded program sat solving C code for the above program
from bmc import *
from z3 import *
bmchecker = bmc()

#list of state variables declared for this model
variables = [('flag1', 'int'), ('flag2', 'int'), ('x', 'int'), ('turn', 'int')]
variables_enc_0, variables_enc_1 = bmchecker.add_variables(variables)

#aliases of state variables

flag1 = variables_enc_0[0]
flag2 = variables_enc_0[1]
x = variables_enc_0[2]
turn = variables_enc_0[3]
flag1_x = variables_enc_1[0]
flag2_x = variables_enc_1[1]
x_x = variables_enc_1[2]
turn_x = variables_enc_1[3]

state0_enc = And((x == 0), (flag1 == 0), (flag2 == 0), (turn == 0))

bmchecker.add_initial_state_enc(state0_enc)

#listed out State Transitions
"""
Thread 1:
    flag1 == 0, -> flag1_x == 1
    flag1 == 1 && !(flag2 < 1) && !(turn == 0) -> flag1_x == 1
    flag ==1 && !(flag_2 < 1) -> flag1_x == 0
    flag ==1 && (flag_2 > 1) && turn == 0 -> flag1_x == 1
"""

#thread 1
thr1 = Or(And(flag1 == 0, flag1_x ==1),
        And(flag1 == 1, Not(flag2 < 1), Not(turn == 0), flag1_x == 1, flag2_x == 0, turn_x == 0), x_x == x,
        And(flag1 == 1, Not(flag2 < 1), flag1_x == 0, flag2_x == 0, turn_x == 0, x_x == x),
        And(flag1 == 1, flag2 > 1, turn == 0, flag1_x == 1, flag2_x == 0, turn_x == 0, x_x == x))

"""
Thread 2:
    flag2 == 0, -> flag2_x == 1
    flag2 == 1 && !(flag1 < 1) && !(turn == 1) -> flag2_x == 1
    flag ==1 && !(flag_1 < 1) -> flag2_x == 0
    flag ==1 && (flag_1 > 1) && turn == 1 -> flag2_x == 1
"""
#thread 2
thr2 = Or(And(flag2 == 0, flag2_x ==1),
        And(flag2 == 1, Not(flag1 < 1), Not(turn == 1), flag2_x == 1, flag1_x == 0, turn_x == 1, x_x == x+1),
        And(flag2 == 1, Not(flag1 < 1), flag2_x == 0, flag1_x == 0, turn_x == 1, x_x == x+1),
        And(flag2 == 1, flag1 > 1, turn == 1, flag2_x == 1, flag1_x == 0, turn_x == 1, x_x == x+1))

#critical section       




all_thrds = Or(And(0<=turn, 1<=turn),
            And(turn==1, turn_x == 0,  flag1 == 0, flag2 == 1),
            And(turn==0, turn_x ==1, flag2 == 1, flag1 == 0))
bmchecker.add_transition_enc(all_thrds)

bmchecker.add_property_enc(Not(And(0>=x, x<=1)))

status, step = bmchecker.run(100)
if status is sat:
    trace = bmchecker.get_trace(step)
    print('Error trace is printed below:')
    bmchecker.print_trace()
