#import random generating library
from numpy import random


#variables used to store parameters as described in section 4.6 of the lab manual
#note: we don't use discrete observer events but use a continuous approach instead, so a(alpha) is not used
#let user input the values of L, C, and rho
L = float(input('Please type the value of parameter L (in bits) and hit enter:'))
C = float(input('Please type the value of parameter C (in bits/second) and hit enter:'))
rho = float(input('Please type the value of parameter rho and hit enter:'))

#now calculate the value of lambda using L, C, and rho
#notice that we use lamb instead of lambda to avoid conflicting with python keyword lambda
lamb = rho*C/L

#other parameters to be calculated later on
E_N = 0.0 #E[N]
P_IDLE = 0.0
P_LOSS = 0.0

#other parameters required
T = float(input('Please type the simulation time in seconds and hit enter:'))
K = int(input('Please type the value of K in M/M/1/K model (this should be an integer), or 0 for M/M/1 model and hit enter:'))


#class used to represent the arrival/departure of a packet
class event: 
    def __init__(self, type, time, length): 
        self.type = type #0 for arrival, 1 for departure
        self.time = time #arrival time of the packet/finish time of the departure in seconds
        self.length = length #length of the packet arrving/departing in bits


#list used to store all arrival/departure events
#note: should have only one departure event at a time
event_list = [] 
#list used as the waiting queue for BOTH M/M/1 and M/M/1/K model
waiting = []


#generate objects of arrival class until the arrival time of the last generated object is greater than simulation time
#note that the last generated object will not actually 'arrive', it will be used to stop the simulation
cumulative_arrival_time = 0.0
length_for_generation = 0
while cumulative_arrival_time <= T:
  cumulative_arrival_time += random.exponential(1/lamb)
  length_for_generation = random.exponential(L)
  event_list.append( event(0, cumulative_arrival_time, length_for_generation) )

flag_busy = False #flag indicating if the server if free
drop_counter = 0 #number of packets dropped in total
arrival_counter = 0 #number of packets arrived in total
integrated_sum = 0.0 #the cumulative sum of length of a certain time period times the number of wating packets in that period (similar to integration)
free_time = 0.0 #total free (idle) time of the server
last_free = 0.0 #the time when the server is set free for the last time
last_change = 0.0 #the time when the number of waiting packets is changed for the last time
while True: #infinite while loop used to traverse through event_list
  current_event = event_list.pop(0)
  print(current_event.time)
  if current_event.time > T:
    #stop the simulation when actual simulation time has exceeded T
    if flag_busy == False:
      free_time += T - last_free #add the last piece of free time (if any) to total free time
    print('anticipated simulation time reached, stopping simulator')
    break
  elif current_event.type == 0:
    #deal with arrival event here
    arrival_counter += 1
    if flag_busy:
      #server is not free, check if the waiting queue has free slot(s)
      if K == 0 or len(waiting) < K:
        #there're available slot(s) in the waiting queue
        integrated_sum += len(waiting) * (current_event.time - last_change)
        last_change = current_event.time
        waiting.append( current_event )
      else:
        #the waiting queue is full, dropping packet!
        drop_counter += 1
    else:
      #server free, create departure event
      flag_busy = True
      free_time += current_event.time - last_free #update the total free time
      event_list.append( event(1, (current_event.time+(current_event.length/C)), current_event.length) )
      event_list.sort( key=lambda x: x.time )
  elif current_event.type == 1:
    #deal with departure event here
    if len(waiting) == 0:
      #waiting queue is empty, mark server as free
      flag_busy = False
      last_free = current_event.time #set last_free to be the end time of this departure
    else:
      #there're event(s) in the waiting queue, pop a packet from the waiting queue based on FIFO rule and create departure event for it
      integrated_sum += len(waiting) * (current_event.time - last_change)
      last_change = current_event.time
      next_departure = waiting.pop(0)
      event_list.append( event(1, (current_event.time+(next_departure.length/C)), next_departure.length) )
      event_list.sort( key=lambda x: x.time )
  else:
    #reserved for possible errors
    print('UNKNOWN event type: aborting')
    break

#calculate the asked parameters using the data collected
E_N = integrated_sum/T #notice that this calculate the time-average of waiting packets using a continuous (calculus-like) approach
P_IDLE = free_time/T
P_LOSS = drop_counter/arrival_counter

#print out the parameters at the end
print("E[N] is:")
print(E_N)
print("P_idle is:")
print(P_IDLE)
print("P_loss is:")
print(P_LOSS) #note: should be zero for M/M/1 model