# Uberdoku solver

Near my house, there is a geocache that has an uberdoku (16x16 sudoku) that must be solved in order to progress the puzzle.

Naturally, the correct solution is to solve this with constraint programming.

## Dependencies
* Python 3.7
* ORTools
* numpy

## Inputs
* input.csv of the 16x16 grid

## Acknowledgements
Thank you jdevor for the geocache puzzle, pintowar for the ORtools tutorial. and google for ORtools. :)

## Notes
The puzzle I wanted to solve was coded with character 0-F, but my test case was 1-G. So right now it will work on the 0-F case but not the 1-G codes. D'oh.
