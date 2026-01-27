# BubbleSort.py

Quick README for the `BubbleSort.py` script in this folder.

## Overview

`BubbleSort.py` implements an optimized bubble sort that sorts a list of integers
in descending order. The script reads integers from `dataset.txt` (one number per line),
sorts them, and prints the sorted list and the time taken.

## Requirements

- Python 3.x

## Usage

From the repository root run:

```bash
python Prelim-Lab-Work1/BubbleSort.py
```

Or change into the folder and run:

```bash
cd Prelim-Lab-Work1
python BubbleSort.py
```

## Input

`dataset.txt` — plain text file with one integer per line. Blank lines are ignored.

## Output

The script prints:
- Number of elements loaded
- Sorted list in descending order
- Time spent performing the sort (in seconds)

Example output (abbreviated):

```
Loaded 100 numbers from dataset.txt

Starting Bubble Sort (Descending Order)...

============================================================
RESULTS
============================================================
Total elements sorted: 100

All sorted data (descending order):
[...sorted numbers...]
Time spent: 0.012345 seconds
============================================================
```

## Notes

- The implementation uses an early-exit optimization: if no swaps occur during a pass,
  sorting stops early.
- To sort a different file, update the `dataset_file` variable in the script or modify
  the script to accept a command-line argument.
