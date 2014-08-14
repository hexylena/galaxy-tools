#!/usr/bin/env python
import sys

failure_type = sys.argv[1]

if failure_type == 'raise':
	raise Exception("you asked for it")
elif failure_type == 'sysexit':
	sys.exit(1)
else:
	raise Exception("Really? Really???")
