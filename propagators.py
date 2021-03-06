'''
This file contains constraint propagators to be used within bt_search.

A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object - the propagator can use this to get access to the 
variables and constraints of the problem. The assigned variables and values
can be accessed via methods.

newly_instantiated_variable is an optional argument.
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs.

Propagators will return False if they detect a dead-end. In this case, 
bt_search will backtrack. Propagators will return True if we can continue.

The list of variable-value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search needs to know 
this in order to correctly restore these values when it undoes a variable 
assignment.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Only 
    check fully instantiated constraints.

    If called with newVar = a variable V, we check all constraints with V that
    are fully assigned.
    '''
    if not newVar:
        return True, []
    #loop through list of [constraints that include newVar in their scope]
    for c in csp.get_cons_with_var(newVar):
        #if all vars in constraint c's scope are assigned
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            #loop through scope: list of [vars that the constraint is over]
            for var in vars:
                #append var's assigned value to vals
                vals.append(var.get_assigned_value())
            #if vals assignments don't satisfy constraint c
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''
    Do forward checking propagation. Check constraints that have exactly one 
    uninstantiated variable in their scope, and prune appropriately. 

    If newVar is None, forward check all constraints whose scope contains one 
    variable. Otherwise if newVar = V, forward check constraints containing V
    that have one unassigned variable left.
    '''
    pruned = []
    
    if newVar: #check constraints containing newVar
        constraints = csp.get_cons_with_var(newVar)
    else: #check all constraints
        constraints = csp.get_all_cons()

    for c in constraints:
        
        #if only 1 var in constraint c's scope is unassigned
        if c.get_n_unasgn() == 1:
            v = c.get_unasgn_vars()[0]
            
            #loop through list of [vals in current domain of unassigned var]
            for d in v.cur_domain(): #check d & prune if violates
                
                #assign d to value of unassigned var
                v.assign(d)
                
                #loop through scope of c, add variables' vals in scope order
                vals = []
                vars = c.get_scope()
                for var in vars:
                    vals.append(var.get_assigned_value())
                
                #if vals assignments don't satisfy constraint c
                if not c.check(vals):
                    #if d is in v's domain && v not yet pruned
                    if (v.in_cur_domain(d)) and ((v, d) not in pruned):
                        #prune d from current domain (of v)
                        v.prune_value(d)
                        pruned.append((v, d))

                #unassign d
                v.unassign()
                    
                if v.cur_domain_size() == 0: #DWO
                    return False, pruned

    return True, pruned

def prop_GAC(csp, newVar=None):
    '''
    Do GAC propagation. 

    If newVar is None, we initialise the GAC queue (do GAC enforce) with all 
    constraints of the CSP. Otherwise if newVar = V, we initialise the queue
    with constraints containing V.
    
    note: CSP is GAC iff all constraints are GAC.
    A constraint is GAC iff it's GAC w/r/t each var in scope.
    A constraint is GAC w/r/t a var iff for every value of V_i exist values 
    that satisfy C.
    '''
    pruned = []
    
    if newVar: #check constraints containing newVar
        constraints = csp.get_cons_with_var(newVar)
    else: #check all constraints
        constraints = csp.get_all_cons()

    for c in constraints:
        for v in c.get_scope():
        
            #loop through list of [vals in current domain of v]
            for d in v.cur_domain():

                #test if (var, val) pair has supporting tuple in c
                if not c.has_support(v, d):
                    
                    if (v.in_cur_domain(d)) and ((v, d) not in pruned):
                        #prune d from current domain (of v)
                        v.prune_value(d)
                        pruned.append((v, d))
                
                if v.cur_domain_size() == 0: #DWO
                    return False, pruned

    return True, pruned