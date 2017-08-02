py-common-scheduling-algorithms
===============================
Common scheduling algorithms implemented in Python 2.7


## AUTHOR
Diego Perini, Istanbul Technical University, May 2013


## INTRODUCTION
This folder contains Python 2.7 implementations of the following scheduling algorithms.

* RM: Rate Monotonic
* DM: Deadline Monotonic
* EDF: Earliest Deadline First
* LLF: Least Laxity First
* Deferrable: Deferrable Server
* Sporadic: Sporadic Server

Task execution is simulated via verbose messages. Prepare your tasks using the inputs and modify relevant print lines with your code to apply scheduling.


## FILE STRUCTURE
Each folder contains one main program named after its corresponding algorithm.

`prime.py` is a utility library provided by third parties for mathematical operations.

`tasks.txt` is the input file for RM, DM, EDF and LLF implementations. Its structure is explained below.

`deferrable_inputs.txt` and `sporadic_inputs.txt` files are special input files. They can only contain a single server named after its corresponding algorithm. Task that are set their period 0 (zero) are considered aperiodic and are only executed once. Their structure is explained below.



tasks.txt
=========
    Period1 ReleaseTime1 ExecutionTime1 Deadline1 Taskname1
    Period2 ReleaseTime2 ExecutionTime2 Deadline2 Taskname2
    Period3 ReleaseTime3 ExecutionTime3 Deadline3 Taskname3
    ..
    


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




## HOW TO RUN
In order to run the project, execute the following command in terminal. Replace algorithm name with one of the given implementations (i.e rm.py)

    python path/algorithm_name.py

The result will be shown on standard output. A visual representation will also be rendered in html. Look for `output.html` file in your project folder after each execution. 


## LICENSE
Public Domain

Noob info: Public Domain means you are free to decide what to do with this code. There are absolutely no restrictions regarding copyright, distribution and commercial appliances. Use it as if you have written it.
