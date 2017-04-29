#!/usr/bin/python3

import os
import datetime
import random
import runjobs
import sortlogs

def main():

    test_jobs = ['400.jobA.sh', '401.jobB.sh', '402.jobC.sh', '403.jobD.sh']

    remotehost = '10.0.0.1'
    create_log_folders()
    runjobs.single_thread(test_jobs)
    create_archive('./logs/SingleThread', 'singlethread.tar')
    runjobs.all_combinations(test_jobs)
    create_archive('./logs/AllCombinations', 'allcombinations.tar')

    totaljoblist = [4, 8, 12, 24]

    counter = 0:
    while counter < 10:
        jobs = random.sample(test_jobs, 2)
        for totaljobs in totaljobslist:
            if runjobs.check_logs(jobs, totaljobs) == 0:
                runjobs.all_pairs(jobs, totaljobs)
                runjobs.no_pairs(jobs, totaljobs)
                if totaljobs == 12:
                    runjobs.no_ht(jobs, totaljobs)
            else:
                print("Combination already run. Getting new job mix")

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