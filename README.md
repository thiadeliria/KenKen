# KenKen
A CSP (constraint satisfaction problem) implementation to solve a [KenKen puzzle](https://www.kenkenpuzzle.com).
The puzzle grid and its constraints are defined in kenken_csp.py using three different CSP models. 

Two constraint propagators are implemented in propagators.py:
* Forward Checking
* Generalised Arc Consistence

Additionally, the following heuristics are implemented in heuristics.py:
* Minimum-Remaining Value (MRV) heuristic
* Degree heuristic
* Least-Constraining Value (LCV) heuristic


## Table of Contents
* [How to Play KenKen](https://github.com/thiadeliria/KenKen)
    * [Rules](https://github.com/thiadeliria/KenKen#rules)
* [Propagators](https://github.com/thiadeliria/KenKen#propagators)
    * [Forward Checking](https://github.com/thiadeliria/KenKen#forward-checking)
    * [Generalised Arc Consistence](https://github.com/thiadeliria/KenKen#generalised-arc-consistence)
* [Heuristics](https://github.com/thiadeliria/KenKen#heuristics)
        
## How to Play KenKen
KenKen (also known as KenDoku or Mathdoku) is a puzzle game designed to improve your math skills. Similar to Sudoku, the objective is to fill in an *n* × *n* grid of cells with digits 1 to *n*. A KenKen grid outlines *n* -sized groups of cells called ***cages*** that contain a ***target*** and, optionally, an ***operation***. A target is an integer. An operation might be addition, subtraction, multiplication, or division. In a cage, digits 1 to *n* must be combined via the given operation, in some order, to produce the target value.

For example, here is a 3x3 grid with five cages.

<p align="left">
<img src="https://github.com/thiadeliria/KenKen/blob/master/images/example.png" width="300" />
</p> Explanation:

* 3: the target and solution (since this cage is a single cell) is 3
* 2÷: the two digits we fill in must produce 2 when one digit divides the other
* 2-: the two digits must produce 2 when one digit subtracts the other
* 4×: means that the three digits must produce 4 when all three are multiplied 

The solution:
<p align="center">
<img src="https://github.com/thiadeliria/KenKen/blob/master/images/example_sol.png" width="300" />
</p>

### Rules:
* Each digit appears only once in a row
* Each digit appears only once in a column
* Each digit appears only once in a cage 
*


## Propagators

### Forward Checking

### Generalised Arc Consistence

## Heuristics
