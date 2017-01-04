#!/usr/bin/env python

# Tobey Carman, November 2016

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial

import argparse

def fmt(x, y):
    return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x=x, y=y)

class FollowDotCursor(object):
    """Display the x,y location of the nearest data point.
    http://stackoverflow.com/questions/20637113/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib-in-stem
    http://stackoverflow.com/a/4674445/190597 (Joe Kington)
    http://stackoverflow.com/a/13306887/190597 (unutbu)
    http://stackoverflow.com/a/15454427/190597 (unutbu)
    """
    def __init__(self, ax, x, y, tolerance=5, formatter=fmt, offsets=(-20, 20)):
        try:
            x = np.asarray(x, dtype='float')
        except (TypeError, ValueError):
            x = np.asarray(mdates.date2num(x), dtype='float')
        y = np.asarray(y, dtype='float')
        mask = ~(np.isnan(x) | np.isnan(y))
        x = x[mask]
        y = y[mask]
        self._points = np.column_stack((x, y))
        self.offsets = offsets
        y = y[np.abs(y-y.mean()) <= 3*y.std()]
        self.scale = x.ptp()
        self.scale = y.ptp() / self.scale if self.scale else 1
        self.tree = spatial.cKDTree(self.scaled(self._points))
        self.formatter = formatter
        self.tolerance = tolerance
        self.ax = ax
        self.fig = ax.figure
        self.ax.xaxis.set_label_position('top')
        self.dot = ax.scatter(
            [x.min()], [y.min()], s=130, color='green', alpha=0.7)
        self.annotation = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def scaled(self, points):
        points = np.asarray(points)
        return points * (self.scale, 1)

    def __call__(self, event):
        ax = self.ax
        # event.inaxes is always the current axis. If you use twinx, ax could be
        # a different axis.
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
        elif event.inaxes is None:
            return
        else:
            inv = ax.transData.inverted()
            x, y = inv.transform([(event.x, event.y)]).ravel()
        annotation = self.annotation
        x, y = self.snap(x, y)
        annotation.xy = x, y
        annotation.set_text(self.formatter(x, y))
        self.dot.set_offsets((x, y))
        bbox = ax.viewLim
        event.canvas.draw()

    def setup_annotation(self):
        """Draw and hide the annotation box."""
        annotation = self.ax.annotate(
            '', xy=(0, 0), ha = 'right',
            xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
            bbox = dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
            arrowprops = dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    def snap(self, x, y):
        """Return the value in self.tree closest to x, y."""
        dist, idx = self.tree.query(self.scaled((x, y)), k=1, p=1)
        try:
            return self._points[idx]
        except IndexError:
            # IndexError: index out of bounds
            return self._points[0]



def histoplot_normal(ax, data, titlestring):
   num_bins= 15
   n, bins, patches = ax.hist(data, num_bins, normed=1, facecolor='blue', alpha = 0.5)
   #y = mlab.normpdf(bins, np.mean(data), np.std(data))
   #plt.plot(bins, y, 'k--')
   ax.axvline(x=np.median(data), linewidth=1, color='r')
   ax.axvline(x=np.mean(data), linewidth=1, color='k')
   ax.set_title(titlestring, fontsize=14)
   ax.set_xlabel('residuals', fontsize=14)
   ax.set_ylabel('probability density', fontsize=14)
   ax.tick_params(axis='x', labelsize=14)
   ax.tick_params(axis='y', labelsize=14)




def main(file_list):

  color_list = ['blue','red','green','black','orange','yellow','magenta','cyan']

  fig, ax = plt.subplots()

  for i, f in enumerate(file_list):
    data = np.genfromtxt(f, skip_header=4)
    weights = data[:,5]
    measured = data[:,2]
    modeled = data[:,3]
    residuals = data[:,4]
    names = data[:,0]
    groups = data[:,1]

    print "Plotting %s data for file '%s'" % (color_list[i], f)
    ax.scatter(measured*weights, modeled*weights, marker='o', color=color_list[i], alpha=0.30, label="file %s" % (i))
    # Maybe plot is faster?
    #ax.plot(measured*weights, modeled*weights, marker='o', linestyle='', color=color_list[i], alpha=0.30, label="file %s" % (i))

  plt.title("Measured vs Modeled")  

  #ax.xlabel("Measured")
  #ax.ylabel("Modeled")
  plt.legend()

  cursor = FollowDotCursor(ax, measured*weights, modeled*weights, tolerance=20)


  fig2, ax2 = plt.subplots()
  histoplot_normal(ax2, residuals*weights, "WTF")

  
  plt.show(block=False)
  from IPython import embed; embed()

  



if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(
    description = "Make plots of PESTPP residual (.rei) files."
  )

  parser.add_argument('-f', '--files', default='', nargs="+", type=str, help="the file(s) to plot")

  args = parser.parse_args()
  
  main(args.files)
