#!/usr/bin/env python3
import os

def no_turbo(state):


	if state == 0:
		os.system('echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo')
	elif state == 1:
		os.system('echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo')
	else:
		print('State has to be 0 or 1')

def scaling_freq(min_freq, max_freq):

	if min_freq > max_freq:
		print('Max cannot be less than min')
	else:
		max_cmd = 'echo \"{max}\" | tee /sys/devices/system/cpu/cpu*/scaling_max_freq'
		min_cmd = 'echo \"{max}\" | tee /sys/devices/system/cpu/cpu*/scaling_min_freq'
		os.system(max_cmd.format(max=max_freq))
		os.system(min_cmd.format(min=min_freq))