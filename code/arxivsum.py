"""arxivsum.py

A simple script to read specific arXiv RSS feeds daily and send new
entries to your inbox.

This script is distributed under the terms of the GNU GPL v2.

Last update: 2009-06-04
"""

import os, os.path, re, smtplib, feedparser

def StripHTML(s):
    """Stripts all HTML tags from string s. This is *not* very
    intelligent... So anything contained in angle brackets will be
    removed."""
    p = re.compile(r"<.*?>")
    return p.sub('', s)

def Unobfuscate(email):
    """Unobfuscates email addresses."""
    at = re.compile("<ATATAT>")
    dot = re.compile("<DOTDOTDOT>")
    email = at.sub("@", email)
    return dot.sub(".", email)

# List the arXiv categories you want here.
categories = ["quant-ph", "physics.atom-ph", "physics.optics"]

# Where to store history file (to keep track of what was sent yesterday)
history_file = os.environ['HOME'] + '/.arxivsum.hist'
if not os.path.exists(history_file):
    hist = ['']
else:
    histf = open(history_file, 'r')
    hist = histf.readlines()
    for i, item in enumerate(hist):
        hist[i] = item.strip()
    histf.close()
histf = open(history_file, 'w')

# Set to False if you want HTML in your messages.
strip_html = True

# SMTP settings. I have only tried this on Debian machines which by
# default install an SMTP server. To use a remote server, see the
# documentation for the smtplib module.
smtp_server = "localhost"
smtp_port = 25

# Use <ATATAT> for @ sign and <DOTDOTDOT> for . in order to obfuscate
# emails from bots... But you don't have to.
smtp_from = Unobfuscate("depalatis<ATATAT>gmail<DOTDOTDOT>com")
smtp_to = smtp_from
    
# Grab each rss feed
feeds = []
for category in categories:
    print "Retrieving arXiv/%s..." % category
    feeds.append(feedparser.parse("http://arxiv.org/rss/%s" % category))

# Go through each feed item and extract today's updates
body = "SUBJECT: arXiv Updates\n"
print "Parsing feeds..."
new_count = 0
for feed in feeds:
    items = feed["items"]
    title = feed["channel"]["title"]
    body +=  title + "\n" + "="*len(title) + "\n\n"
    for item in items:
        item_id = item["id"].split('/')[-1]
        if item_id in hist:
            # We assume that all following entries have already been
            # seen, so quit parsing this feed.
            break
        else:
            histf.write(item_id + '\n')
            new_count += 1
        body += "Title: " + item["title"] + "\n"
        body += "Authors: " + StripHTML(item["author"]) + "\n"
        body += "Link: " + item["link"] + "\n"
        if strip_html:
            abstract = StripHTML(item["summary"])
        else:
            abstract = item["summary"]
        body += "Abstract:\n" + abstract + "\n\n"
    body += "---\n\n"
histf.close()

print new_count, "new items"
if new_count != 0:
    print "Sending summary... ",
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.sendmail(smtp_from, [smtp_to], body)
        smtp.quit()
    except SMTPConnectError:
        print "Error connecting to SMTP server."
    print "Done."
