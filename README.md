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
* [Heuristics](https://github.com/thiadeliria/KenKen#heuristics)
        
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
Implemented as `prop_FC` in propagators.py. The strategy is to check - as we fill in cells and eliminate unwanted values - the CSP's constraints that have one unassigned variable left in its scope. We comb through the forward checking process below. At each step, the domain of each variable, *i.e.*, {1 2 3}, is updated in its corresponding cell.

| Step | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Assignment&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pruning&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Explanation |
|---:|:---:|:---:|--------------------------|
| 00 |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc00.png" width="180" title="Forward checking step 00"/> | | Empty puzzle board.
| 01 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc01.png" width="180" title="Forward checking step 01"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc02.png" width="180" title="Forward checking step 01"/> | The constraint *V13*=3 has only one unassigned variable (*V13*). We do *V13*:=3. From *V11≠V12≠V13* we get *V11≠V13* and *V12≠V13*, both of which are now constraints with only one unassigned variable. Since *V13* is now 3, we can remove 3 from the domains of *V11* and *V13*. Given the non-equal column constraints, we do the same for variables *V23* and *V33*.
| 02 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc03.png" width="180" title="Forward checking step 02"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc04.png" width="180" title="Forward checking step 02"/> | Similarly, we assign *V31*:=3 and remove some values from the domains of *V31*'s row- and column-neighbours.
| 03 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc05.png" width="180" title="Forward checking step 03"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc06.png" width="180" title="Forward checking step 03"/> | No constraints currently have one unassigned variable, so we pick one, *V11*, and assign a value - 1 - in its domain.
| 04 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc07.png" width="180" title="Forward checking step 04"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc08.png" width="180" title="Forward checking step 04"/> | *V11≠V12* now has only one unassigned variable - *V12*. The only possible value in its domain is 2.
| 05 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc09.png" width="180" title="Forward checking step 05"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc10.png" width="180" title="Forward checking step 00"/> | From the non-equal column constraints, we get the constraints *V11≠V21* and *V21≠V31*, which give *V21*=2.
| 06 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc11.png" width="180" title="Forward checking step 06"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc12.png" width="180" title="Forward checking step 06"/> | We pick a value, 1, for *V22* from its domain. It follows that its neighbours, *V23* and *V32* have empty domains. We hit Domain Wipe-Out (DWO), so we step back.
| 07 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc13.png" width="180" title="Forward checking step 07"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc14.png" width="180" title="Forward checking step 07"/> | Instead of assigning 1, we assign 3 to *V22*. This falsifies the cage constraint *V21-V22*=|2|, so we have to step back further.
| 08 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc15.png" width="180" title="Forward checking step 08"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc16.png" width="180" title="Forward checking step 08"/> | We try assigning 2 to *V11*.
| 09 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc17.png" width="180" title="Forward checking step 09"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc18.png" width="180" title="Forward checking step 09"/> | We choose a value from *V12*'s domain.
| 10 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc19.png" width="180" title="Forward checking step 10"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc20.png" width="180" title="Forward checking step 10"/> | Now we choose a value from *V21*'s domain.
| 11 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc21.png" width="180" title="Forward checking step 11"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc22.png" width="180" title="Forward checking step 11"/> | Now we choose a value from *V22*'s domain. We get DWO again, so we backtrack and try another value.
| 12 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc23.png" width="180" title="Forward checking step 12"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc24.png" width="180" title="Forward checking step 12"/> | We try assigning *V22*:=3.
| 13 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc25.png" width="180" title="Forward checking step 13"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc26.png" width="180" title="Forward checking step 13"/> |
| 14 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc27.png" width="180" title="Forward checking step 14"/> |<img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc28.png" width="180" title="Forward checking step 14"/> |
| 15 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc29.png" width="180" title="Forward checking step 15"/> | |
| 16 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc30.png" width="180" title="Forward checking step 16"/> | |
| 17 | <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc31.png" width="180" title="Forward checking step 17"/> | | Solution found.

#### Search Space

<p align="center">
   <img src="https://github.com/thiadeliria/KenKen/blob/master/images/fc_searchspace.png" width="340" title="Forward checking search space"/>
</p>

### Generalised Arc Consistence
Implemented as `prop_GAC` in propagators.py. Generalised Arc Consistence (GAC) is concerned with consistency. A CSP is GAC if all its constraints are GAC. A constraint is GAC if there is some combination of values that, when assigned, satisfies the constraint. *e.g.*, If we find a solution that fills in every cell and satisfies all of a KenKen puzzle's row, column, and cage constraints, this puzzle is GAC.

GAC employs propagation to make each arc in a constraint graph consistent. We find inconsistencies and remove them by pruning the offending values from the domains of variables. Since these values are arc-inconsistent, they do not constitute a solution, so we eliminate them altogether.

## Heuristics
