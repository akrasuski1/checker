#!/usr/bin/env python
import sys
import os
import subprocess, threading
import signal
import re

CURRENT_WORKING_DIRECTORY=os.getcwd()
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

IN_FILE_PATTERN=re.compile("test(\d+?).in")
OUT_FILE_PATTERN=re.compile("test(\d+?).out")

in_dir=os.path.join(CURRENT_WORKING_DIRECTORY,"in/")
expected_out_dir=os.path.join(CURRENT_WORKING_DIRECTORY,"out/")

prog_out_dir=os.path.join(SCRIPT_DIRECTORY,"prog_out/")
timer_file=os.path.join(SCRIPT_DIRECTORY,"tmp/timer")
diff_file=os.path.join(SCRIPT_DIRECTORY,"tmp/difference")
diff_tmp1_file=os.path.join(SCRIPT_DIRECTORY,"tmp/tmp1")
diff_tmp2_file=os.path.join(SCRIPT_DIRECTORY,"tmp/tmp2")
default_time_limit=2

time_limit=default_time_limit

# Functions and utilities

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None
	
	def run(self):
		def target():
			self.process = subprocess.Popen(self.cmd,shell=True,preexec_fn=os.setsid)
			self.process.communicate()
			
		thread = threading.Thread(target=target)
		thread.start()
		thread.join(time_limit)
		if thread.is_alive():
			os.killpg(self.process.pid,signal.SIGTERM)
			thread.join()
			return 1
		return 0

def run(com):
	command=Command(com)
	return command.run()

def run_test(prog,file_in,file_out_prog):
	# type: (str, str, str) -> int
	command="time -f \"Time: %es\\nMemory: %MkB\" -o "+timer_file+" ./"+prog+" < "+file_in
	command=command+" > "+file_out_prog
	if run(command):
		print "Time Limit Exceeded"
		print ""
		return 1
	result=open(timer_file)
	txt=result.read()
	sys.stdout.write(txt)
	result.close()
	return 0

def compare(file_out,file_out_prog):
	command="tr '\\n' ' ' < "+file_out+" > "+diff_tmp1_file
	run(command)
	command="tr '\\n' ' ' < "+file_out_prog+" > "+diff_tmp2_file
	run(command)

	command ="diff -Bqb "+diff_tmp1_file+" "+diff_tmp2_file+" > "+diff_file
	run(command)
	result=open(diff_file)
	txt=result.read()
	if len(txt)>5:
		print "Wrong Answer"
		ret=0
	else:
		print "Correct"
		ret=1
	result.close()
	print ""
	return ret

def usage():
	print "Usage: "+sys.argv[0]+" [time_limit_in_seconds] filename.out"

# Entry point

if len(sys.argv)<2 or len(sys.argv)>3:
	usage()
	exit(2)

if len(sys.argv)==3:
	time_limit=float(sys.argv[1])

prog_name=sys.argv[-1]
print ""
correct=0
wa=0
tle=0

files=os.listdir(prog_out_dir)
for f in files:
	os.remove(prog_out_dir+f)

input_files=[input_file for input_file in os.listdir(in_dir) if IN_FILE_PATTERN.match(input_file)]
input_files.sort(key = lambda file_name: int(IN_FILE_PATTERN.match(file_name).group(1)))
for f in input_files:
	print "Testing "+f+":"
	fi=os.path.join(in_dir,f)
	id=IN_FILE_PATTERN.match(f).group(1)
	out_file_name=OUT_FILE_PATTERN.pattern.replace("(\d+?)",id)
	fo = os.path.join(expected_out_dir, out_file_name)
	if not os.path.isfile(fo):
		print "output file missing - skipping this testcase\n"
		continue
	fop=os.path.join(prog_out_dir,out_file_name)
	if run_test(prog_name,fi,fop):
		tle=tle+1
		continue
	if compare(fo,fop):
		correct=correct+1
	else:
		wa=wa+1

print "Statistics:"
print "========================"
print str(correct)+" x Correct"
print str(wa)+" x Wrong Answer"
print str(tle)+" x Time Limit Exceeded"
print "========================"
