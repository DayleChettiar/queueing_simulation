""" FCFS queues"""
from SimPy.Simulation import *
from math import *
from decimal import *
from random import expovariate, seed

## Model components ------------------------
class QN():   
    def model(self, nrRuns, num, arrRate, endTime):
        averageRespTimeSum = 0.0
        probMetDeadlineSum = 0.0
        for runNr in range(nrRuns):
            self.wm1 = Monitor(name='ResponseTime')
            self.numberMeetDeadline = 0
            
            initialize()
            source = Source(self)
            activate(source,source.generate(num, arrRate, processors), at=0.0)
            simulate(until=endTime)
            
            if(self.wm1.count() > 0):
                result1 = self.wm1.count(), self.wm1.mean(), self.wm1.total()
                averageRespTimeSum = averageRespTimeSum + self.wm1.mean()
                print("Average response time for %3d completions was %3.3f seconds. Total response time = %3.5f." % result1)
                probMetDeadline = float(self.numberMeetDeadline)/self.wm1.count()
                probMetDeadlineSum = probMetDeadlineSum + probMetDeadline
                print("%d out of %d Jobs met the response time requirement of %f" % (self.numberMeetDeadline, self.wm1.count(), responseTimeReq))
                print("Probability of Jobs that met the response time requirement of %3.2f is %3.3f" % (responseTimeReq, probMetDeadline))
                print ("%s run(s) completed" %(runNr + 1))

        print("****************************************************************************")
        print("Configuration is (%d,%d,%d)" % (numberOfL1VMs,numberOfL2VMs,numberOfL3VMs))
        print("Average response time over %d runs is %3.3f seconds." % (nrRuns, averageRespTimeSum/nrRuns))
        print("Probability of Jobs that met the response time requirement of %3.2f over %d runs is %3.3f" % (responseTimeReq, nrRuns, float(probMetDeadlineSum)/nrRuns))
        print("****************************************************************************")
                

class Source(Process):
    """ Source generates jobs randomly"""
    def __init__(self,sys):
        Process.__init__(self)
        self.sys = sys

    def generate(self, number, arrRate, processors):
        for i in range(number):
            c = Job("Job%02d" % (i), i, self.sys)
            activate(c, c.visit(processors))
            t = expovariate(arrRate)
            ##t = 1.0/arrRate
            yield hold, self, t

class Job(Process):
    """ Job arrives, chooses the shortest queue
        is served and leaves
    """
    def __init__(self,name,i,sys):
        Process.__init__(self)
        self.name=name
        self.i=i
        self.sys = sys
        
    
    def visit(self, processors):
        arrivalToSystem = now()
        print ("%8.5f %s: Arrives     "%(now(),self.name))

        arrive = now()
        ##Job then moves to first level of servers
        p = numberOfL1VMs
        j = random.randint(1, p)
        yield request,self,processors[j-1]
        wait = float(now()-arrive)
        print ("%3.8f %s: Waited for %3.8f for %s"%(now(),self.name,wait, processors[j-1].name))
        tiw = expovariate(serviceRateL1)
        ##tiw = 1.0/serviceRateL1
        yield hold,self,tiw                      
        yield release,self,processors[j-1]

        arrive = now()
        ##Job then moves to second level of servers
        q = numberOfL2VMs
        k = random.randint(1, q)
        yield request,self,processors[numberOfL1VMs+k-1]
        wait = float(now()-arrive)
        print ("%3.8f %s: Waited for %3.8f for %s"%(now(),self.name,wait, processors[numberOfL1VMs+k-1].name))
        tiw = expovariate(serviceRateL2)
        ##tiw = 1.0/serviceRateL2
        yield hold,self,tiw                      
        yield release,self,processors[numberOfL1VMs+k-1]

        arrive = now()
        ##Job then moves to third level of servers
        r = numberOfL3VMs
        l = random.randint(1, r)
        yield request,self,processors[numberOfL1VMs+numberOfL2VMs+l-1]
        wait = float(now()-arrive)
        print ("%3.8f %s: Waited for %3.8f for %s"%(now(),self.name,wait, processors[numberOfL1VMs+numberOfL2VMs+l-1].name))
        tiw = expovariate(serviceRateL3)
        ##tiw = 1.0/serviceRateL3
        yield hold,self,tiw                      
        yield release,self,processors[numberOfL1VMs+numberOfL2VMs+l-1]
            
                
        ## Job processing is done and the job leaves the network
        print ("%8.5f %s: Finished      "%(now(),self.name))
        responseTime = now() - arrivalToSystem
        print("%8.5f %s Response time: %2f" % (now(), self.name, responseTime))
        if responseTime <= responseTimeReq:
            self.sys.numberMeetDeadline = self.sys.numberMeetDeadline + 1
        self.sys.wm1.observe(responseTime)
        

## Parameters -------------------------

maxNumber = 1000
endTime = 2000.0    # seconds
serviceRateL1 = 60  # 60 jobs per second
serviceRateL2 = 70  # 70 jobs per second
serviceRateL3 = 80  # 80 jobs per second
arrRate = 100     # 100 arrivals per second
nrRuns = 3       # number of simulation runs
theseed = 787878
processors = []

responseTimeReq = 0.2
numberOfL1VMs = 2
numberOfL2VMs = 1
numberOfL3VMs = 3

for x in range(numberOfL1VMs):
    processors.append(Resource(name="L1VM"+str(x+1)))
for y in range(numberOfL2VMs):
    processors.append(Resource(name="L2VM"+str(y+1)))
for z in range(numberOfL3VMs):
    processors.append(Resource(name="L3VM"+str(z+1)))


## Model ------------------------------

seed(theseed)
plt=QN()
plt.model(nrRuns, maxNumber, arrRate, endTime)


