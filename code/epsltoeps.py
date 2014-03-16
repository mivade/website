#!/usr/bin/env python
import os, sys

def toEPS(fname):
    tex = r"""\documentclass[letterpaper,10pt]{article}
    \usepackage{graphicx}
    \usepackage{fullpage}
    \pagestyle{empty}
    \begin{document}
    \input{%s}
    \end{document}
    """ % fname

    texfile = open('tmp.tex', 'w')
    texfile.write(tex)
    texfile.close()

    os.system('latex tmp.tex')
    os.system('dvips -E -o %s tmp.dvi' % (fname.split('.')[0] + '_out.eps'))
    junk = ['tmp.log', 'tmp.tex', 'tmp.aux', 'tmp.dvi']
    for f in junk:
        os.remove(f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: epsltoeps.py <TeX file>"
        sys.exit(1)
    fname = sys.argv[1]
    toEPS(fname)
    
