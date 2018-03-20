'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy
#custom imports
import operator

def ord_dh(csp):
    '''
    A variable ordering heuristic that chooses the next variable to be assigned
    according to the Degree heuristic (DH). ord_dh returns the variable that is
    involved in the largest number of constraints on other unassigned variables.
    
    consider using csp.get_cons_with_var(v)?
    '''
    # TODO! IMPLEMENT THIS!
    count = {} #count[var] = # of constraints-with-unasgd-vars involving var
    
    #loop through list of [unassigned vars] in the CSP
    vars = csp.get_all_unasgn_vars()
    for v in vars:
        
        #add v to dictionary as key
        count[v] = 0
    
        #loop through list of [all constraints] in the CSP
        for c in csp.get_all_cons():
        
            #if constraint c has unassigned vars
            if c.get_n_unasgn() != 0:
                
                #check if our var is in constraint c's scope
                if v in c.get_scope():
                    
                    #increment v's count by 1
                    count[v] += 1

    #operator.itemgetter (imported) fetches dict key w/greatest value
    dh_var = max(count.items(), key=operator.itemgetter(1))[0]

    return dh_var

def ord_mrv(csp):
    '''
    A variable ordering heuristic that chooses the next variable to be
    assigned according to the Minimum-Remaining-Value heuristic.
    ord_mrv returns the variable with the most constrained current
    domain (i.e., the variable with the fewest legal values).
    '''
    # TODO! IMPLEMENT THIS!
    vars = csp.get_all_unasgn_vars() #list of [unassigned vars] in the CSP
    
    #assign first var in vars to mrv_var
    mrv_var = vars[0]
    min_domain_size = mrv_var.cur_domain_size()
    
    #loop through rest of vars
    for v in vars:
        if v.cur_domain_size() < min_domain_size:
            mrv_var = v #v is the var with the smallest domain
            min_domain_size = v.cur_domain_size()

    return mrv_var

def val_lcv(csp, var):
    '''
    A value heuristic that, given a variable, chooses the value to be assigned
    according to the Least-Constraining-Value (LCV) heuristic. val_lcv
    returns a list of values. The list is ordered by the value that rules out
    the fewest values in the remaining variables (i.e., the variable that gives
    the most flexibility later on) to the value that rules out the most.
    
    choose value that rules out the fewest values for neighbouring vars in
    the constraint graph

    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index,
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.)
    
    The best value, according to LCV, is the one that rules out the fewest domain values in other
    variables that share at least one constraint with var.
    
    examine vals from var's current domain.
    if var=val, how many neighbourvars' values are eliminated?
    (neighbour var = var that shares a constraint with var)
    keep track of # of (domain values in neighbour vars) that var rules out
    '''
    # TODO! IMPLEMENT THIS!
    vals = []
    count = {} #count[var] = # of neighbouring-vars' values ruled out
    
    #loop through list of [values in var's current domain]
    for val in var.cur_domain():

        #add val to dictionary as key
        count[val] = 0

        #loop through list of [constraints containing var]
        for c in csp.get_cons_with_var(var):
            
            #loop through neighbouring variables
            for neighbour in c.get_scope():
                
                #if neighbour is unassigned and is not var
                if ((neighbour != var) and
                   (neighbour in csp.get_all_unasgn_vars())):
    
                    #if (var, v) has no supporting tuple in c
                    if not c.has_support(var, val):
                        
                        #increment v's count by 1
                        count[val] += 1

    #sort count by ascending value, store in **LIST** count_ordered
    count_ordered = sorted(count.items(), key=operator.itemgetter(1))
    #append count elements vals
    for (k,v) in count_ordered:
        vals.append(k)

    return vals















