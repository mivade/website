"""
mplparams.py

M.V. DePalatis, 2010-09-01
Licensed under the GNU GPL v3

matplotlib rc params and axes rects to generate figures of appropriate
size for different types of publication.
"""

# documentclass 'article' with package 'fullpage'
fullpage = {'params': {'axes.labelsize': 10,
                       'text.fontsize': 10,
                       'legend.fontsize': 10,
                       'xtick.labelsize': 8,
                       'ytick.labelsize': 8,
                       'text.usetex': False,
                       'font.family': 'serif',
                       'figure.figsize': (4.774, 2.950)},
            'axes': [0.150,0.175,0.95-0.15,0.95-0.25]}

# two-column APS journal format
aps = {'params': {'axes.labelsize': 10,
                  'text.fontsize': 10,
                  'legend.fontsize': 10,
                  'xtick.labelsize': 8,
                  'ytick.labelsize': 8,
                  'text.usetex': False,
                  'figure.figsize': (3.4039, 2.1037)},
       'axes': [0.125,0.2,0.95-0.125,0.95-0.2]}
       
