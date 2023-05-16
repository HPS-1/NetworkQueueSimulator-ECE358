Note from Peisen:
This is a mini-project I wrote in Python as one of ECE 358 Computer Networks' labs. It is designed to simulate M/M/1 and M/M/1/K queues in network. Further details about the lab can be found in the attached lab manual (LAB1.pdf) and lab report (ECE358-F22-LAB Group67 Lab1 Report.pdf), while instructions on how to run the simulator can be found below. (You may also refer to howtorun.png.)

////////////////////////////////////
How to run our code:
On eceUbuntu (or some other (linux) machine with python and numpy installed) run the command:
*to be more specific, we used ecetesla3, so if you can't run the script on other machines, you may try to switch to ecetesla3

python simsimple.py

and then input the 5 parameters as asked.
There're will be prompts to give you hints on what to input, you may also refer to howtorun.png for a set of sample input.
And then the python script will run for one simulation and print E[N], P_idle, adn P_loss at the end.
It will also print out the arrival/departure time of packets encountered midway.
Done!
P.S. You may run the script for multiple times to test different sets of parameters.

And to run the script for Q1, just run:

python q1.py

#note: when a packet is being transmitted by the server, we consider it as NOT in the queue. This may cause our E[N] to be smaller
for approximately 1 compared to the value of E[N] gained if we consider the packet being transmitted as IN the queue. Also it may
somehow affect P_idle and P_loss.
