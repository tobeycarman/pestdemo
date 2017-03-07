#!/usr/bin/env python

# Tobey Carman
# November 2016

# Make plots of PEST parameter values.
import os
import argparse
import textwrap

import numpy as np
import matplotlib.pyplot as plt
import itertools

def plot_ipar(ifname, save_name, format, no_show):

  with open(ifname, 'r') as f:
    pdata = np.genfromtxt(f, skip_header=1, delimiter=",",)

  # Grab the header text (column names)
  with open(ifname, 'r') as f:
    alldata = f.readlines()
    cols = [i.strip() for i in alldata[0].split(",")]

  fig, ax = plt.subplots()

  marker = itertools.cycle(['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd'])
  
  for i, row in enumerate(pdata):
    ax.plot(pdata[i, 1:], linestyle='', marker=marker.next(), markersize=6.5, alpha=0.75, label="param set %s" % i)

  plt.yscale('log')
  plt.xticks(range(0, len(cols[1:])), cols[1:], rotation=90, fontsize='x-small')
  plt.grid()
  plt.legend()

  if not no_show:
    plt.show(block=True)

  if save_name != "":
    full_name = args.save_name + "plot-ipar." + args.format
    plt.savefig(full_name)


def plot_isen(ifname, save_name, format, no_show):
  with open(ifname, 'r') as f:
    sdata = np.genfromtxt(f, skip_header=1, delimiter=",",)

  with open(ifname, 'r') as f:
    alldata = f.readlines()
    cols = [i.strip() for i in alldata[0].split(",")]

    # labeled array, access labels with sdata.dtype.names or sdata['cmax0']
    # [ [cmax0, cmax1, cmax2, ....],
    #   [cmax0, cmax1, cmax2, ....], ]

  num_subplots = len(sdata)
  if num_subplots > 10:
    print "WARNING! Looks like PEST did a lot of runs!"
    print "WARNING! Maybe you need a different plot layout..."

  fig, axar = plt.subplots(num_subplots,1)

  lefts = np.arange(0, 4*len(sdata[0,1:]), 4)
  centers = 1+lefts # not using this

  for opt_it, ax in enumerate(axar):
    #md = np.ma.masked_less(sdata[opt_it, 1:], 10e-4)
    ax.bar(lefts, sdata[opt_it, 1:], width=3.5, align='center')
    ax.set_yscale('log')

  for ax in axar:
    ax.set_xticks([])

  last_ax = axar[-1]
  last_ax.set_xticks(lefts)
  last_ax.xaxis.set_ticklabels(cols[1:], rotation=90)

  if not no_show:
    plt.show(block=True)

  if save_name != "":
    full_name = args.save_name + "plot-isen." + args.format
    plt.savefig(full_name)




if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    description = "Make plots of various PEST files."
  )

  parser.add_argument('-f', '--file', default='', type=str, help="the file to plot")
  parser.add_argument('-s', '--save-name', default="", type=str, help="the file name to save plot as")
  parser.add_argument('-m', '--format', default="pdf", choices=['pdf', 'png'], help="the image format to save as")
  parser.add_argument('-n', '--no-show', action='store_true', help="Don't display the plot(s)")

  #parser.add_argument('t', '--type', choices=['ipar','postcov','residuals','isen'], help="which plot to make" )
  
  args = parser.parse_args()
  
  infile_base = os.path.basename(args.file)
  infile_bare_name, infile_ext = os.path.splitext(infile_base)

  if '.ipar' == infile_ext:
  	plot_ipar(args.file, args.save_name, args.format, args.no_show)

  if '.isen' == infile_ext:
  	plot_isen(args.file, args.save_name, args.format, args.no_show)





