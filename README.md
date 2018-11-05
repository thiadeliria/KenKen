# KenKen
A CSP (constraint satisfaction problem) implementation to solve a [KenKen puzzle](https://www.kenkenpuzzle.com).
The puzzle board and its constraints are defined as CSP models in kenken_csp.py. 

Two constraint propagators are implemented in propagators.py:
* Forward Checking
* Generalised Arc Consistence

Additionally, the following heuristics are implemented in heuristics.py:
* Minimum-Remaining Value (MRV) heuristic
* Degree heuristic
* Least-Constraining Value (LCV) heuristic


## Table of Contents
* [How to Play KenKen](https://github.com/thiadeliria/KenKen#how-to-play-kenken)
    * [Rules](https://github.com/thiadeliria/KenKen#rules)
* [Constraint Satisfaction Problems (CSPs)](https://github.com/thiadeliria/KenKen#csps)
* [Constraint Propagation](https://github.com/thiadeliria/KenKen#constraint-propagation)
    * [Forward Checking](https://github.com/thiadeliria/KenKen#forward-checking)
         * [Search Space](https://github.com/thiadeliria/KenKen#search-space)
    * [Generalised Arc Consistence](https://github.com/thiadeliria/KenKen#generalised-arc-consistence)
        
## How to Play KenKen
KenKen (also known as Kashikoku-Naru-Puzzle or 賢くなるパズル) is a puzzle game designed to improve your math skills. Similar to Sudoku, the objective is to fill an *n* × *n* grid of cells with digits 1 to *n*. For example, here is a 3×3 grid.

<p align="center">
<img src="https://github.com/thiadeliria/KenKen/blob/master/images/example.png" width="230" title="blank KenKen puzzle"/>
</p>

A KenKen board contains groups of cells called *cages*, which are outlined in bold. The board above has 5 cages.

Each cage contain a *target* and, optionally, an *operation*. Those are the little numbers and symbols in the corner of the cages. A target is an integer. An operation might be addition, subtraction, multiplication, or division. We must fill in the cages with digits that combine via the given operation, in some order, to produce the target value. 

For example, there are two single-cell cages that read "3" - which means 3 is the target and solution. As for the three-cell cage in the lower right grid, "4×" means that the three digits must produce 4 when all three are multiplied, such as in 1×2×2.

### Rules:
* Each digit appears only once in a row
* Each digit appears only once in a column
* In a cage, digits combine via the given operation to produce the given target

The solution:
<p align="center">
<img src="https://github.com/thiadeliria/KenKen/blob/master/images/example_sol.png" width="230" title="KenKen puzzle solution"/>
</p>

## CSPs
Constraint satisfaction problems (CSPs) define a problem by representing states in a structured, uniform way. A CSP consists of:

* a set of **variables**; - 
* each of which has a **domain** of possible **values**; and -
* a set of **constraints** that specifies the valid combinations of values we may assign to variables. 

A solution to a CSP is a complete assignment of values to variables that satisfies all the constraints (=is consistent). The strategy of CSPs is to eliminate parts of the search space by identifying value assignments that violate constraints.

<p align="center">
<img src="https://github.com/thiadeliria/KenKen/blob/master/images/example_vars.png" width="230" title="KenKen puzzle with variables"/>
</p>

In this problem, we have 9 variables *V11* to *V33*, each representing the value of a cell on the board. Each variable has a domain of {1,2,3}, meaning it can take on a value of 1, 2, or 3. A state consists of a filled-in board. A solution is found when each variable is assigned a value that satisfies the constraints. We can get the constraints from the rules of KenKen:

|   | Rule                                                                          | Constraint |
|---|-------------------------------------------------------------------------------|------------|
| 1 | Each digit appears only once in a row                                         | *V11≠V12≠V13, V21≠V22≠V23, V31≠V32≠V33* |
| 2 | Each digit appears only once in a column                                      | *V11≠V21≠V31, V12≠V22≠V32, V13≠V23≠V33* |
| 3 | In a cage, digits combine via the given operation to produce the given target | *V11÷V12*=2 or *V12÷V11*=2, *V13*=3, *V21-V22*=\|2\|, *V31*=3, *V23×V32×V33*=4 |


## Constraint Propagation
We apply propagation to detect possible failures in future value assignments during search. By "looking ahead" at unassigned variables, we can eliminate constraint-incompatible values. Once we find assignments that violate a constraint, we remove or "prune" those values from their corresponding domains.

### Forward Checking
Implemented as `prop_FC` in propagators.py. The strategy is to check - as we fill in cells and eliminate unwanted values - the CSP's constraints that have one unassigned variable left in its scope. We walk through the forward checking process below. At each step, the domain of each variable, *i.e.*, {1 2 3}, is updated in its corresponding cell.

| Step | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Assignment&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Board&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Explanation |
|:-:|:---:|:---:|--------------------------|
| 00 | | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc00.png" title="Forward checking step 00"/> | Empty puzzle board.
| 01 | *V11*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc01p.png" title="Forward checking step 01"/> | We pick an unassigned variable, *V11*, and try assigning a value in its domain. Then we check the constraints involving *V11* and one other unassigned variable, pruning the values that falsify those constraints. Given *V11*=1, *e.g.*, *V12*=3 violates the cage constraint over *V11* and *V12*, so we remove 3 from *V12*'s domain.
| 02 | *V12*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc02p.png" title="Forward checking step 02"/> | Only one value is left in *V12*'s domain. We assign *V12*:=2 and prune appropriately from unassigned variables in the scope of constraints involving *V12*.
| 03 | *V13*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc03p.png" title="Forward checking step 03"/> | Similarly, we assign *V13*=3.
| 04 | *V21*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc04p.png" title="Forward checking step 04"/> | After doing *V21*:=2, we check relevant constraints. A constraint that includes *V21* and one unassigned variable is the cage constraint over *V21* and *V22*. Neither *V22*=1 or *V22*=3 satisfies *V21-V22*=\|2\|, so we get a Domain Wipe-Out (DWO). We have to backtrack and unassign the value that led us to DWO.
| 05 | *V21*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc05p.png" title="Forward checking step 05"/> | Instead of *V21*:=2 we assign *V21*:=3 (and remove 2 from its domain).
| 06 | *V22*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc06p.png" title="Forward checking step 06"/> | 
| 07 | *V23*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc07p.png" title="Forward checking step 07"/> | 
| 08 | *V31*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc08p.png" title="Forward checking step 08"/> | *V31*'s single-cell cage has target 3. Assigning it 2 falsifies this constraint. We hit another DWO. This time we have to backtrack further, restoring pruned values so that we can find a solution that leaves 3 in the domain of *V31*.
| 09 | *V11*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc09p.png" title="Forward checking step 09"/> | The backtrack brings us back to step 1. We know now that *V11*:=1 doesn't lead to a solution, so we try *V11*:=2.
| 10 | *V12*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc10p.png" title="Forward checking step 10"/> | 
| 11 | *V13*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc11p.png" title="Forward checking step 11"/> | 
| 12 | *V21*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc12p.png" title="Forward checking step 12"/> | 
| 13 | *V22*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc13p.png" title="Forward checking step 13"/> |
| 14 | *V23*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc14p.png" title="Forward checking step 14"/> |
| 15 | *V31*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc15.png" title="Forward checking step 15"/> | This value assignment leads to no prunings.
| 16 | *V32*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc16.png" title="Forward checking step 16"/> |
| 17 | *V33*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc17.png" title="Forward checking step 17"/> | Solution found.

#### Search Space

<p align="center">
   <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc_searchspace.png" width="340" title="Forward checking search space"/>
</p>

### Generalised Arc Consistence
Implemented as `prop_GAC` in propagators.py. Generalised Arc Consistence (GAC) is concerned with consistency. A CSP is GAC if all its constraints are GAC. A constraint is GAC if there is some combination of values that, when assigned, satisfies the constraint. *i.e.*, If we find a solution that fills in every cell and satisfies all of a KenKen puzzle's row, column, and cage constraints, this puzzle is GAC.

GAC employs propagation to make each arc in a constraint graph consistent. We find inconsistencies and remove them by pruning the offending values from the domains of variables. Values that are arc-inconsistent do not constitute a solution, so we eliminate them altogether.

| Step | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Assignment&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Board&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Explanation |
|:-:|:---:|:---:|--------------------------|
| 00 | | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac00.png" title="GAC step 00"/> | Empty puzzle board.
| 01 | *V11*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac01p.png" title="GAC step 01"/> | We prune inconsistent values from domains of variables in the scopes of constraints over *V11*. Then we consider the constraints C' over those affected variables and prune the variables involved in C'.
| 02 | *V11*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac02p.png" title="GAC step 02"/> | 
| 03 | *V12*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac03.png" title="GAC step 03"/> | 
| 04 | *V13*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac04.png" title="GAC step 04"/> | 
| 05 | *V21*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac05.png" title="GAC step 05"/> | 
| 06 | *V22*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac06.png" title="GAC step 06"/> | 
| 07 | *V23*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac07.png" title="GAC step 07"/> | 
| 08 | *V33*:=3 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac08.png" title="GAC step 08"/> | 
| 09 | *V32*:=2 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac09.png" title="GAC step 09"/> | 
| 10 | *V33*:=1 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/gac10.png" title="GAC step 10"/> | 
