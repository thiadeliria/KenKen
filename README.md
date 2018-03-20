# KenKen
A CSP (constraint satisfaction problem) implementation to solve a KenKen puzzle 
(http://thinkmath.edc.org/resource/introducing-kenken-puzzles).
The puzzle grid and its constraints are defined in kenken_csp.py using three different CSP models. 

Two constraint propagators are implemented in propagators.py:
* Forward Checking
* Generalised Arc Consistence

Additionally, the following heuristics are implemented in heuristics.py:
* Minimum-Remaining Value (MRV) heuristic
* Degree heuristic
* Least-Constraining Value (LCV) heuristic
