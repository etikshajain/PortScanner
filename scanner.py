import socket
import threading
from queue import Queue
import time


print_lock=threading.Lock()

target='' ##ip to be scanned

#function to check whether a port is open or not
def pscan(port):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn=s.connect((target,port))
        with print_lock:
            print("port",port,"is open")
        conn.close()
    except:
        pass


#########################################################################################################################################################################


#S9: Thread flow: threads take jobs from a queue and not a list
#1: create worker threads
#2: store jobs in queue
#3: create work function and get the queue
queue=Queue()
numOfTasks = 65000   #num of ports
numOfWorkers = 65000

#so:
#numOfWorkers is the number of workers are created
#numOfTasks is the number of jobs to be done, their index is stored in queue using createjobs()
#work() function defines the task that the worker will do by taking the index number from queue as input
#createWorkers() creates a worker and make sit call the work function and do the task
#so:
#createWorkers() is called->it runs a loop of numOfWorkers-->each worker calls work() function-->but first the queue of the index of task is already created->when a worker calls work()->
#this worker gets assigned the topmost element(index of task) of the queue and the work uses that index to do the task and -->then this element of queue is deleted->
#then the next worker performs the next task and so on....


#so number of tasks done by each worker=number of tasks/number of workers



def createWorkers():    #createWorkers() creates a worker and make sit call the work function and do the task
    for _ in range(numOfWorkers):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def createJobs():  #numOfTasks is the number of jobs to be done, their index is stored in queue using createjobs()
    for x in range(numOfTasks):
        queue.put(x)
    queue.join()

def work():   #work() function defines the task that the worker will do by taking the index number from queue as input
    while True: #in this case, we have the same task for every worker
        worker = queue.get()
        pscan(worker)
        queue.task_done()

start=time.time()
createWorkers()
createJobs()
print('time taken for',numOfTasks,'ports is:', time.time()-start)
