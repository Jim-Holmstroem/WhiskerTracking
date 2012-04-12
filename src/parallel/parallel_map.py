#! /usr/bin/env python

__all__=['parallel_map']

import random
import multiprocessing, Queue
import time

import numpy

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
                print "Queue.empty"
                break
            try:
                job.data=self.map_function(job.data) #and preserve the in the MapJob
            except MemoryError: #not totally bulletproof but handles it batter
                print job.id,". OutOfMemory, retrying"
                continue
            print job.id,". work done"
            self.result_queue.put(job)

def parallel_map(map_function,input_list,num_processors=4):
    """
    @param input_list list<A>
    @param map_function f:A->B
    @return list<B>
    """
    num_jobs=len(input_list)
    
    work_queue  =multiprocessing.Queue()
    result_queue=multiprocessing.Queue()

    map(lambda job_id:work_queue.put(MapJob(job_id,input_list[job_id])),range(num_jobs)) #create a list with job_id to keep track
    workers = map(lambda proc:MapWorker(work_queue,result_queue,map_function).start(),range(num_processors)) #create, connect and start the workers to the queues
    output_list=[]
    print "start fetching output"
    map(lambda job_id:output_list.append(result_queue.get()),range(num_jobs)) #fetch all the resulting data
    print "done fetching output"
    for worker in workers:
        worker=[]
    print "killed workers"
    output_list=sorted(output_list,key=lambda job:job.id)
    output_list =  map(lambda v:v.data,output_list) #extract the data by removing id

    return output_list

if __name__ == "__main__":
    
    def workload(indata):
        return numpy.sum(indata+numpy.array(range(5*10**7)))

    print "start parallel"
    ticp=time.clock()
    answer_parallel=parallel_map(workload,range(16))
    tacp=time.clock()
    print "start serial"
    tics=time.clock()
    answer_serial=map(workload,range(16))
    tacs=time.clock()

    print "Parallel:",(tacp-ticp),"s"
    print "Serial:",(tacs-tics),"s"

