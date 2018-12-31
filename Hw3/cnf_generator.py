import sys
import random

argument_str = """ Random CNF generator
                   ====================
                   This program is run from the command line with arguments:
                   php cnf_generator.php $num_variables $num_clauses $max_width
                   Its output format matches that used by satcompetition.org
               """

cnf_str = """c
c Random CNF in satcompetition.org format created by cnf_generator.php
c
p cnf %s %s
"""

if len(sys.argv) < 4:
	print argument_str
	sys.exit(0)

num_variables = int(sys.argv[1])
num_clauses = int(sys.argv[2])
max_width = int(sys.argv[3])

formated_cnf_str = cnf_str%(num_variables, num_clauses)
print formated_cnf_str
for i in range(num_clauses+1):
	out = {}
	for j in range(1, max_width+1):
		k = random.randint(1, num_variables)
		if random.randint(0,1):
			out[k] = k
		else:
			out[k] = -k
	my_str = " ".join(str(x) for x in out.values()) + " 0"
        print my_str
