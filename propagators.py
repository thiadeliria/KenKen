'''
This file will contain different constraint propagators to be used within 
bt_search.

---
A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object---the propagator can use this to get access to the variables 
and constraints of the problem. The assigned variables can be accessed via 
methods, the values assigned can also be accessed.

newly_instantiated_variable is an optional argument. SEE ``PROCESSING REQUIRED''
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs, like so
    (True/False, [(Variable, Value), (Variable, Value) ...]

Propagators will return False if they detect a dead-end. In this case, bt_search 
will backtrack. Propagators will return true if we can continue.

The list of variable value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search NEEDS to know this 
in order to correctly restore these values when it undoes a variable assignment.

Propagators SHOULD NOT prune a value that has already been pruned! Nor should 
they prune a value twice.

---

PROCESSING REQUIRED:
When a propagator is called with newly_instantiated_variable = None:

1. For plain backtracking (where we only check fully instantiated constraints)
we do nothing...return true, []

2. For FC (where we only check constraints with one remaining 
variable) we look for unary constraints of the csp (constraints whose scope 
contains only one variable) and we forward_check these constraints.

3. For GAC we initialize the GAC queue with all constaints of the csp.

When a propagator is called with newly_instantiated_variable = a variable V

1. For plain backtracking we check all constraints with V (see csp method
get_cons_with_var) that are fully assigned.

2. For forward checking we forward check all constraints with V that have one 
unassigned variable left

3. For GAC we initialize the GAC queue with all constraints containing V.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Just 
    check fully instantiated constraints.
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
    Do FC propagation. Check constraints that have exactly one uninstantiated
    variable in their scope, and prune appropriately. If newVar is None, 
    forward check all constraints. Otherwise only check constraints 
    containing newVar.
    '''
    # TODO! IMPLEMENT THIS!
    pruned = []
    
    if newVar: #check constraints containing newVar
        constraints = csp.get_cons_with_var(newVar)
    else: #check all constraints
        constraints = csp.get_all_cons()

    #loop through list of constraints
    for c in constraints: #find ones that have only 1 unassigned var
        
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
                    #append var's assigned value to vals
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
                    
                if v.cur_domain_size() == 0: #dead end reached
                    return False, pruned

    return True, pruned

def prop_GAC(csp, newVar=None):
    '''
    Do GAC propagation. If newVar is None we do initial GAC enforce 
    processing all constraints. Otherwise we do GAC enforce with constraints
    containing newVar on GAC Queue.
    
    note: CSP is GAC iff all constraints are GAC.
    constraint is GAC iff it's GAC w/r/t each var in scope.
    constraint is GAC w/r/t a var iff for every value of V_i exist values that
    satisfy C.
    '''

    # TODO! IMPLEMENT THIS!
    pruned = []
    
    if newVar: #check constraints containing newVar
        constraints = csp.get_cons_with_var(newVar)
    else: #check all constraints
        constraints = csp.get_all_cons()

    #find constraints whose scope contains v
    for c in constraints:
        for v in c.get_scope():
        
            #loop through list of [vals in current domain of v]
            for d in v.cur_domain():

                #test if (var, val) pair has supporting tuple in c
                if not c.has_support(v, d): #prune d from current domain (of v)
                    
                    #if d is in current domain (of v) && v not yet pruned
                    if (v.in_cur_domain(d)) and ((v, d) not in pruned):
                        v.prune_value(d)
                        pruned.append((v, d))
                
                if v.cur_domain_size() == 0: #dead end reached
                    return False, pruned

    return True, pruned

