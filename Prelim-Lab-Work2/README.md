# LAB.py — Sorting Algorithm Suite

Brief README for the `LAB.py` GUI application in this folder.

## Overview

`LAB.py` is a Tkinter-based GUI that loads a numeric dataset from `dataset.txt` and
provides interactive controls to run three sorting algorithms (Bubble Sort, Insertion Sort,
and Merge Sort). The app displays a data preview, basic statistics, sorted results,
and execution time for each algorithm.

## Requirements

- Python 3.x
- Standard library only (`tkinter`, `time`, `copy`, `tkinter.scrolledtext`)

## Usage

From the repository root run:

```bash
python Prelim-Lab_Work2/LAB.py
```

Or change into the folder and run:

```bash
cd Prelim-Lab_Work2
python LAB.py
```

## Input

Place a file named `dataset.txt` in the same folder. It should contain one integer per line.
Blank lines are ignored. The GUI will attempt to auto-load this file on startup.

## Features

- Clean, dark-themed professional UI for dataset preview and results
- Algorithms: Bubble Sort, Insertion Sort, Merge Sort
- Displays statistics: total, min, max, average, and sum
- Shows execution time and element count after sorting
- Clear results control

## Output

The GUI shows the sorted list in the results panel and updates labels for algorithm name,
execution time, and total elements sorted.

## Notes & Tips

- If `dataset.txt` is missing or contains non-integer lines, the GUI will show an error message.
- To test with a custom file, replace `dataset.txt` or modify the code to accept a filename argument.

## License

Use as-is for learning and demonstration purposes.
