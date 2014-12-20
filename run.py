#!/usr/bin/env python
import sys
import os
import subprocess, threading

in_dir="in/"
expected_out_dir="out/"
prog_out_dir="prog_out/"
timer_file="tmp/timer"
diff_file="tmp/difference"
diff_tmp1_file="tmp/tmp1"
diff_tmp2_file="tmp/tmp2"
suffix=".out"
default_time_limit=2

time_limit=default_time_limit

# Functions and utilities

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None
	
	def run(self):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True)
			self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(time_limit)
		if thread.is_alive():
			self.process.terminate()
			thread.join()
			return 1
		return 0

def run(com):
	command=Command(com)
	return command.run()

def run_test(prog,file_in,file_out_prog):
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

files=os.listdir(in_dir)
files.sort()
for f in files:
	print "Testing "+f+":"
	fi=in_dir+f
	fo=expected_out_dir+os.path.splitext(f)[0]+suffix
	fop=prog_out_dir+os.path.splitext(f)[0]+suffix
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