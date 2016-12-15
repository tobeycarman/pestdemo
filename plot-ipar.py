#!/usr/bin/env python

# Tobey Carman
# November 2016

# Make plots of PEST parameter values.

import argparse
import textwrap

import numpy as np
import matplotlib.pyplot as plt
import itertools


#def read_data(fname):


#def dot_plot(fname)


def main(fname):

  #fname = "/Users/tobeycarman/Downloads/oct-10-pestpp-posterior-results/master-00000/tussock_full.isen"

  with open(fname, 'r') as f:
    pdata = np.genfromtxt(f, skip_header=1, delimiter=",",)

  # Grab the header text (column names)
  with open(fname, 'r') as f:
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

  plt.show(block=True)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    description = "Make plots of PESTPP parameter (.ipar) file."
  )

  parser.add_argument('-f', '--file', default='', type=str, help="the file to plot")

  args = parser.parse_args()
  
  main(args.file)


