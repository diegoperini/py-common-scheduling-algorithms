#########AUTHOR#########
Diego Perini, 040080187, Istanbul Technical University, 2013

#########INTRODUCTION#########
This folder contains Python 2.7 implementations of the following scheduling algorithms.

RM: Rate Monotonic
DM: Deadline Monotonic
EDF: Earliest Deadline First
LLF: Least Laxity First
Deferrable: Deferrable Server
Sporadic: Sporadic Server


#########FILE_STRUCTURE#########
Each folder contains one main program named after its corresponding algorithm.

`prime.py` is a utility library provided by third parties for mathematical operations.



`tasks.txt` is the input file for RM, DM, EDF and LLF implementations. Its structure is explained below.

tasks.txt
=========
Period1 ReleaseTime1 ExecutionTime1 Deadline1 Taskname1
Period2 ReleaseTime2 ExecutionTime2 Deadline2 Taskname2
Period3 ReleaseTime3 ExecutionTime3 Deadline3 Taskname3
..



`deferrable_inputs.txt` and `sporadic_inputs.txt` files are special input files. They can only contain a single server named after its corresponding algorithm. Task that are set their period 0 (zero) are considered aperiodic and are only executed once. Their structure is explained below.

deferrable_inputs.txt
========================================
Period1 ReleaseTime1 ExecutionTime1 Deadline1 Taskname1
Period2 ReleaseTime2 ExecutionTime2 Deadline2 Taskname2
Period3 ReleaseTime3 ExecutionTime3 Deadline3 Taskname3
ServerPeriod ServerRelease ServerExecution ServerDeadline Deferrable=Budget
..

sporadic_inputs.txt
========================================
Period1 ReleaseTime1 ExecutionTime1 Deadline1 Taskname1
Period2 ReleaseTime2 ExecutionTime2 Deadline2 Taskname2
Period3 ReleaseTime3 ExecutionTime3 Deadline3 Taskname3
ServerPeriod ServerRelease ServerExecution ServerDeadline Sporadic=Budget
..


#########HOW_TO_RUN#########
In order to run the project, execute the following command in terminal. Replace algorithm nape with one of the given implementations (i.e rm.py)

python algorithm_name.py

The result will be shown on standard output. A visual representation will also be rendered in html. Look for `output.html` file in your project folder after each execution. 
