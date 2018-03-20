'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
import itertools
from cspbase import *


def binary_ne_grid(kenken_grid):
    '''
    A model of a KenKen grid (without cage constraints) built using only
    binary-not-equal constraints for both the row and column constraints.
    
    binary-not-equal constraints: V1!=V2, V1!=V3,...V2!=V1,...Vn!=Vn-1
    '''
    # TODO! IMPLEMENT THIS!
    n = kenken_grid[0][0] #dimension size n gives a n*n board
    
    #---VARIABLES---
    #build domain of possible values
    domain = []
    for i in range(1, n+1): #range goes from 1 to n
        domain.append(i)

    #init variables
    board = [] #list of list of Variable objs (1 list for each row)
    #add Variable for each cell (row * column)
    for row in range(1, n+1):
        vars_row = [] #list of vars
        for column in range(1, n+1):
            #add Variable V{row#}{col#}
            vars_row.append(Variable('V{}{}'.format(row, column), domain))
        board.append(vars_row)

    #---CONSTRAINTS---
    constraints = [] #list of Constraint objs

    #add row constraints between (V11,V12)(V11,V13)...(V12,V13)...(V13,V14)
    i = 0 #keep track of row number
    for row in board:
        for j in range(i, n): #(i+1)~5
            
            #init constraint c with scope
            c = Constraint("C(V{}{},V{}{})".format(i+1, j+1, i+1, j+1), [row[i], row[j]])
            
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of 2-tuples with diff elements
            for t in itertools.permutations(domain, 2):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            
            #add constraint c to constraints[]
            constraints.append(c)

        i += 1 #increment var's index

    #add column constraints between (V11,V21)(V11,V31)...(V21,V31)...(V31,V41)
    i = 0 #keep track of column number
    for column in board:
        for j in range(i+1, n): #(i+1)~5
            
            #init constraint c with scope
            c = Constraint("C(V{},V{})".format(j+1,i+1), [row[j], row[i]])
            
            #build list of satisfying tuples
            sat_tuples = []
            #this generates a list of 2-tuples with diff elements
            for t in itertools.permutations(domain, 2):
                sat_tuples.append(t)
            #add tuples to constraint c
            c.add_satisfying_tuples(sat_tuples)
            
            #add constraint c to constraints[]
            constraints.append(c)
        
        i += 1 #increment var's index

    #---CSP---
    #init csp
    csp = CSP("{}-BinaryKenKen".format(n))

    print("this csp's variables are:\n") #testing
    #add variables to csp
    for row in board:
        for every_var in row:
            csp.add_var(every_var)
            print(every_var.name) #testing

    print("this csp's constraints are:\n") #testing
    #add constraints to csp
    for c in constraints:
        csp.add_constraint(c)
        print(c.name) #testing



    return csp, board

def nary_ad_grid(kenken_grid):
    '''
    A model of a KenKen grid (without cage constraints) built using only
    n-ary all-different constraints for both the row and column constraints.
    '''
    # TODO! IMPLEMENT THIS!
    pass

def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    pass
