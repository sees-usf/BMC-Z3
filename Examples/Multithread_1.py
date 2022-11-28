""""
bool flag1 = false, 
bool flag2 = false; 
int turn = 0;   // integer variable to hold the ID of the thread whose turn is it
int x; // variable to test mutual exclusion

void thr1() {
0: flag1 = true;

1: while (flag2) 

2:     if (turn != 0) 

3:     flag1 = false;

4:     while (turn != 0) {};

5:     flag1 = 1;

// begin: critical section  ```````

6: x = x+1;

// end: critical section

7: turn = 1;

8: flag1 = false;

9: x = x-1;

void thr2() {
0: flag2 = true;

1: while (flag1) 

2:          if (turn != 1) 

3:          flag2 = false;

4:          while (turn != 1) {};

5:          flag2 = 1;

// begin: critical section

6: x = x+1;

// end: critical section

7: turn = 0;

8: flag2 = false;

9: x = x-1;
"""
#multi-threaded program sat solving C code for the above program
from bmc import *

bmchecker = bmc()

#list of state variables declared for this model
variables = [('pc_thrd1', 'int'), ('pc_thrd2', 'int'), ('flag1', 'bool'), ('flag2', 'bool'), ('x', 'int'), ('turn', 'int')]
variables_enc_0, variables_enc_1 = bmchecker.add_variables(variables)

#aliases of state variables
pc_thrd1 = variables_enc_0[0]
pc_thrd2 = variables_enc_0[1]
flag1 = variables_enc_0[2]
flag2 = variables_enc_0[3]
x = variables_enc_0[4]
turn = variables_enc_0[5]
pc_thrd1_x = variables_enc_1[0]
pc_thrd2_x = variables_enc_1[1]
flag1_x = variables_enc_1[2]
flag2_x = variables_enc_1[3]
x_x = variables_enc_1[4]
turn_x = variables_enc_1[5]


# bound variable x within range -1, 2
tr_inv = And(x>=1, x<=2, x_x>=1, x_x<=2)


state0_enc = And((flag1 == False), (flag2 == False), (turn == 0), (pc_thrd1 == 0), (pc_thrd2 == 0))

bmchecker.add_initial_state_enc(state0_enc)

#listed out State Transitions
def nochange(*l):
    c = None
    a, b = l
    if c is None:
        c = (a == b)
    else:
        c = And(a == b, (c))
    return c
#thread 1
thr1 = Or(And(pc_thrd1 == 0, flag1_x == True, pc_thrd1_x == 1, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 1, flag2_x == flag2, pc_thrd1_x == 6, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 1, Not(flag2_x == flag2), pc_thrd1_x == 2, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 2, turn == 0, pc_thrd1_x == 6, nochange(flag2, flag2_x), nochange(flag1, flag1_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 2, Not(turn == 0), pc_thrd1_x == 3, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(flag1, flag1_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 3, flag1_x == False, pc_thrd1_x == 4, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 4, turn == 0, pc_thrd1_x == 5, nochange(flag2, flag2_x), nochange(flag1, flag1_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 4, Not(turn == 0), pc_thrd1_x == 4, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(flag1, flag1_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 5, flag1_x == True, pc_thrd1_x == 6, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 6, x_x == x + 1, pc_thrd1_x == 7, nochange(flag2, flag2_x), nochange(flag1, flag1_x),nochange(turn, turn_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 7, turn_x == 1, pc_thrd1_x == 8, nochange(flag2, flag2_x), nochange(flag1, flag1_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 8, flag1_x == False, pc_thrd1_x == 0, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd2_x == pc_thrd2),
    And(pc_thrd1 == 9, x_x == x - 1, pc_thrd1_x == 0, nochange(flag2, flag2_x), nochange(flag1, flag1_x), nochange(turn, turn_x), pc_thrd2_x == pc_thrd2))


#thread 2
thr2 = Or(And(pc_thrd1 == 0, flag2_x == True, pc_thrd2_x == 1, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 1, flag1_x == flag1, pc_thrd2_x == 6, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 1, Not(flag1_x == flag1), pc_thrd2_x == 2, nochange(flag2, flag2_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 2, turn == 1, pc_thrd2_x == 6, nochange(flag1, flag1_x), nochange(flag2, flag2_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 2, Not(turn == 1), pc_thrd2_x == 3, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(flag2, flag2_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 3, flag2_x == False, pc_thrd2_x == 4, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 4, turn == 1, pc_thrd2_x == 5, nochange(flag1, flag1_x), nochange(flag2, flag2_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 4, Not(turn == 1), pc_thrd2_x == 4, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(flag2, flag2_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 5, flag2_x == True, pc_thrd2_x == 6, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 6, x_x == x + 1, pc_thrd2_x == 7, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(flag2, flag2_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 7, turn_x == 0, pc_thrd2_x == 8, nochange(flag1, flag1_x), nochange(flag2, flag2_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 8, flag2_x == False, pc_thrd2_x == 0, nochange(flag1, flag1_x), nochange(turn, turn_x), nochange(x, x_x), pc_thrd1_x == pc_thrd1),
        And(pc_thrd2 == 9, x_x == x - 1, pc_thrd2_x == 0, nochange(flag1, flag1_x), nochange(flag2, flag2_x), nochange(turn, turn_x), pc_thrd1_x == pc_thrd1))


all_thrds = And(Or(And(thr1, pc_thrd2_x == pc_thrd2), And(thr2, pc_thrd1_x == pc_thrd1)), tr_inv)


bmchecker.add_transition_enc(all_thrds)

bmchecker.add_property_enc(Or(x<0, x>1))

status, step = bmchecker.run(2000)
if status is sat:
    trace = bmchecker.get_trace(step)
    print('Error trace is printed below:')
    bmchecker.print_trace()
