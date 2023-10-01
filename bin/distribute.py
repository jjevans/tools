#!/usr/bin/env python
import sys
import os
import jobs
import re

do_run = True
do_print = True
do_throw = False
do_kill = False
default_nt=1


re_tosub = re.compile("{}")

#jje 01/2020
#executable to distribute multiple command-line jobs in a controlled way


try:
	possible_nt = sys.argv[1]#will throw error if no args


	if possible_nt.startswith("nt="):#first arg may indicate num cores to use (needs to be nt=12 or another integer)
		cmd_idx = 2
		fld, val = possible_nt.split("=")
		nt = val
	else:
		cmd_idx = 1
		nt = default_nt

	cmd = " ".join(sys.argv[cmd_idx:])
except:
	print("distribute.py your_command(arg on stdin with placeholder {})")
	exit(1)

cmds = list()

if not sys.stdin.isatty():#has stdin to sub in

	for line in sys.stdin.readlines():
		runthis, nummatch = re_tosub.subn(line.rstrip(), cmd)

		if do_throw and nummatch == 0:
			message = "ERROR: no match of '{}' in command provided.  no ability to sub in that from stdin.\n"
			raise Exception(message)

		cmds.append([runthis])

else:#run as single command
	cmds.append([cmd])

if do_print:
	for cmd in cmds:
		print("cmd: " + " | ".join(cmd))


if do_run:
	jobs_obj = jobs.Process(nt=nt, do_print=False, do_throw=do_throw, do_verbose=False, do_kill=do_kill)

	res = jobs_obj.run_pipes(cmds)

	pids = jobs_obj.pids

	for pid in pids:
		print("#INFO:\tprocess id: " + str(pid) + "\texit status: " + str(pids[pid]["returncode"]) + "\tstdout: '" + str(pids[pid]["stdout"]) + "'\tstderr: '" + str(pids[pid]["stderr"]) + "'\tcommand: '" + str(pids[pid]["cmd"]))
else:
	if do_print:
		for cmd in cmds:
			sys.stderr.write(cmd + "\n")

		sys.stderr.write("dry run.  did not make system calls.\n")

if do_print:
	sys.stderr.write("done.\n")

exit

