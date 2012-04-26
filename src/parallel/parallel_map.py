#! /usr/bin/env python

__all__=['parallel_map']

import random
import multiprocessing, Queue
import time

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

def parallel_map(map_function,input_list,num_processors=8):
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
        #print "Queue.Full"
        raise Exception("worker queue is full, this is not supported")

    print work_queue.qsize() #only approx size
    workers = map(lambda proc:MapWorker(work_queue,result_queue,map_function).start(),range(num_processors)) #create, connect and start the workers to the queues
    output_list=[]
    #print "start fetching output"

    #def getter(job_id):
    #    print "getter(",job_id,")"
    #    ans = result_queue.get()
    #    print "gotten(",job_id,")"
    #    return ans

    map(lambda job_id:output_list.append(result_queue.get()),range(num_jobs)) #fetch all the resulting data
    
    #print "done fetching output"
    
    for worker in workers:
        worker=[]
    #print "killed workers"
    output_list=sorted(output_list,key=lambda job:job.id)
    output_list =  map(lambda v:v.data,output_list) #extract the data by removing id

    return output_list


class SimpleProcessor(multiprocessing.Process):
    def __init__(self,function,input_list,idx):
        multiprocessing.Process.__init__(self)
        self.input_list=input_list
        self.function=function
        self.idx=idx

    def run(self):
        print "run"
        self.output=list(map(lambda i:self.function(self.input_list[i]),self.idx))

def parallel_homogenload_map(map_function,input_list,num_processors=8):
    input_size=len(input_list)
    workload_distribution=itertools.groupby(range(len(input_list)),lambda i:num_processors*i//input_size)
    processes=map(lambda (proc_id,idx):SimpleProcessor(map_function,input_list,idx),workload_distribution)
    print "start all"
    map(lambda process:process.start(),processes) #start all
    print "wait for all"
    map(lambda process:process.join(),processes) #wait for all
    print "all done"
    print dir(processes[0])
    return sum(map(lambda process:process.output,processes)) #get all the output and concatinate


if __name__ == "__main__":
    
    def workload(indata):
        return numpy.sum(indata+numpy.array(range(10**7)))

    measure=time.time#time.clock didnt work to well for parallel for some reason

    pool=multiprocessing.Pool(8)

    print "start parallelhomogenload"
    ticph=measure()
    answer_parallelhomogen=parallel_homogenload_map(workload,range(16))#parallel_map(workload,range(10),8)
    tacph=measure()
    print "start parallel"
    ticp=measure()
    answer_parallel=pool.map(workload,range(16))#parallel_map(workload,range(10),8)
    tacp=measure()
    print "start serial"
    tics=measure()
    answer_serial=map(workload,range(10))
    tacs=measure()

    
    print "Parallel:",(tacph-ticph),"s"
    print "Parallel:",(tacp-ticp),"s"
    print "Serial:",(tacs-tics),"s"

