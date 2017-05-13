#!/bin/python3

import os
import time
import itertools

def start_job(thread, job, log, donejobs):

    donefile = 'done.{job}.{thread}'.format(job=job, thread=thread)
    taskset = '(/usr/bin/time -f \"Thread {thread}: {job}: %e\" -a -o {log} taskset -c {thread} ./{job};touch {donefile}) &'
    os.system(taskset.format(thread=thread, job=job, log=log, donefile=donefile))

    print('Running {job} on Thread: {thread}'.format(job=job, thread=thread))
    if donefile not in donejobs:
        donejobs.append(donefile)

    return donejobs

def start_job_wo_time(thread, job, done):

    taskset = '(taskset -c {thread} ./{job}; touch {done}) &' 
    os.system(taskset.format(thread=thread, job=job, done=done))
    print('Running dummy for {job} on Thread: {thread}'.format(job=job, thread=thread)) 

def sync():

    os.system("sync")
    time.sleep(30)

def scp_log(logdir, logfile, remotehost):

    remote_dir = logdir.replace('./', '')
    scp_cmd = 'scp {log} {remotehost}:{remotedir}'
    os.system(scp_cmd.format(log=log, remotehost=remotehost, remotedir=remotedir))

def single_thread(jobs, remotehost=None):

    #this function doesn't use start_job and check_done 
    thread = 0
    logdir = './logs/SingleThread/'

    for job in jobs:
        logfile = logdir + 'singlethread.log'.format(job=job)
        donefile = 'done.{job}.{thread}'.format(job=job, thread=thread)

        print("Running {job} on Thread: {thread}".format(job=job, thread=thread))
        taskset = '(/usr/bin/time -f \"Thread {thread}: {job}: %e\" -a -o {log} taskset -c {thread} ./{job};touch {donefile}) &'
        os.system(taskset.format(thread=thread, job=job, log=logfile, donefile=donefile))

        while os.path.isfile(donefile) == False:
            time.sleep(5)
        os.system('rm {done}'.format(done=donefile))

        sync()
        if remotehost:
            scp_log(logdir, logfile, remotehost)

def all_combinations(jobs, remotehost=None):

    thread1 = 0
    thread2 = 12
    totaljobs = 2
    logdir = './logs/AllCombinations/'

    for comb in itertools.combinations_with_replacement(jobs, 2):

    	donejobs = []
        logfile = logdir + '{jobA}_{jobB}.log'.format(jobA=comb[0], jobB=comb[1])

        start_job(thread1, comb[0], logfile, donejobs)
        start_job(thread2, comb[1], logfile, donejobs)

        finishedlist = []
        finished = False

        if comb[0] != comb[1]:
            check_done(donejobs, totaljobs)
            
        else:
            print("Pair detected. Not running dummies\n")
            while not finished:
                time.sleep(5)
                for donefile in donejobs:
                    if os.path.isfile(donefile):
                        finishedlist.append(donefile)
                    if len(finishedlist) >= totaljobs:
                        finished = True

        for donefile in finishedlist:
            os.system('rm {done}'.format(done=donefile))

        if remotehost:
            scp_log(logdir, logfile, remotehost)
        sync()

def all_pairs(jobs, totaljobs, remotehost=None):

    jobs_unique = len(jobs)
    jobs_instances = totaljobs//jobs_unique
    assert jobs_unique % 2 == 0

    logdir = './logs/Runs{jobs}_{instances}'.format(jobs=jobs_unique, instances=jobs_instances)
    logfile = logdir + '_'.join(jobs) + '_AllPairs.log'

    print('Running {jobs}_{instances} All Pairs'.format(jobs=jobs_unique, instances=jobs_instances))

    donejobs = []
    thread = 0

    for job in jobs:
        for _ in range(jobs_instances//2):
            start_job(thread, job, logfile, donejobs)
            start_job(thread+12, job, logfile, donejobs)
            thread += 1

    print('All processes are running')
    check_done(donejobs, totaljobs)

    if remotehost:
        scp_log(logdir, logfile, remotehost)
    sync()

def no_pairs(jobs, totaljobs, remotehost=None):

    jobs_unique = len(jobs)
    jobs_instances = totaljobs//jobs_unique
    assert jobs_unique % 2 == 0

    logdir = './logs/Runs{jobs}_{instances}'.format(jobs=jobs_unique, instances=jobs_instances)
    logfile = logdir + '_'.join(jobs) + '_NoPairs.log'

    print('Running {jobs}_{instances} No Pairs'.format(jobs=jobs_unique, instances=jobs_instances))
    job_split1 = jobs[:jobs_unique//2]
    job_split1 = jobs[jobs_unique//2:]
    donejobs = []

    thread = 0
    for job in job_split1:
        for _ in range(thread, thread+job_instances):
            start_job(thread, job, logfile, donejobs)

    thread = 12
    for job in job_split2:
        for _ in range(thread, thread+job_instances):
            start_job(thread, job, logfile, donejobs)

    print("All processes are running")
    check_done(donejobs, totaljobs)

    if remotehost:
        scp_log(logdir, logfile, remotehost)
    sync()

def no_ht(jobs, totaljobs, remotehost=None):
    jobs_unique = len(jobs)
    jobs_instances = totaljobs//jobs_unique
    assert jobs_unique % 2 == 0
    assert totaljobs <= 12

    logdir = './logs/Runs{jobs}_{instances}'.format(jobs=jobs_unique, instances=jobs_instances)
    logfile = logdir + '_'.join(jobs) + '_NoHT.log'

    print('Running {jobs}_{instances} without HT'.format(jobs=jobs_unique, instances=jobs_instances))

    donejobs = []
    thread = 0

    for _ in range(total_jobs//2):
        start_job(thread, jobs[0], logfile, donejobs)
        start_job(thread+6, jobs[1], logfile, donejobs)
        thread += 1
    print("All processes are running")
    check_done(donejobs, totaljobs)

    if remotehost:
        scp_log(logdir, logfile, remotehost)
    sync()

def check_logs(jobs, totaljobs):
    #This is bad, and I should feel bad. Also only works if totaljobs == 2
    jobs_unique = len(jobs)
    jobs_instances = totaljobs//jobs_unique
    logdir = './logs/Runs{unique}_{instances}'.format(unique=jobs_unique, instances=jobs_instances)
    logfile = logdir + '/{jobA}_{jobB}'.format(jobA=jobs[0], jobB=jobs[1])

    allpairs_log = logfile + '_AllPairs'
    nopairs_log = logfile + '_NoPairs'
    logexist = 0

    if os.path.isfile(allpairs_log):
        logexist += 1
    if os.path.isfile(nopairs_log):
        logexist += 1

    jobs[0], jobs[1] = jobs[1], jobs[0]
    logfile = logdir + '/{jobA}_{jobB}'.format(jobA=jobs[0], jobB=jobs[1])

    if os.path.isfile(allpairs_log):
        logexist += 1
    if os.path.isfile(nopairs_log):
        logexist += 1

    return logexist

def check_done(donejobs, totaljobs):

    finishedlist = []
    finished = False

    while not finished:
        time.sleep(2)
        for donefile in donejobs:
            if os.path.isfile(donefile):
                donesplit = donefile.split('.')
                thread = donesplit[4]
                indices = [1, 2, 3]
                job = '.'.join([donesplit[i] for i in indices])
                if donefile not in finishedlist:
                    finishedlist.append(donefile)
                os.system('rm {done}'.format(done=donefile))
                start_job_wo_time(thread, job, donefile)
                if len(finishedlist) >= totaljobs:
                    finished = True

    print('Done running dummies\nWaiting for existing dummies to finish.')

    finishedlist = []
    finished = False

    while not finished:
        time.sleep(2)
        for donefile in donejobs:
            if os.path.isfile(donefile) and donefile not in finishedlist:
                finishedlist.append(donefile)
            if len(finishedlist) >= totaljobs:
                finished = True

    print('All dummies are done\nCleaning up...\n')
    os.system('rm done*')