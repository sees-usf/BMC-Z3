from z3 import *

_BMC_UPPER_BOUND_ = (1 << 16)

class bmc:
    
    def __init__(self):
        self.variables = []
        self.variables_enc_0 = []  # list of variable encoding for current state
        self.variables_enc_1 = []  # list of variable encoding for next state
        self.frame_variables_enc = [] # list of encoded variables for each frame
        self.init_state = None
        self.prop_state = None
        self.transitions = None
        self.solver = Solver()
        self.param_variables = []  # list of parameterizable variables to enable transition encoding
        self.trace = []

        # pre-allocate the space for frame variables list
        for i in range(_BMC_UPPER_BOUND_):
            self.frame_variables_enc.append([])

    # add variables and create their different encodings
    def add_variables(self, var_list):
        self.variables = var_list
        for name, type in var_list:
            if type == 'bool':
                self.variables_enc_0.append(Bool(name+'0'))
                self.variables_enc_1.append(Bool(name+'1'))
            elif type == 'int':
                self.variables_enc_0.append(Int(name+'0'))
                self.variables_enc_1.append(Int(name+'1'))

            # Create list of parameterized variables for transition encodings 
            self.param_variables.append(name+'@{}')

        return self.variables_enc_0, self.variables_enc_1


    # add initial state encoding 
    def add_initial_state_enc(self, s0):
        self.init_state = s0

    # add property encoding
    def add_property_enc(self, p):
        self.prop_state = p

    # add transition encoding
    def add_transition_enc(self, tr):
        self.transitions = tr

    # Create and return an encoded Z3 variables for the given name, type and bound = k
    def encode_variable(self, name, type, k):
        new_var = None
        if type == 'bool':
            new_var = Bool(name.format(k))
        else:
            new_var = Int(name.format(k))
        return new_var

    # Encode and return the state constraints for bound = k
    def encode_state(self, state, k):
        replace_list = []
        frame_var = []
        for i in range(len(self.variables_enc_0)):
            old_var = self.variables_enc_0[i]
            new_var = None
            name, type = self.variables[i]
            new_var = self.encode_variable(self.param_variables[i], type, k)
            replace_list.append((old_var, new_var))
            frame_var.append(new_var)
        if not self.frame_variables_enc[k]:
            self.frame_variables_enc[k] = frame_var
        
        return substitute(state, replace_list)

    # Encode and return a frame of transition constraints from bounds k to l
    def encode_frame(self, k, l):
        frame_k = self.transitions

        replace_list = []
        frame_var = []
        for i in range(len(self.variables_enc_0)):
            old_var = self.variables_enc_0[i]
            new_var = None
            name, type = self.variables[i]
            new_var = self.encode_variable(self.param_variables[i], type, k)
            replace_list.append((old_var, new_var))
            frame_var.append(new_var)
        frame_k = substitute(frame_k, replace_list)
        if not self.frame_variables_enc[k]:
            self.frame_variables_enc[k] = frame_var

        replace_list = []
        frame_var = []
        for i in range(len(self.variables_enc_1)):
            old_var = self.variables_enc_1[i]
            new_var = None
            name, type = self.variables[i]
            new_var = self.encode_variable(self.param_variables[i], type, l)
            replace_list.append((old_var, new_var))
        frame_k = substitute(frame_k, replace_list)
        if not self.frame_variables_enc[k]:
            self.frame_variables_enc[k] = frame_var

        return frame_k

    # Run bmc process
    def run(self, bound):                
        #insert the instantiated initial state into the solver
        self.solver.add(self.encode_state(self.init_state, 0)) 

        tr_enc = None
        for k in range(1, bound+1): 
            self.solver.add(self.encode_frame(k-1, k))  # insert instantiated transitions into the solver

            # instantiate property
            prop_state = self.encode_state(self.prop_state, k)
            
            step = ('k = %d: ' % k)

            # run Z3 solver to check property at bound k
            if self.solver.check(prop_state) == sat:
                print(step, 'sat')
                return sat, k
            else:
                print(step, 'unsat')

        return unsat, k     

    # generate and return error trace extracted from the model of the Z3 solver
    def get_trace(self, k):
        model = self.solver.model()
        
        # pre-cllocate spaces for the list for the error trace
        for i in range(k+1):
            self.trace.append([])

        for i in range(k+1):
            frame_val = []
            frame_var = self.frame_variables_enc[i]
            for j in range(len(frame_var)):
                frame_val.append(model[frame_var[j]])
            self.trace[i] = frame_val
        
        return self.trace
    
    # print trace to std output
    def print_trace(self):
        vars = '%6s'%' '
        for name, type in self.variables:
            vars = vars + ('%10s'% (name))
        print(vars)
        print('-'*len(vars)+'-------')

        vars =''
        for i in range(len(self.trace)):
            vars = vars + '%6s: ' % (i)
            for val in self.trace[i]:
                vars = vars + ('%10s'% (val))
            vars = vars + '\n'
        print(vars)



