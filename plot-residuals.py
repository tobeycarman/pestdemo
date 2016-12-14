#!/usr/bin/env python

# Tobey Carman, November 2016

import numpy as np
import matplotlib.pyplot as plt

import argparse


def main(file_list):

	color_list = []

	for f in file_list:
		data = np.genfromtxt(f, skiprows=4)
		weights = data[:,5]
		measured = data[:,2]
		modeled = data[:,3]
		residuals = data[:,4]

		plt.plot(measured*weights, modeled*weights, marker='o', linestyle='', label=f.split('/')[-1])

		#plt.scatter(measured*weights, modeled*weights alpha=.15)


	plt.legend()
	plt.show()

	



if __name__ == '__main__':
	
  parser = argparse.ArgumentParser(
  	description = "Make plots of PESTPP residual (.rei) files."
  )

  parser.add_argument('-f', '--files', default='', nargs="+", type=str, help="the file(s) to plot")

  args = parser.parse_args()
  
  main(args.files)
