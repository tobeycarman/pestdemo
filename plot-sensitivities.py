#!/usr/bin/env python

# Tobey Carman
# November 2016

# Make plots of PEST Sensitivity values.

import argparse
import textwrap

import numpy as np
import matplotlib.pyplot as plt


def read_data(fname):


def dot_plot(fname)


def main(fname):

	#fname = "/Users/tobeycarman/Downloads/oct-10-pestpp-posterior-results/master-00000/tussock_full.isen"

	with open(fname, 'r') as f:
		sdata = np.genfromtxt(f, skiprows=1, delimiter=",",)

	with open(fname, 'r') as f:
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

	plt.show(block=True)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(
  	description = "Make plots of PESTPP sensitivity (.isen) files."
  )

  parser.add_argument('-f', '--file', default='', type=str, help="the file to plot")

  args = parser.parse_args()
  
  main(args.file)


