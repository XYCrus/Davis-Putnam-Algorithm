# Davis-Putnam Algorithm Implementation

This project implements the Davis-Putnam algorithm to solve variations of the peg game. It includes a suite of three main programs that work together to translate a peg game board into a set of logical clauses, solve these clauses using the Davis-Putnam procedure, and then interpret the solution into a series of moves that solve the original peg game.

## Source Files

The project is organized into three primary Python scripts under the `source` directory:

- `DP.py`: Implements the Davis-Putnam procedure. It accepts a set of clauses as input and returns either a satisfying valuation or indicates that the clauses cannot be satisfied.
- `FrontEnd.py`: Acts as a front end, converting a geometric layout of a board and a starting state into a set of clauses for `DP.py`.
- `BackEnd.py`: Serves as a back end, transforming the output from `DP.py` into a solution for the original problem.

## Input / Output Specifications

All programs read their input from and write their output to text files. The expected input format is as follows:

- **First line**: Specifies the number of holes and identifies the hole that is empty at the start.
- **Subsequent lines**: Represent the puzzle configuration as a series of triples. Each line contains three numbers corresponding to holes that align in a row.

A sample input file, `FrontEndInput.txt`, is provided in the `data` directory and serves as the default input.

## Usage Instructions

To use these programs, follow the steps below from your terminal or command line interface:

1. Navigate to the `source` directory:
```
cd source
```
2. Run the `FrontEnd.py` script:
```
python FrontEnd.py
```
3. Execute the `DP.py` script:
```
python DP.py
```
4. Finally, run the `BackEnd.py` script:
```
python BackEnd.py
```


For custom input and output paths, append `--InputFilePath "YourInputFilePath.txt"` and `--OutputFilePath "YourOutputFilePath.txt"` to the commands for any of the three Python programs. If not specified, the default paths under the `/data` directory are used.

