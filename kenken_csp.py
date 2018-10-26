'''
The following CSP models take as input a KenKen grid, in the form of a 
list of lists.

binary_ne_grid - a model of a KenKen grid (without cage constraints) 
built using only binary-not-equal constraints for both the row and column 
constraints.

nary_ad_grid - a model of a KenKen grid (without cage constraints) built 
using only n-ary all-different constraints for both the row and column 
constraints.

kenken_csp_model - a model built using n-ary all-different constraints for 
the grid and KenKen cage constraints.

All models return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

'''
import itertools
from cspbase import *

def generate_cons_name(t_list):
    '''
    Returns a Constraint name given its scope of variables in a list.
    Helper function for nary_ad_grid.
    Example:
    Input: [V11,V12,V13]
    Output: "C(V11,V12,V13)"
    '''
    n = len(t_list)
    cons_name = "C("
    comma = ","
    close = ")"
    for i in range(0, n): #range goes from 0 to n-1
        if type(t_list[i]) is str:
            cons_name += "V" + t_list[i]
        if type(t_list[i]) is int:
            cons_name += "V" + str(t_list[i])
        else:
            cons_name += t_list[i].name
        if i < n-1: #i is not last index
            cons_name += comma
    cons_name += close

    return cons_name

def generate_tuple_list(var_list, n):
    '''
    Returns list of all possible tuple combinations with no repeated
    elements. Helper function for binary_ne_grid and nary_ad_grid.
    Example:
    Input: ["V11","V12","V13"], 2
    Output: [("V11","V12"), ("V11","V13"), ("V12","V13")]
    '''
    return itertools.combinations(var_list, n)

def check_add(vals, target):
    '''
    Returns True iff values in vals can be added together 
    to give sum target.
    '''
    sum = 0
    for v in vals:
        sum += v
    if sum != target:
        return False
    return True 

def check_sub(vals, target):
    '''
    Returns True iff values in vals can be subtracted
    to give difference target.
    '''
    for perm in itertools.permutations(vals):
        diff = perm[0]
        i = 1
        while (i < len(vals)):
            diff -= perm[i]
            i += 1
        if diff == target:
            return True
    return False

def check_div(vals, target):
    '''
    Returns True iff values in vals can be divided
    to give quotient target.
    '''
    for perm in itertools.permutations(vals):
        quotient = perm[0]
        i = 1
        while(i < len(vals)):
            quotient //= perm[i]
            i += 1
        if quotient == target:
            return True
    return False

def check_mult(vals, target):
    '''
    Returns True iff values in vals can be multiplied together 
    to give product target.
    '''
    product = 1
    for v in vals:
        product *= v
    if product != target:
        return False
    return True 

def generate_vars(domain):
    '''
    Returns list of list variables for a KenKen board with given
    domain. Helper function for binary_ne_grid and nary_ad_grid.
    Example:
    Input: domain = [1, 2, 3]
    Output: [["V11", "V12" ,"V13"], 
             ["V21", "V22" ,"V23"], 
             ["V31", "V32" ,"V33"]]
    '''
    n = len(domain)

    #init variables
    board = []
    #add Variable for each cell (row * column)
    for row in range(1, n+1):
        vars_row = [] #list of vars
        for column in range(1, n+1):
            #add Variable V{row#}{col#}
            vars_row.append(Variable('V{}{}'.format(row, column), domain))
        board.append(vars_row)

    return board

def binary_ne_grid(kenken_grid):
    '''
    A model of a KenKen grid (without cage constraints) built using only
    binary-not-equal constraints for both the row and column constraints.
    '''
    n = kenken_grid[0][0] #dimension size
    
    #---VARIABLES---
    #build domain of possible values
    domain = []
    for i in range(1, n+1): #range goes from 1 to n
        domain.append(i)
    #init variables
    board = []
    #add nxn Variables V{row#}{col#}
    for row in range(1, n+1):
        vars_row = [] #list of vars
        for column in range(1, n+1):
            vars_row.append(Variable('V{}{}'.format(row, column), domain))
        board.append(vars_row)

    #---CONSTRAINTS---
    constraints = []
    #add row constraints
    for row in board:
        for t in generate_tuple_list(row, 2):
            #init constraint c with scope
            c = Constraint("C({},{})".format(t[0].name, t[1].name),
                           [t[0], t[1]])
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of 2-tuples with diff elements
            for t in itertools.permutations(domain, 2):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            #add constraint c to constraints[]
            constraints.append(c)

    #add column constraints
    for i in range(len(domain)): #column num from 0 to n-1
        column = []
        for j in range(len(domain)): #num of rows
            column.append(board[j][i])
        for t in generate_tuple_list(column, 2):
            #init constraint c with scope
            c = Constraint("C({},{})".format(t[0].name, t[1].name),
                       [t[0], t[1]])
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of 2-tuples with diff elements
            for t in itertools.permutations(domain, 2):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            #add constraint c to constraints[]
            constraints.append(c)

    #---CSP---
    #init csp
    csp = CSP("{}-BinaryKenKen".format(n))
    #add variables to csp
    for row in board:
        for every_var in row:
            csp.add_var(every_var)
    #add constraints to csp
    for c in constraints:
        csp.add_constraint(c)

    return csp, board

def nary_ad_grid(kenken_grid):
    '''
    A model of a KenKen grid (without cage constraints) built using only
    n-ary all-different constraints for both the row and column constraints.
    '''
    n = kenken_grid[0][0] #dimension size
    
    #---VARIABLES---
    #build domain of possible values
    domain = []
    for i in range(1, n+1): #range goes from 1 to n
        domain.append(i)
    #init variables
    board = []
    #add nxn Variables V{row#}{col#}
    for row in range(1, n+1):
        vars_row = [] #list of vars
        for column in range(1, n+1):
            vars_row.append(Variable('V{}{}'.format(row, column), domain))
        board.append(vars_row)

    #---CONSTRAINTS---
    constraints = []
    #add row constraints
    for row in board:
        for t in generate_tuple_list(row, n):
            #init constraint c with scope
            cons_name = generate_cons_name(row)
            c = Constraint(cons_name, row)
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of n-tuples with diff elements
            for t in itertools.permutations(domain, n):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            #add constraint c to constraints[]
            constraints.append(c)

    #add column constraints
    #build columns
    for i in range(len(domain)): #column num from 0 to n-1
        column = []
        for j in range(len(domain)): #num of rows
            column.append(board[j][i])
        for t in generate_tuple_list(column, n):
            #init constraint c with scope
            cons_name = generate_cons_name(column)
            c = Constraint(cons_name, column)
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of 2-tuples with diff elements
            for t in itertools.permutations(domain, 2):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)

            #add constraint c to constraints[]
            constraints.append(c)

    #---CSP---
    #init csp
    csp = CSP("{}-aryKenKen".format(n))
    #add variables to csp
    for row in board:
        for every_var in row:
            csp.add_var(every_var)
    #add constraints to csp
    for c in constraints:
        csp.add_constraint(c)

    return csp, board
    
def kenken_csp_model(kenken_grid):
    '''
    A model built using n-ary all-different constraints for the grid and
    KenKen cage constraints.
    '''
    n = kenken_grid[0][0] #dimension size
    
    #---VARIABLES---
    #build domain of possible values
    domain = []
    for i in range(1, n+1): #range goes from 1 to n
        domain.append(i)
    #init variables
    board = []
    #add nxn Variables V{row#}{col#}
    for row in range(1, n+1):
        vars_row = []
        for column in range(1, n+1):
            vars_row.append(Variable('V{}{}'.format(row, column), domain))
        board.append(vars_row)

    #---CONSTRAINTS---
    constraints = []
    
    #add cage constraints
    for cage in kenken_grid[1:len(kenken_grid)]: #ignore the 1st list
        scope = []
        #init scope, target, [operation]
        if len(cage) == 2:
            cell_i = (cage[0] // 10) - 1
            cell_j = (cage[0] % 10) - 1
            scope.append(board[cell_i][cell_j])
            target = cage[1]

            c = Constraint("cage: " + "C(V{}{})".format(cell_i+1,cell_j+1), scope)
            c.add_satisfying_tuples([(target,)]) #list of 1-ele tuple
            constraints.append(c)
            continue #go on to next cage

        for num in range(0, len(cage)-2):
            cell_i = (cage[num] // 10) - 1
            cell_j = (cage[num] % 10) - 1
            scope.append(board[cell_i][cell_j])
        target = cage[-2]
        operation = cage[-1]
    
        cons_name = generate_cons_name(scope)
        # c = Constraint("cage: " + cons_name + ", target = " + str(target), scope)
        c = Constraint("cage: " + cons_name, scope)
        sat_tuples = []
        for t in itertools.product(domain, repeat=len(scope)):
            if operation == 0: #add +
                if check_add(t, target):
                    sat_tuples.append(t)
            elif operation == 1: #sub -
                if check_sub(t, target):
                    sat_tuples.append(t)
            elif operation == 2: #div /
                if check_div(t, target):
                    sat_tuples.append(t)
            elif operation == 3: #mult *
                if check_mult(t, target):
                    sat_tuples.append(t)
        c.add_satisfying_tuples(sat_tuples)
        constraints.append(c)
    
    #add row constraints
    for row in board:
        for t in generate_tuple_list(row, n):
            #init constraint c with scope
            cons_name = generate_cons_name(row)
            c = Constraint("row: " + cons_name, row)
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of n-tuples with diff elements
            for t in itertools.permutations(domain, n):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            #add constraint c to constraints[]
            constraints.append(c)

    #add column constraints
    #build columns
    for i in range(len(domain)): #column num from 0 to n-1
        column = []
        for j in range(len(domain)): #num of rows
            column.append(board[j][i])
        for t in generate_tuple_list(column, n):
            #init constraint c with scope
            cons_name = generate_cons_name(column)
            c = Constraint("column: " + cons_name, column)
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of 2-tuples with diff elements
            for t in itertools.permutations(domain, n):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            #add constraint c to constraints[]
            constraints.append(c)

    #---CSP---
    #init csp
    csp = CSP("{}-KenKen".format(n))
    #add variables to csp
    for row in board:
        for every_var in row:
            csp.add_var(every_var)
    #add constraints to csp
    for c in constraints:
        csp.add_constraint(c)

    return csp, board