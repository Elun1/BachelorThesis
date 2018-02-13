#!/usr/bin/python3

import os
import datetime
import random
from runjobs import *
from sortlogs import *
from cpu_conf import *


def main():

    benchmark_list = ['400.perlbench.sh', '401.bzip2.sh', '403.gcc.sh', '410.bwaves.sh', '429.mcf.sh', '433.milc.sh', '434.zeusmp.sh', '435.gromacs.sh', '436.cactusADM.sh', '437.leslie3d.sh', '444.namd.sh', '445.gobmk.sh', '447.dealII.sh', '450.soplex.sh', '453.povray.sh', '454.calculix.sh', '456.hmmer.sh', '458.sjeng.sh', '459.GemsFDTD.sh', '462.libquantum.sh', '464.h264ref.sh', '465.tonto.sh', '470.lbm.sh', '471.omnetpp.sh', '473.astar.sh', '481.wrf.sh', '482.sphinx3.sh', '483.xalancbmk.sh']
    test_jobs = ['400.jobA.sh', '401.jobB.sh', '402.jobC.sh', '403.jobD.sh']

    remotehost = '10.0.0.1'
    create_log_folders()

    single_thread(benchmark_list, remotehost)
    create_archive('./logs/SingleThread', 'singlethread.tar.gz')

    all_combinations(benchmark_list, remotehost)
    create_archive('./logs/AllCombinations', 'allcombinations.tar.gz')

    total_jobs_increment = [4, 8, 12, 24]
    c = 0
    while c >= 20:
        jobs = random.sample(benchmark_list, 2)
        for totaljobs in total_jobs_increment:
            if check_logs(jobs) == 0:
                all_pairs(jobs, totaljobs, remotehost)
                no_pairs(jobs, totaljobs, remotehost)
                no_ht(jobs, totaljobs, remotehost)

    for subdir in os.listdir('./logs/'):
        if subdir.startswith('Runs'):
            archive = 'subdir' + 'tar.gz'
            src_file = './logs/' + subdir
            create_archive(archive, src_file)

    stp()

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
    tar_cmd = 'tar -cf {archive} {file}'

    fcounter = 1
    if os.path.isfile(archive) or os.path.isdir(archive):
        while os.path.isfile(archive + str(fcounter) + '.tar.gz'):
            fcounter += 1

    archive += str(fcounter)
    os.system(tar_cmd.format(archive=archive, file=src))

if __name__ == '__main__':
    main()
