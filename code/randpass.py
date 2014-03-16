#!/usr/bin/env python
#
# randpass - A command line random password generator.
# Version 0.1.0
#
# Written January 2006 by Michael V. De Palatis <mdepalatis@mail.utexas.edu>
# This program is freely distributable under the terms of the GNU GPL.
#
# Usage: 	randpass [options] num_chars
# Options:	None yet!

###########
##IMPORTS##
###########

import sys
import random
import time
import traceback

#############
##FUNCTIONS##
#############

# Main program.
def main():
	try:

		# Parse command line arguments.
		# (Or really for now, just see how many characters to use).
		num_chars = int(sys.argv[1])	# The first argument is the file name.

		# Build the password.
		print genpass(num_chars)
	
	except:
		print "Some error has occurred. Oops."
		traceback.print_exc()
		traceback.print_stack()

# Generate the password.
def genpass(num_chars):

	# Password to be built.
	password = ""

	# Build the password.
	random.seed(time.time())
	for i in range(1, num_chars):

		# Choose a character.
		ch = chr(random.randint(ord('!'), ord('z')))
		
		# Add to the password.
		password += ch

	return password

# Run the main program.
if __name__ == "__main__":
	main()
