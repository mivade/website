#!/usr/bin/env python
#
# orgmusic - A simple music organizing script.
# Version 0.1.1
#
# Written January 2006 by Michael V. De Palatis <mdepalatis@mail.utexas.edu>
# This program is freely distributable under the terms of the GNU GPL.
#
# Usage:	orgmusic.py [options] -p path
# Options:	-h:	Print help and exit.
#		-v:	Print version and exit.
#
# !!!WARNING!!!
# I can make NO GUARANTEE that this won't erase stuff. It's not supposed to, and it
# doesn't for me, but consider yourself warned.
#
# TODO: "Neater" organizing, i.e., look for similar names.

###########
##IMPORTS##
###########

import sys
import getopt
import os.path
import dircache
import re
import pyid3lib

#############
##CONSTANTS##
#############

VERSION = "0.1.1"

#############
##FUNCTIONS##
#############

# Main function.
def main():

	# Get command line arguments.
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvp:")
	except getopt.GetoptError:
		printhelp()
		print "\nInvalid option. Exiting."
		sys.exit(0)

	# Process options.
	for opt, arg in opts:

		# Help.
		if opt in ['-h']:
			printhelp()
			sys.exit(1)

		# Version.
		elif opt in ['-v']:
			print "orgmusic version " + VERSION

		# Path.
		elif opt in ['-p']:
			path = arg

			# Verify that the path is valid.
			if not os.path.exists(path):
				print "Invalid path. Exiting."
				sys.exit(0)
			else:

				# Make into an absolute path.
				path = os.path.abspath(path)
				
				# Organize.
				organize(path)

# Prints help.
def printhelp():
	print "orgmusic version " + VERSION
	print "Usage: orgmusic.py [options] -p path"
	print "Options:\t-h: Print help.\n\t\t-v: Print version number."
	print '\norgmusic takes the specified path and organizes the MP3 files contained in it. "Organization" means that the MP3 files are placed in directories named after the artist.'

# Organizes the music.
def organize(path):

	# Get a list of the given directory.
	contents = dircache.listdir(path)

	# Organize the MP3 files.
	# Valid extensions are mp3, MP3, Mp3, and mP3.
	for file in contents:

		# Get extension.
		ext = file[len(file) - 3:len(file)]

		# If an MP3 file, perform organization. Otherwise go to the next file.
		if ext not in ['mp3', 'MP3', 'Mp3', 'mP3']:
			continue
		else:

			# Access the ID3 tag.
			try:
				tag = pyid3lib.tag(path + '/' + file)
				artist = tag.artist.replace('\0', '')

				# Get rid of "bad" characters.
				# Allowable characters: Alphanumeric, _, -, and .
				regex = re.compile('[^-_.\d\w]')
				artist = re.sub(regex, '', artist)
				
			except AttributeError:
				print "WARNING: " + file + " does not appear to have an artist tag. Skipping."
				continue

			# Move the file to the directory path/artist/file.
			oldfile = path + '/' + file 
			newdir = path + '/' + artist
			newfile = newdir + '/' + file
			os.path.normpath(newdir)
			if not os.path.exists(newdir):
				os.mkdir(newdir)
			if os.path.exists(newfile):
				print "WARNING: " + newfile + " already exists. Skipping."
				continue
			else:
				os.rename(oldfile, newfile)

# Run the main program.
if __name__ == "__main__":
	main()
