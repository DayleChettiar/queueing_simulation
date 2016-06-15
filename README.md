# queueing_simulation
analytical simulator model for open queuing network systems (Jackson Networks) using the open-source process-based discrete event simulation package, SimPy. This simulator model analyses the performance of a configuration of virtual machines (VMs) for a workload of jobs arriving at a queuing network system.


The file 'queueing_simulation.py' is a complete queueing network system for a (2, 1, 3) network where '2' is the number of servers in the first tier, '1' is the number of servers in the second tier and '3' is the number of servers in the third tier. This was part of a research project. So, if you modified the queuing network configuration between the ranges (1, 1, 1) to (3, 3, 3), you would find that the more  

The results showed that for a large number of jobs to be processed, if the number of servers in each tier were to be increased, generally, the performance (viz. mean response time or percentiles) of the system was better.

To run the file 'queueing_simulation.py', you need to install the 'simpy' library. You also need to install python version 2.7+. 

from the command line, execute the command 'python queueing_simulation.py'. 
