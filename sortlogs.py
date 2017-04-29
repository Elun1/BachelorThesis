#!/usr/bin/env python3

import os
import csv

def sort_allcombinations(src_dir, dst_dir):
    #Creates a combined file for all results in src dir
    for file in src_dir:
        output_line = ""
        first_bench = file.partition("_")[0]
        if file.startswith("4"):
            with open(file, 'r') as input_file, open(os.path.join(dst_path, 'ALL.log'), 'a') as output_file:
                lines = input_file.read().splitlines()

                if first_bench in lines[0]:
                    for line in lines:
                        output_line += line
                        output_line += " "
                else:
                    #swap lines
                    lines[0], lines[1] = lines[1], lines[0]
                    for line in lines:
                        output_line += line
                        output_line += " "

                #Columns in right order
                output_line = output_line.split(" ")
                output_line[1], output_line[2] = output_line[2], output_line[1]
                output_line = " ".join(output_line)

                output_file.write(output_line)
                output_file.write("\n")

    #Creates seperate logfiles for each program
    benchmark_list = ['400.perlbench.sh', '401.bzip2.sh', '403.gcc.sh', '410.bwaves.sh', '429.mcf.sh', '433.milc.sh', '434.zeusmp.sh', '435.gromacs.sh', '436.cactusADM.sh', '437.leslie3d.sh', '444.namd.sh', '445.gobmk.sh', '447.dealII.sh', '450.soplex.sh', '453.povray.sh', '454.calculix.sh', '456.hmmer.sh', '458.sjeng.sh', '459.GemsFDTD.sh', '462.libquantum.sh', '464.h264ref.sh', '465.tonto.sh', '470.lbm.sh', '471.omnetpp.sh', '473.astar.sh', '481.wrf.sh', '482.sphinx3.sh', '483.xalancbmk.sh']
    for benchmark in benchmark_list:
        with open(os.path.join(dst_dir, 'ALL.log'), 'r') as input_file, open(os.path.join(dst_dir,'{}.log'.format(benchmark)), 'w') as output_file:
            lines = input_file.read().splitlines()
            output_data = []

            for line in lines:
                columns = line.split(' ')
                if benchmark in line:
                    if benchmark in columns[0]:
                        output_data.append(" ".join(columns))

                    else:
                        columns[0], columns[1] = columns[1], columns[0]
                        columns[2], columns[3] = columns[3], columns[2]
                        output_data.append(" ".join(columns))
            output_data = sorted(output_data, key=lambda x: float(x.split(" ")[2]), reverse=True)
            for line in output_data:
                output_file.write(line)
                output_file.write("\n")

def convert_logs_to_csv(path, remove=None):
    os.chdir(path)
    for file in os.listdir(path):
        log_file = file
        csv_file = log_file.replace('.log', '.csv')
        with open(log_file, 'r') as input_file, open(csv_file, 'w') as output_file:
            in_log = csv.reader(input_file, delimiter = ' ')
            out_csv = csv.writer(output_file)
            out_csv.writerows(in_log)
    if remove:
        for file in os.listdir(path):
            if file.endswith('.log'):
                os.remove(file)

def calculate_stp():
    path = os.getcwd() + '/logs/'
    st_file = path + 'SingleThread/singlethread.log'
    # Read singlethread.log into dict
    st_times = {} 
    with open(st_file, 'r') as f:
        data = f.read().splitlines()
    for line in data:
        job_name, job_time = line.split(" ")[2:]
        st_times[job_name] = job_time
    # Read smt logs into dict

    for subdir in os.listdir(path):
        if subdir.startswith("Runs"):
            stp_times = {} # {'462.libquantum.sh_470.lbm.sh': {'stp_pairs': 31231, 'stp_no_pairs': 32123, 'stp_diff': 21313}}
            for file in os.listdir(path + subdir):

                if file.endswith("_NoPairs.log"):
                    file_key = file.rstrip("_NoPairs.log")
                    if file_key not in stp_times:
                        stp_times[file_key] = {}
                    stp_times[file_key]["stp_no_pairs"] = calc_stp(path + subdir + '/' + file, st_times)

                elif file.endswith("_AllPairs.log"):
                    file_key = file.rstrip("_AllPairs.log")
                    if file_key not in stp_times:
                        stp_times[file_key] = {}
                    stp_times[file_key]["stp_pairs"] = calc_stp(path + subdir + '/' + file, st_times)

                elif file.endswith("_NoHT.log"):
                    file_key = file.rstrip("_NoHT.log")
                    if file_key not in stp_times:
                        stp_times[file_key] = {}
                    stp_times[file_key]["stp_no_ht"] = calc_stp(path + subdir + '/' + file, st_times)

            for file_key in stp_times:
                stp_times[file_key]["stp_diff"] = stp_times[file_key]["stp_no_pairs"] - stp_times[file_key]["stp_pairs"]
                with open(path + subdir + '/' + file_key + "_stp.log", 'w') as f:
                    f.write("STP AllPairs: " + str(stp_times[file_key]["stp_pairs"]) + "\n")
                    f.write("STP NoPairs: " + str(stp_times[file_key]["stp_no_pairs"]) + "\n")
                    f.write("STP Diff: " + str(stp_times[file_key]["stp_diff"]))
                    if "stp_no_ht" in stp_times[file_key]:
                        f.write("\n" + "STP NO HT: " + str(stp_times[file_key]["stp_no_ht"]))


def calc_stp(filename, st_times):
    #print(filename)
    smt_times = {}
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    for line in data:
        job_name, job_time = line.split(" ")[2:]
        if not job_name in smt_times:
            smt_times[job_name] = []
        smt_times[job_name].append(job_time)

    stp = 0.0 # System throughput
    for job_name, smt_job_times in smt_times.items():
        st_time = st_times[job_name]
        for smt_time in smt_job_times:
            #print(st_time + " / " + smt_time + " = " + str(float(st_time) / float(smt_time)))
            stp += float(st_time) / float(smt_time)
    #print(stp)
    return stp

if __name__ == "__main__":
    calculate_stp2()