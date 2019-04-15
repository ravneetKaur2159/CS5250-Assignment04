'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):

    # Initialization
    schedule = []
    RR_process_list = process_list.copy()
    current_wait_queue = []
    count = 0
    waiting_time = 0
    current_process_index = 0
    running_queue = []
    running_queue_timestamp = []
    running_queue_timestamp.append(0)
    process_killed = False
    indices_added_till_now = None

    while count < len(RR_process_list):
        current_wait_queue, indices_added_till_now, running_queue_timestamp = RR_wait_queue_creation(current_wait_queue, RR_process_list,
                                                                                          current_process_index, running_queue_timestamp,
                                                                                          process_killed, indices_added_till_now)
        process_killed = False

        if len(current_wait_queue) == 0:
            average_waiting_time = waiting_time / float(len(process_list))
            return schedule, average_waiting_time
        current_process_index = current_wait_queue[0]
        current_process = RR_process_list[current_process_index]
        current_wait_queue.pop(0)
        unique_item = False
        if current_process_index not in running_queue:
            unique_item = True

        running_queue.append(current_process_index)
        print((running_queue_timestamp[-1], current_process.id))
        schedule.append((running_queue_timestamp[-1], current_process.id))

        if current_process.burst_time <= time_quantum:
            running_queue_timestamp.append(running_queue_timestamp[-1] + current_process.burst_time)
            current_process.burst_time = 0
            count = count +1
            process_killed = True
        else:
            running_queue_timestamp.append(running_queue_timestamp[-1] + time_quantum)
            current_process.burst_time = current_process.burst_time - time_quantum


        # Added for the first time
        if unique_item:
            waiting_time = waiting_time + (running_queue_timestamp[-2] - current_process.arrive_time)
            unique_item = False

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def RR_wait_queue_creation(current_wait_queue, RR_process_list, current_process_index,
                           running_queue_timestamp, process_killed, indices_added_till_now):
    # First run - process now added to wait queue
    if running_queue_timestamp[-1] == 0:
        current_wait_queue.append(current_process_index)
        indices_added_till_now = 0
    
    else:
        # Adding processes in queue
        for process_indices in range(current_process_index, len(RR_process_list)):
            x = process_indices + 1
            if  RR_process_list[x].arrive_time <= running_queue_timestamp[-1] and x not in current_wait_queue and x >= indices_added_till_now:
                current_wait_queue.append(x)
                indices_added_till_now = x if indices_added_till_now < x else indices_added_till_now

            else:
                if not process_killed:
                    current_wait_queue.append(current_process_index)
                break

    return current_wait_queue, indices_added_till_now, running_queue_timestamp


def SRTF_scheduling(process_list):
    return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    #for process in process_list:
        #print (process)
    print ("simulating FCFS ----")
    #FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    #write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    #write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    #write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])