from bmc import *

    
bmchecker = bmc()

# list of state variables declared for this model
variables = [('a', 'bool'), ('b', 'bool')]

# variables_enc_0: current state variables
# variables_enc_1: next state variables
# they are lists in the same order of variabls.
variables_enc_0, variables_enc_1 = bmchecker.add_variables(variables)


# aliases of state variables
a = variables_enc_0[0]
b = variables_enc_0[1]
a_x = variables_enc_1[0]
b_x = variables_enc_1[1]

# encode initial state, and add the constraint to the BMC
state0_enc = And(Not(a), Not(b))
bmchecker.add_initial_state_enc(state0_enc)

    
#declaring a static method that lists out all the transitions then combines
#them into one transition called all_trans which is then returned
tr_1 = And(And(Not(a), Not(b)), And(Not(a_x), b_x))
tr_2 = And(And(Not(a), Not(b)), And(a_x, Not(b_x)))
tr_3 = And(And(Not(a), b), And(Not(a_x), Not(b_x)))
tr_4 = And(And(a, Not(b)), And(Not(a_x), Not(b_x)))
tr_5 = And(And(a, Not(b)), And(a_x, b_x))
tr_6 = And(And(a,b), And(Not(a_x), Not(b_x)))
        
all_tr = Or(tr_1, tr_2, tr_3, tr_4, tr_5, tr_6)

bmchecker.add_transition_enc(all_tr)


bmchecker.add_property_enc(And(a, b))

status, step = bmchecker.run(9)
if status is sat:
    trace = bmchecker.get_trace(step)
    print('Error trace is printed below:')
    bmchecker.print_trace()
    
