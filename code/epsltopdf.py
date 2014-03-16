import os, sys
import epsltoeps as e

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: epsltopdf.py <TeX file>"
        sys.exit(1)
    fname = sys.argv[1]
    e.toEPS(fname)
    os.system('epstopdf %s' % (fname.split('.')[0] + '_out.eps'))
    os.remove(fname.split('.')[0] + '_out.eps')
