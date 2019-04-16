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
    def __init__(self, id, arrive_time, burst_time, index):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.index = index
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d, index %d]'%(self.id, self.arrive_time, self.burst_time, self.index))

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
    process_killed = False
    indices_added_till_now = None
    running_queue_timestamp.append(0)
    prev_process_index = -1
    RR_process_list_not_added = RR_process_list.copy()
    while count < len(RR_process_list):
        current_wait_queue, indices_added_till_now, running_queue_timestamp, RR_process_list_not_added = \
            RR_wait_queue_creation(current_wait_queue, RR_process_list_not_added, RR_process_list, current_process_index, running_queue_timestamp,
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
        if prev_process_index != current_process_index:
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

        prev_process_index = current_process.index

        # Added for the first time
        if unique_item:
            waiting_time = waiting_time + (running_queue_timestamp[-2] - current_process.arrive_time)
            unique_item = False

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def RR_wait_queue_creation(current_wait_queue, RR_process_list_not_added, RR_process_list, current_process_index,
                           running_queue_timestamp, process_killed, indices_added_till_now):
    # First run - process now added to wait queue
    if running_queue_timestamp[-1] == 0:
        current_wait_queue.append(current_process_index)
        indices_added_till_now = 0
        RR_process_list_not_added.pop(current_process_index)
    else:
        # Adding processes in queue
        for process in RR_process_list_not_added:
            if process.arrive_time <= running_queue_timestamp[-1]:
                current_wait_queue.append(process.index)
                indices_added_till_now = process.index if indices_added_till_now < process.index else indices_added_till_now
            elif len(current_wait_queue) == 0 \
                    and RR_process_list_not_added[0].arrive_time > running_queue_timestamp[-1] \
                    and RR_process_list[current_process_index].burst_time == 0:
                current_wait_queue.append(RR_process_list_not_added[0].index)
                indices_added_till_now = RR_process_list_not_added[0].index if \
                    indices_added_till_now < RR_process_list_not_added[0].index else indices_added_till_now
                running_queue_timestamp.append(RR_process_list_not_added[0].arrive_time)
            else:
                if not process_killed:
                    current_wait_queue.append(current_process_index)
                break


        if len(RR_process_list_not_added) == 0 or len(RR_process_list_not_added) == 1:
            if not process_killed:
                current_wait_queue.append(current_process_index)


        for process_index in current_wait_queue:
            process = RR_process_list[process_index]
            if process in RR_process_list_not_added:
                RR_process_list_not_added.remove(process)

    return current_wait_queue, indices_added_till_now, running_queue_timestamp, RR_process_list_not_added


def SRTF_scheduling(process_list):
    SRTF_process_list = process_list.copy()
    schedule = []
    current_wait_queue = []
    count = 0
    waiting_time = 0
    prev_process_index = None
    running_queue_timestamp = 0
    current_process_index_to_be_executed = 0
    running_queue = []
    while count < len(SRTF_process_list):

        current_wait_queue = SRTF_wait_queue_creation(current_wait_queue, SRTF_process_list,
                                                      running_queue_timestamp, current_process_index_to_be_executed)
        current_process_index_to_be_executed = shortest_process_extraction(current_wait_queue, SRTF_process_list)

        if current_process_index_to_be_executed != None:
            SRTF_process_list[current_process_index_to_be_executed].burst_time = SRTF_process_list[current_process_index_to_be_executed].burst_time - 1
            running_queue.append(SRTF_process_list[current_process_index_to_be_executed].id)
            if SRTF_process_list[current_process_index_to_be_executed].burst_time == 0:
                count = count + 1

        running_queue_timestamp = running_queue_timestamp + 1
        if current_process_index_to_be_executed != None and prev_process_index != current_process_index_to_be_executed:
            #print((running_queue_timestamp - 1 , SRTF_process_list[current_process_index_to_be_executed].id))
            schedule.append((running_queue_timestamp - 1 , SRTF_process_list[current_process_index_to_be_executed].id))
        prev_process_index = current_process_index_to_be_executed

        # first run of the process
        if current_process_index_to_be_executed != None:
            unique_elements_current_wait_queue =  list(set(current_wait_queue))
            if running_queue.count(SRTF_process_list[current_process_index_to_be_executed].id) == 1:
                waiting_time = waiting_time + (running_queue_timestamp-1 - SRTF_process_list[current_process_index_to_be_executed].arrive_time)
                #print("waiting time",waiting_time)
            else:
                all_processes_burst_time_over = True
                for processes_index in unique_elements_current_wait_queue:
                    if SRTF_process_list[processes_index].burst_time != 0:
                        all_processes_burst_time_over = False
                        break

                if all_processes_burst_time_over:
                    running_queue = []

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def SRTF_wait_queue_creation(current_wait_queue, SRTF_process_list, running_queue_timestamp, current_process_index):
    # First run - process now added to wait queue
    if running_queue_timestamp == 0:
        current_wait_queue.append(current_process_index)

    else:
        for process in SRTF_process_list:
            if process.arrive_time <= running_queue_timestamp and process.burst_time != 0 :
                current_wait_queue.append(SRTF_process_list.index(process))

    return current_wait_queue


def shortest_process_extraction(current_wait_queue, SRTF_process_list):
    shortest_remaining_time = 99999
    shortest_remaining_time_index = None
    for process_index in current_wait_queue:
        if shortest_remaining_time > SRTF_process_list[process_index].burst_time and SRTF_process_list[process_index].burst_time != 0:
            shortest_remaining_time_index = process_index
            shortest_remaining_time = SRTF_process_list[process_index].burst_time
    return shortest_remaining_time_index


def SJF_scheduling(process_list, alpha):
    count = 0
    total_processes = len(process_list)
    current_wait_queue = []
    current_time = 0
    waiting_time = 0
    schedule = []
    predictive_timings = {}
    shortest_process_index = 0
    predictive_value = 5
    sjf_process_list = process_list.copy()
    transition = []

    for process in sjf_process_list:
        predictive_timings[process.id] = predictive_value

    while count < total_processes:
        if len(current_wait_queue) > 0:
            shortest_process_index = 0
            for process_curr_queue in current_wait_queue[1:]:
                if (predictive_timings[process_curr_queue.id] < predictive_timings[current_wait_queue[shortest_process_index].id]):
                    shortest_process_index = current_wait_queue.index(process_curr_queue)


            # add current_time, process_id of the shortest job, index of the shortest job
            if len(schedule) == 0 or \
                    (len(schedule) > 0 and schedule[len(schedule)-1][2] != (current_wait_queue[shortest_process_index]).index):
                schedule.append([current_time, (current_wait_queue[shortest_process_index]).id, (current_wait_queue[shortest_process_index]).index])
                transition.append((current_time, (current_wait_queue[shortest_process_index]).id))

            current_time = current_time + current_wait_queue[shortest_process_index].burst_time
            current_wait_queue, sjf_process_list = sjf_current_wait_queue_creation(sjf_process_list, current_time, current_wait_queue)
            waiting_time = waiting_time + \
                           (current_time - current_wait_queue[shortest_process_index].arrive_time - current_wait_queue[shortest_process_index].burst_time)

            predictive_timings[current_wait_queue[shortest_process_index].id] = alpha * \
                                                                                current_wait_queue[shortest_process_index].burst_time + \
                                                                                (1 - alpha) * \
                                                                                predictive_timings[current_wait_queue[shortest_process_index].id];
            del current_wait_queue[shortest_process_index]
            count = count + 1
        else:
            current_wait_queue, sjf_process_list = sjf_current_wait_queue_creation(sjf_process_list, current_time, current_wait_queue)
            if len(current_wait_queue) == 0:
                current_time = current_time + 1

    average_waiting_time = waiting_time / float(len(process_list))
    return transition, average_waiting_time

def sjf_current_wait_queue_creation(sjf_process_list, current_time, current_wait_queue):
    for process in sjf_process_list:
        if process.arrive_time <= current_time:
            current_wait_queue.append(process)

    for process in current_wait_queue:
        if process in sjf_process_list:
            sjf_process_list.remove(process)

    return current_wait_queue, sjf_process_list

def read_input():
    result = []
    with open(input_file) as f:
        index = 0
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2]), index))
            index = index + 1
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
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    process_list = read_input()
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    process_list = read_input()
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    process_list = read_input()
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])