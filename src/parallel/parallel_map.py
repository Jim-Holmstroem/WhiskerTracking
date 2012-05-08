#! /usr/bin/env python

__all__=['parallel_map']

import multiprocessing, Queue
import time
import operator

import numpy
import itertools

class MapJob:
    """
    Data acts as both inputdata and output data
    """
    def __init__(self,id,data):
        self.id=id
        self.data=data

class MapWorker(multiprocessing.Process):
    def __init__(self, work_queue,result_queue,map_function):
        multiprocessing.Process.__init__(self)
        self.work_queue=work_queue
        self.result_queue=result_queue
        self.map_function=map_function
        self.kill_received = False

    def start(self):
        multiprocessing.Process.start(self)
        return self

    def run(self):
        while not self.kill_received:
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                if self.work_queue.qsize()>0:
                    time.sleep(0.001)
                    continue
                else:
                    break
            try:
                job.data=self.map_function(job.data) #and preserve the in the MapJob
            except MemoryError: #not totally bulletproof but handles it better
                print job.id," OutOfMemory, retrying"
                continue
            self.result_queue.put(job)

def parallel_map(map_function,input_list,num_processors=multiprocessing.cpu_count()):
    """
    @param input_list list<A>
    @param map_function f:A->B
    @return list<B>
    """
    num_jobs=len(input_list)
    
    work_queue  =multiprocessing.Queue()
    result_queue=multiprocessing.Queue()
    
    try:
        map(lambda job_id:work_queue.put(MapJob(job_id,input_list[job_id])),range(num_jobs)) #create a list with job_id to keep track
    except Queue.Full:
        raise Exception("worker queue is full, this is not supported")

    workers = map(lambda proc:MapWorker(work_queue,result_queue,map_function).start(),range(num_processors)) #create, connect and start the workers to the queues
    output_list=[]

    map(lambda job_id:output_list.append(result_queue.get()),range(num_jobs)) #fetch all the resulting data
    
    output_list=sorted(output_list,key=lambda job:job.id)
    output_list =  map(lambda v:v.data,output_list) #extract the data by removing id

    return output_list

class SimpleProcess(multiprocessing.Process):
    def __init__(self,function,input_list,idx):
        """
        The total input list and the idx representing the works assigned to this process
        """
        multiprocessing.Process.__init__(self)
        self.input_list=input_list
        self.function=function
        self.idx=list(idx)
        self.output=[None]*len(self.idx)

    def start(self):
        multiprocessing.Process.start(self)
        return self
    
    def run(self):
        self.output= list(map(lambda i:self.function(self.input_list[i]),self.idx))
        
def parallel_homogenload_map(map_function,input_list,num_processors=multiprocessing.cpu_count()):
    """
    Simplest map-reduce
    """
    input_size=len(input_list)
    workload_distribution=itertools.groupby(range(len(input_list)),lambda i:num_processors*i//input_size)
    processes=map(lambda (proc_id,idx):SimpleProcess(map_function,input_list,idx),workload_distribution)
    map(lambda process:process.start(),processes) #start all
    map(lambda process:process.join(),processes) #wait for all
    
    return reduce(operator.add,map(lambda process:process.output,processes)) #get all the output and concatenate

if __name__ == "__main__":
    
    def workload(indata):
        return numpy.sum(indata+numpy.array(range(10**7)))

    measure=time.time#time.clock didnt work to well for parallel for some reason

    pool=multiprocessing.Pool(multiprocessing.cpu_count())

    N=16

    print "start parallelhomogenload"
    ticph=measure()
    answer_parallelhomogen=parallel_homogenload_map(workload,range(N))#parallel_map(workload,range(10),8)
    print "ans",answer_parallelhomogen
    tacph=measure()
    print "superParallel:",(tacph-ticph),"s"
    
    print "start parallel"
    ticp=measure()
    answer_parallel=parallel_map(workload,range(10),8)
    tacp=measure()
    print "Parallel:",(tacp-ticp),"s"
    
    print "start serial"
    tics=measure()
    answer_serial=map(workload,range(N//multiprocessing.cpu_count())) #only measure on /num_processors (easier to compare)
    tacs=measure() 
    print "Serial:",multiprocessing.cpu_count()*(tacs-tics),"s"
