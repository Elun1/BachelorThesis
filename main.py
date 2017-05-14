#!/usr/bin/python3

import os
import datetime
import random
from runjobs import *
'''
start_job(thread, job, log, donejobs)
start_job_wo_time(thread, job, done)
sync() #Calls sync with os.system() and sleeps for 30 sec
scp_log(logdir, logfile, remotehost)
single_thread(jobs, remotehost=None)
all_combinations(jobs, remotehost=None)
all_pairs(jobs, totaljobs, remotehost=None)
no_pairs(jobs, totaljobs, remotehost=None)
no_ht(jobs, totaljobs, remotehost=None)
check_logs(jobs, totaljobs)
check_done(donejobs, totaljobs)
'''
from sortlogs import *
'''
sort_allcombinations(src_dir, dst_dir) #this isnt tested
convert_logs_to_csv(path, remove=None)
stp()
calc_stp(filename, st_times) #
'''
from cpu_conf import *
'''
no_turbo(state) #this isnt tested, but should work
scaling_freq(min_freq, max_freq) #this isnt tested
'''

def main():

    benchmark_list = ['400.perlbench.sh', '401.bzip2.sh', '403.gcc.sh', '410.bwaves.sh', '429.mcf.sh', '433.milc.sh', '434.zeusmp.sh', '435.gromacs.sh', '436.cactusADM.sh', '437.leslie3d.sh', '444.namd.sh', '445.gobmk.sh', '447.dealII.sh', '450.soplex.sh', '453.povray.sh', '454.calculix.sh', '456.hmmer.sh', '458.sjeng.sh', '459.GemsFDTD.sh', '462.libquantum.sh', '464.h264ref.sh', '465.tonto.sh', '470.lbm.sh', '471.omnetpp.sh', '473.astar.sh', '481.wrf.sh', '482.sphinx3.sh', '483.xalancbmk.sh']
    test_jobs = ['400.jobA.sh', '401.jobB.sh', '402.jobC.sh', '403.jobD.sh']

    remotehost = '10.0.0.1'
    create_archive()

def create_log_folders():

    #These are the folders I use, add subfolders for different scaling methods
    root_folder = './logs/'
    subfolders = ['Runs2_2/', 'Runs2_4/', 'Runs2_6/', 'Runs2_12/', 'AllCombinations', 'SingleThread']

    #Create root and subfolders if they don't exist
    if not os.path.isdir(root_folder):
        os.system('mkdir {folder}'.format(folder=root_folder))

    for subfolder in subfolders:
        folder = root_folder + subfolder
        if not os.path.isdir(folder):
            os.system('mkdir {folder}'.format(folder=folder))

def create_archive(src, archive):
    #creates archive.
    tar_cmd = 'tar -cf {archive}.tar.gz {file}'

    fcounter = 1
    if os.path.isfile(archive + '.tar.gz'):
        while os.path.isfile(archive + str(fcounter) + '.tar.gz'):
            fcounter += 1

    archive += str(fcounter)
    os.system(tar_cmd.format(archive=archive, file=src))

if __name__ == '__main__':
    main()