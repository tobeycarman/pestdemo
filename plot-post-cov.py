#!/usr/bin/env python

# Tobey Carman
# late december 2016


import argparse
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.colors as colors

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid


# Copied directly from here:
# http://stackoverflow.com/questions/7404116/defining-the-midpoint-of-a-colormap-in-matplotlib
# I can't get it to work the way I want...
def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

############################

def main(files):

  with open(files[0], 'r') as f:
      data = [line.rstrip('\n') for line in f.readlines()]

  # Look for the beginning of the row/col name section,
  # grab all lines till the end.
  r0 = data.index("* row and column names")
  names = data[r0+1:]

  # Look for the beginning of the space delimited data section
  r1 = data.index("Outer pointers:")
  subdata = data[r1+3:r0]


  # Go thru every line in the sub data, take off the extra space at the end,
  # split in to values, interpert the values as floats, and return 2D list
  sd  = [map(float, l.rstrip(' ').split(' ')) for l in subdata]

  sd2 = np.array(sd)

  ax = plt.gca()
  ax.xaxis.set_tick_params(names, labeltop='on')
  ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(0,sd2.shape[0])))
  ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(0,sd2.shape[1])))
  ax.set_xticklabels(names, rotation=90, ha='center')
  ax.set_yticklabels(names)
  ax.grid('off')


  # Can't quite get this to work
  mp = 1 - sd2.max() / (sd2.max() + abs(sd2.min()))
  shifted_cmap = shiftedColorMap(plt.cm.RdBu_r, midpoint=mp, name='shifted')
  #plt.imshow(sd2, cmap=shifted_cmap, norm=colors.SymLogNorm(linthresh=1, linscale=1, vmin=-sd2.max(), vmax=sd2.max()), interpolation='none')
  plt.imshow(sd2, cmap=plt.cm.RdBu_r, norm=colors.SymLogNorm(linthresh=1, linscale=1, vmin=-sd2.max(), vmax=sd2.max()), interpolation='none')


  plt.colorbar( ticks=[sd2.min(), -10e1, -1, 0, 1, 10e1, sd2.max()] ) #matplotlib.ticker.SymmetricalLogLocator(matplotlib.transforms.IdentityTransform) )

  # Handle showing data and axis coords in lower right corner of interactive window
  numrows, numcols = sd2.shape
  def format_coord(x, y):
      col = int(x+0.5)
      row = int(y+0.5)
      if col>=0 and col<numcols and row>=0 and row<numrows:
          z = sd2[row,col]
          return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
      else:
          return 'x=%1.4f, y=%1.4f'%(x, y)

  ax.format_coord = format_coord



  plt.show(block=True)

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(
    description = "Make plots of PESTPP covariance files ('*.post.cov')."
  )

  parser.add_argument('-f', '--files', default='', nargs="+", type=str, help="the file(s) to plot")

  args = parser.parse_args()
  
  main(args.files)








