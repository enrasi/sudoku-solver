# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A:
![alt tag](https://raw.githubusercontent.com/enrasi/sudoku-solver/master/content/naked_twins_1.JPG)
![alt tag](https://raw.githubusercontent.com/enrasi/sudoku-solver/master/content/naked_twins_2.JPG)

As shown in above figures digit 1 and 5 are only allowed in shown boxes. So we can apply contraint propagation and eliminate any 1 or 5 in the group. 

Second figure shows a special case where we can eliminate 1 and 5 from two groups.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:
![alt tag](https://raw.githubusercontent.com/enrasi/sudoku-solver/master/content/diagonal.JPG)
As shown in the figure if one digit is present in the diagonal it can't be presented in other locations in the diagonal. So we use this constraint to solve a diagonal sudoku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.