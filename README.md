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
* [How to Play KenKen](https://github.com/thiadeliria/KenKen#how-to-play-kenken)
    * [Rules](https://github.com/thiadeliria/KenKen#rules)
* [Propagators](https://github.com/thiadeliria/KenKen#propagators)
    * [Forward Checking](https://github.com/thiadeliria/KenKen#forward-checking)
    * [Generalised Arc Consistence](https://github.com/thiadeliria/KenKen#generalised-arc-consistence)
* [Heuristics](https://github.com/thiadeliria/KenKen#heuristics)
        
## How to Play KenKen
KenKen (also known as KenDoku or Mathdoku) is a puzzle game designed to improve your math skills. Similar to Sudoku, the objective is to fill in an *n* × *n* grid of cells with digits 1 to *n*. For example, here is a 3x3 grid.

<p align="center">
<img src="https://github.com/thiadeliria/KenKen/blob/master/images/example.png" width="300" />
</p>

A KenKen grid contains *n* -sized groups of cells called ***cages***, which are outlined in bold. The grid above has 5 cages.

Each cage contain a ***target*** and, optionally, an ***operation***. Those are the little numbers and symbols in the corner of the cages. A target is an integer. An operation might be addition, subtraction, multiplication, or division. We must fill in the cages with digits that combine via the given operation, in some order, to produce the target value. For example, there are two single-cell cages in the upper right and lower left corners. Each cage reads "3" - which means 3 is the target and solution (since each cage is a single cell). As for the three-cell cage in the lower right grid, "4×" means that the three digits must produce 4 when all three are multiplied, such as in 1×2×2.

### Rules:
* Each digit appears only once in a row
* Each digit appears only once in a column
* In a cage, digits combine via the given operation to produce the given target

The solution:
<p align="center">
<img align="right" src="https://github.com/thiadeliria/KenKen/blob/master/images/example_sol.png" width="300" />
</p>

## Propagators

### Forward Checking

### Generalised Arc Consistence

## Heuristics
