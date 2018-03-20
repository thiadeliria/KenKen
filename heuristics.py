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
    A variable ordering heuristic that chooses the next variable to
    be assigned according to the Degree heuristic (DH). ord_dh returns
    the variable that is involved in the largest number of constraints
    on other unassigned variables.
    '''
    # TODO! IMPLEMENT THIS!
    count = {} #count[var] = no. of links to unasg'd vars across 
                #all constraints
    
    #loop through list of [unassigned vars] in the CSP
    vars = csp.get_all_unasgn_vars()
    for v in vars:
        
        #add v to dictionary as key
        count[v] = 0
    
        #loop through list of [all constraints] in the CSP with v
        for c in csp.get_all_cons_with_var(v):
        
            #if constraint c has unassigned vars
            if c.get_n_unasgn() != 0:

                #consider all unasgn'd vars that aren't v
                for uv in c.get_unasgn_vars():
                    if uv != v:
                        #increment v's count by 1
                        count[v] += 1

    #operator.itemgetter fetches dict key w/greatest value
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
    vars = csp.get_all_unasgn_vars() #list of [unassigned vars] in CSP
    
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
    A value heuristic that, given a variable, chooses the value to be 
    assigned according to the Least-Constraining-Value (LCV) heuristic.
    val_lcv returns a list of values. The list is ordered by the value
    that rules out the fewest values in the remaining variables (i.e., 
    the variable that gives the most flexibility later on) to the value
    that rules out the most.
    '''
    # TODO! IMPLEMENT THIS!
    vals = []
    count = {} #count[val] = no. of resulting neighbour prunes
        
        # #add v to dictionary as key
        # count[v] = 0
    
    #loop through list of [all constraints] in the CSP with var
    for c in csp.get_all_cons_with_var(var):
    
        #if constraint c has unassigned vars besides var
        if c.get_n_unasgn() > 1:

            #count no. of values in all neighbour vars' domains
            sum = 0
            for nbr in c.get_unasgn_vars():
                if nbr != var:
                    sum += nbr.cur_domain_size()

            for possval in var.cur_domain():

                #assign it to var
                var.assign(possval)

                #count new no. of values in all neighbours' domains
                sum_new = 0
                for nbr in c.get_unasgn_vars():
                    if nbv != var:
                        sum_new += nbr.cur_domain_size()

                #add no. of prumes to count{}
                count[possval] = sum - sum_new

                var.unassign()

    #sort count by ascending value, store in **LIST** count_ordered
    count_ordered = sorted(count.items(), key=operator.itemgetter(1)) 
    #append count elements vals
    for (k,v) in count_ordered:
        vals.append(k)

    return vals