#!/usr/bin/env python

# mdscript.py
# Version 0.1.4
# 2008-02-29

# Original author: Michael V. De Palatis <em vee dee at gatech dot edu>
# Contributions also by John R. Dowdle <jay arr dee at vtmu dot net>
# (see CHANGELOG for further details)

# You may freely distribute this script under the GNU GPLv2.

# This script invokes markdown to process markdown text into
# XHTML-compliant files. It will also intelligently place necessary
# tags, such as <title> without putting it in <p> environments.

# If an html file already exists, there is no need to specify what the
# <title> should be, as this script will just reuse the old one unless
# explicitly overridden.

# See the usage function below for usage information.

###########
##IMPORTS##
###########

import os
import os.path
import sys
import re
import datetime
from getopt import *

#############
##CONSTANTS##
#############

VERSION = "0.1.4"

# The command to call. Sometimes this might be markdown.pl.
MARKDOWN_CMD = "markdown"

# Change this if you use something else.
DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
## DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
## DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">'
## DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
## DOCTYPE = '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 2.0//EN" "http://www.w3.org/TR/MathML2/dtd/mathml2.dtd">'

# Change this html tag if you're using something somewhat different.
HTMLTAG = '<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">'

# Any kind of metadata that you might need.
# Just put a \n and another meta tag if you need/want more.
# This is a good place to put stylesheets, e.g.
META = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>'

# Format for appended "modified on" date.
FORMAT = "%d %B %Y"

# These are both True if you are using headers and footers.
HEADER = True
FOOTER = True

#############
##FUNCTIONS##
#############

# Print usage information.
def usage():
    print """
Usage: mdscript.py [options] <markdown file>
Options:
	-h		Print help information and quit.
	-v		Print version number and quit.
	-t <title text> Set the title of the resultant HTML page. This
         is not necessary to be called if the HTML file already
         exists, as mdscript will grab the old title to use again
         unless -t is used explicitly.
	-n		Do not use the <!DOCTYPE...> tag.
        
        -d		Do not append the last modified date to the
          HTML file.
        --bg-color <color>	Background color of the page
        --text-color <color>    Text color
        --link-color <color>    Link color
        --vlink-color <color>   Visited link color
    """

########
##MAIN##
########

# Get options.

tmp_opts, filename = getopt(sys.argv[1:], "hvt:nd",
                            ['bg-color=','text-color=','link-color=',
                             'vlink-color=', "no-header", "no-footer"])
opts = {}
for key, value in tmp_opts:
    opts[key] = value
    
# Process options.
title = ""
body_string = ""
use_doctype = True
append_date = True

if opts.has_key('-h'):
    usage()
    sys.exit(1)
    
if opts.has_key('-v'):
    print "\nmdscript.py version %s" % VERSION
    print "This script is available under the GNU GPL version 2.\n"
    sys.exit(1)

if len(filename) < 1:
    print "No file specified."
    usage()
    sys.exit(0)

if opts.has_key('-t'):
    title = opts['-t']

if opts.has_key('-n'):
    use_doctype = False

if opts.has_key('-d'):
    append_date = False

if opts.has_key('--bg-color'):
    bg_color = opts['--bg-color']
    body_string += ' bgcolor="%s"'%bg_color

if opts.has_key('--text-color'):
    text_color = opts['--text-color']
    body_string += ' text="%s"'%text_color    

if opts.has_key('--link-color'):
    link_color = opts['--link-color']
    body_string += ' link="%s"'%link_color    

if opts.has_key('--vlink-color'):
    vlink_color = opts['--vlink-color']
    body_string += ' vlink="%s"'%vlink_color

if opts.has_key("--no-header"):
    HEADER = False

if opts.has_key("--no-footer"):
    FOOTER = False

# Separate filename from extension.
tmp = filename[0].split('.')
try:
    name = tmp[0]
    extension = tmp[1]
except:
    print "Whoops. Maybe the file didn't have an extension?"
    sys.exit(0)

# Does the html file already exist?
if os.path.exists(name + ".html"):	#TODO: Make this work for other extensions.
    exists = True
else:
    exists = False

# Process the file using markdown.
markdown_processed_raw = os.popen(MARKDOWN_CMD + ' ' + filename[0])
markdown_processed_text = markdown_processed_raw.read()

# Process headers and footers.
header_processed_text = ""
footer_processed_text = ""

if HEADER:
    if os.path.exists("header.txt"):
        #header_processed_raw = os.popen(MARKDOWN_CMD + ' ' + "header.txt")
        #header_processed_text = header_processed_raw.read()
        #header_processed_raw = os.popen("header.txt")
        header_file = open("header.txt")
        header_processed_text = header_file.read(-1)
        header_file.close()
if FOOTER:
    if os.path.exists("footer.txt"):
        #footer_processed_raw = os.popen(MARKDOWN_CMD + ' ' + "footer.txt")
        #footer_processed_text = footer_processed_raw.read()
        footer_file = open("footer.txt")
        footer_processed_text = footer_file.read(-1)
        footer_file.close()

# Affix the title and doctype.
if use_doctype:
    pre_text = "%s\n%s\n<head>\n%s\n" % (DOCTYPE, HTMLTAG, META)
else:
    pre_text = "%s\n<head>\n%s\n" % (HTMLTAG, META)
    
main_text = "<body" + body_string + ">\n%s%s%s" % (header_processed_text, markdown_processed_text, footer_processed_text)
post_text = "</body>\n</html>"

if append_date:
    date = datetime.date.today().strftime(FORMAT)
    main_text = main_text + "\n<p><i>Last updated %s</i></p>" % date

if not exists or title != "":	# We also want to allow manual overrides.
    title_text = "<title>%s</title>\n</head>\n" % title
    
else:

    # Make regex's to find what's between the title tags.
    re_start = re.compile(r"<title>", re.IGNORECASE)
    re_end = re.compile(r"</title>", re.IGNORECASE)

    # Read the html file.
    infile = open(name + ".html", 'r')
    html_text = infile.read()
    infile.close()

    # Search for the tags.
    start = re_start.search(html_text)
    end = re_end.search(html_text)

    # Make sure the title tags were actually found.
    if start and end:
        title = html_text[start.end():end.start()]
    else:
        title = ""

    title_text = "<title>%s</title>\n</head>\n" % title
    
markdown_processed = pre_text + title_text + main_text + post_text

# Write the file and quit.
outfile = open(name + ".html", 'w')
outfile.write(markdown_processed)
outfile.close()
