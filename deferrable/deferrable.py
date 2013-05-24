#Author: Diego PERINI
#License: Public Domain
#Deferrable server scheduling implementation

import string
import random
from math import fabs
from prime import lcm

#A task instance
class TaskIns(object):

    #Constructor (should only be invoked with keyword parameters)
    def __init__(self, start=None, end=None, priority=None, a_start=None, a_end=None, a_deadline=None, name='Task'):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.budget   = None
        if self.name[:11] == "Deferrable=":
            self.budget = int(self.name[11:])
            self.name = self.name[:10]
        self.a_start    = a_start
        self.a_end      = a_end
        self.a_deadline = a_deadline
        self.id = int(random.random() * 10000)

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    #Allow an instance to use the cpu (aperiodic)
    def a_use(self, usage):
        self.usage += usage
        if self.usage >= self.a_end - self.a_start:
            return True
        return False

    #Consume budget of a deferrable server
    def consume(self, usage):
        if self.budget is None:
            raise Error("This task is not a deferrable server.")
        amount = self.budget - usage
        if amount < 0:
            amount = self.budget
        self.budget -= amount
        return amount
    
    #Default representation (periodic only)
    def __repr__(self):
        budget_text = ""
        if self.budget is not None:
            budget_text = " budget: " + str(self.budget)
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) + budget_text

    #Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

#Special exception for aperiodic tasks
class JumpToPeriodicExecution(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#Task types (templates for periodic tasks)
class TaskType(object):

    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

#Aperiodic release time comparison
def aperiodic_cmp(one, other):
    if one.a_start < other.a_start:
        return -1
    elif one.a_start > other.a_start:
        return 1
    return 0

#Rate monotonic comparison
def tasktype_cmp(self, other):
    if self.period < other.period:
        return -1
    if self.period > other.period:
        return 1
    return 0

#Main
if __name__ == '__main__':
    #Variables
    html_color = { 'Task1':'red', 'Task2':'blue', 'Task3':'green', 'Task4':'aqua', 'Task5':'coral', 'Deferrable':'yellow', 'Empty':'grey', 'Finish':'black'}
    taskfile = open('deferrable_inputs.txt')
    lines = taskfile.readlines()
    task_types = []
    tasks = []
    hyperperiod = []
    aperiodic_tasks = []

    #Allocate task types
    for line in lines:
        #Explode lines
        line = line.split(' ')  
        for i in range (0,4):
            line[i] = int(line[i])

        #Check for name availablity and file format
        if len(line) == 5:
            name = line[4]
        elif len(line) == 4:
            name = 'Task'
        else:
            raise Exception('Invalid deferrable_inputs.txt file structure')

        #Fill task lists
        if int(line[0])>0:
            task_types.append(TaskType(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))
        else:
            aperiodic_tasks.append(TaskIns(a_start=line[1], a_end=int(line[1]) + int(line[2]), a_deadline=line[3], name=name))
        
    #Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(task_type.period)
    hyperperiod = lcm(hyperperiod)

    #Sort types rate monotonic
    task_types = sorted(task_types, tasktype_cmp)
    aperiodic_tasks = sorted(aperiodic_tasks, aperiodic_cmp)

    #Create task instances 
    for i in xrange(0, hyperperiod):
        for task_type in task_types:
            if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = task_type.period
                tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))

    #Html output start
    html = "<!DOCTYPE html><html><head><title>Deferrable Server Scheduling</title></head><body>"

    #Check utilization
    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)
    if utilization > 1:
        print 'Utilization error!'
        html += '<br /><br />Utilization error!<br /><br />'

    #Simulate clock
    clock_step = 1
    for i in xrange(0, hyperperiod, clock_step):
        #Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, priority_cmp)

        #Truncate duplicate servers, only keep latest one (replenishment)
        for p in possible:
            if p.start == i and p.name == "Deferrable":
                for deprecate_server in possible:
                    if deprecate_server.start < i and deprecate_server.name == "Deferrable":
                        tasks.remove(deprecate_server)
                        possible.remove(deprecate_server)
        possible = sorted(possible, priority_cmp)

        #Select task with highest priority
        try:
            on_cpu = possible[0]
            on_def = None

            #If selected task is server, scan aperiodic tasks
            if on_cpu.name == "Deferrable":

                #Scan aperiodic tasks for requests
                for a in aperiodic_tasks:
                    if a.a_start <= i:
                        on_def = a
                        break

                #If request is found, consume server
                if on_def is not None:

                    #Try consuming server, if consumed
                    if on_cpu.consume(clock_step):
                        print on_def.get_unique_name() , " uses the processor. " , 
                        html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color[on_cpu.name] + ';">' + on_def.get_unique_name() + '</div>'
                        if on_cpu.use(clock_step):
                            tasks.remove(on_cpu)
                        if on_def.a_use(clock_step):
                            aperiodic_tasks.remove(on_def)
                            html += '<div style="float: left; text-align: center; width: 10px; height: 20px; background-color:' + html_color['Finish'] + ';"></div>'                            #
                            print "Finish!" ,

                    #If consume fails
                    else:                        
                        tasks.remove(on_cpu)
                        on_cpu = possible[1]
                        raise JumpToPeriodicExecution("")

                #If nothing to do for server
                else:
                    on_cpu = possible[1]
                    raise JumpToPeriodicExecution("")

            #If selected task is a regular periodic task
            else:
                raise JumpToPeriodicExecution("")

        #Cpu is idle
        except IndexError:
            print 'No task uses the processor. '
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color['Empty'] + ';">Empty</div>'
        
        #A periodic task uses the CPU
        except JumpToPeriodicExecution:
            print on_cpu.get_unique_name() , " uses the processor. " ,
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color[on_cpu.name] + ';">' + on_cpu.get_unique_name() + '</div>'            
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                html += '<div style="float: left; text-align: center; width: 10px; height: 20px; background-color:' + html_color['Finish'] + ';"></div>'
                print "Finish!" ,            
        print "\n"

    #Print remaining periodic tasks
    html += "<br /><br />"
    for p in tasks:
        if p.name == "Deferrable":
            continue
        print p.get_unique_name() + " is dropped due to overload!"
        html += "<p>" + p.get_unique_name() + " is dropped due to overload!</p>"

    #Print remaining aperiodic tasks
    html += "<br /><br />"
    for a in aperiodic_tasks:
        print a.get_unique_name() + " is dropped due to overload!"
        html += "<p>" + a.get_unique_name() + " is dropped due to overload!</p>"

    #Html output end
    html += "</body></html>"
    output = open('output.html', 'w')
    output.write(html)
    output.close()
