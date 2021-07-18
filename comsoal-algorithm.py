# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 23:52:04 2021

@author: busra
"""

"""COMSOAL ASSEMBLY LINE BALANCING"""
# %% Preparing the data to algorithm
import random

file = open("data/BUXEY.IN2", "r")  # Read file
C = int(input("Enter the cycle time"))  # get cycle time as an input

# assign all rows in the file to a list
all_data = [row.split("\n")[0] for row in file]
# first row in file represents the number of tasks
number_of_tasks = int(all_data[0])
time_of_tasks = [int(all_data[row]) for row in range(
    1, number_of_tasks+1)]  # add time of tasks to a list

# add precedence relations in form "i,j" to a list. It will look like [['1', '2'], ['1', '5'], ['1', '7'], ['1', '10'],...]
pre_relations = [all_data[row].split(",") for row in range(
    number_of_tasks+1, len(all_data)-1)]

# create a list that precedence relations and number of relations for each task
precedences = []
num_of_pre = []
for task in range(1, number_of_tasks+1):
    tasks = [task]
    pre_of_task = [int(pre[0]) for pre in pre_relations if int(pre[1]) == task]
    # add number of precedence relations of a task to a list
    temp = [task,len(pre_of_task)]
    num_of_pre.append(temp)
    tasks.insert(1, pre_of_task)
    # list of precedences of tasks  [[1, []], [2, [1]], [3, [2,1]],...]
    precedences.append(tasks)
    
# %% ALGORITHM
n = int(input("How many times do you want the algorithm to be repeated?"))
for line in range(n):
    A = num_of_pre.copy()
    stations = {}
    station = 1
    assign_counter = 0
    assembly_line_time = 0
    time_of_stations = []  # a list that includes total time of stations

    while assign_counter < number_of_tasks:  # all tasks has to assign a station

        # Initially, the station time starts with 0 because the station has no any tasks yet.
        station_time = 0
        station_tasks = []  # a list that includes tasks of the relevant station

        while station_time <= C:  # total station time can't exceed the cycle time

            # check precedence relations. If a task has no pre then assign task to list B
            B = [i[0] for i in A if i[1] == 0]
            # If the cycle time doesn't exceed when add the task to the station
            F = [task for task in B if station_time + time_of_tasks[task-1] <= C]
                # assign task to list F.

            if F == []:  # if F is empty then there is no tasks to assign, new station
                assembly_line_time = assembly_line_time + station_time  # total time of line
                time_of_stations.append(station_time)
                # calculate remaining time of station
                station_remain_time ="empty time of station:"+str((C - station_time))  # istasyon kalan süresinin hesaplanması
                station_time = "total time of station:" + str(station_time)
                station_tasks.append([station_time,station_remain_time])
                stations[station] = station_tasks
                station = station + 1  # open new station
                break
            else:
                # choise a task from F randomly
                chosen_task = random.choice(F)
                for task in range(number_of_tasks):
                    if chosen_task in precedences[task][1]:
                        # reduce the number of precedence relations of task by one
                        A[task][1] = A[task][1] - 1
                A[chosen_task-1][1] = "used"  # mark the chosen task
                station_time = station_time + time_of_tasks[chosen_task-1]  # calculate station time
                station_tasks.append(chosen_task)  # add chosen task to station
                assign_counter = assign_counter + 1  # assign is done
    #update number of precedences relations 
    num_of_pre = []
    for task in range(number_of_tasks):
        temp = [task+1, len(precedences[task][1])]
        num_of_pre.append(temp)

    print("."*100)
    print("ASSEMBLY LINE {}".format(line+1))
    print("."*100)
    print("Number of Assigned task:",assign_counter)
    for i in range(1,len(stations)+1):
        print("Station {}:".format(i),stations.get(i)) #show the stations orderly