#!/usr/bin/env python

import json
import glob
import textwrap
import argparse
import os        # for removing temporary file
import shutil    # for making temp copy of calibration targets to be imported
import collections # for OrderedDict


# Map the short names that we need to use with PEST to the longer
# selection of keys that are used in the calibration_targets, configured_suites
# and dvmdostem json files.
# NOTES ON CONSTRUCTING:
#   A basic initialization of an OrderedDict doesn't work as expected, because 
#   defining a dict in-line does not preserve the initial order. So we have to
#   initialize it with a list of tuples. Gets messy for the nested aspect...

# First mapping. Works for targets2obs conversion, cause Nuptake is used in
# the targets file.
MAPPING1 = collections.OrderedDict(
  [
    ('mdc'     ,  'MossDeathC'),
    ('cshall'  ,  'CarbonShallow'),
    ('cdeep'   ,  'CarbonDeep'),
    ('cminsum' ,  'CarbonMineralSum'),
    ('onsum'   ,  'OrganicNitrogenSum'),
    ('ansum'   ,  'AvailableNitrogenSum' ),

    ('pftvars', collections.OrderedDict(
        [
          ('nppa'     , ['NPPAll']),
          ('tnup'     , ['Nuptake']),
          ('vcl'      , ['VegCarbon', 'Leaf']),
          ('vcs'      , ['VegCarbon', 'Stem']),
          ('vcr'      , ['VegCarbon', 'Root']),
          ('vsnl'     , ['VegStructuralNitrogen', 'Leaf']),
          ('vsns'     , ['VegStructuralNitrogen', 'Stem']),
          ('vsnr'     , ['VegStructuralNitrogen', 'Root']),
        ]
      )
    )
  ]
)

# Seem to need this one (which is basically the same as the other mapping)
# because of TotNitrogenUptake...can't decide if I should refactor this to
# Nuptake (or vice versa).
MAPPING2 = collections.OrderedDict(
  [
    ('mdc'     ,  'MossDeathC'),
    ('cshall'  ,  'CarbonShallow'),
    ('cdeep'   ,  'CarbonDeep'),
    ('cminsum' ,  'CarbonMineralSum'),
    ('onsum'   ,  'OrganicNitrogenSum'),
    ('ansum'   ,  'AvailableNitrogenSum' ),

    ('pftvars', collections.OrderedDict(
        [
          ('nppa'     , ['NPPAll']),
          ('tnup'     , ['TotNitrogenUptake']),
          ('vcl'      , ['VegCarbon', 'Leaf']),
          ('vcs'      , ['VegCarbon', 'Stem']),
          ('vcr'      , ['VegCarbon', 'Root']),
          ('vsnl'     , ['VegStructuralNitrogen', 'Leaf']),
          ('vsns'     , ['VegStructuralNitrogen', 'Stem']),
          ('vsnr'     , ['VegStructuralNitrogen', 'Root']),
        ]
      )
    )
  ]
)

# Given a list of keys, this function will return the item found in a nested
# dict by following the keys in the list.
def recursive_get(d, keys):
  if len(keys) == 1:
    return d[keys[0]]
  return recursive_get(d[keys[0]], keys[1:])


def caltargetvalues2pestobsvalues(caltargetsfile, outobsfile, cmtnum):
  '''Reads a calibration_targets file and writes a PEST "observation" file with data from calirbation_targets'''

  print textwrap.dedent('''??''')

  # bit of a hack, but allows importing calibration_targets.py as a module
  shutil.copy(caltargetsfile, "calibration_targets.py")
  import calibration_targets

  # find the right cmt data section, based on number
  for cmtname, data in calibration_targets.calibration_targets.iteritems():
    if data['cmtnumber'] == int(cmtnum):

      NUMPFTS = 8

      with open(outobsfile, 'w') as f:
        for key, value in MAPPING1.items():
          if key != 'pftvars':
            f.write('{0:<10} {1:>20}\n'.format(key, data[value]))
          else:
            pass

        for key, value in MAPPING1['pftvars'].items():
          for i in range(0, NUMPFTS):
            key_list = value[:]
            key_list.append(i)
            f.write('{0:}{1:<10} {2:>20}\n'.format(key, i, recursive_get(data, key_list)))

    else:
      pass # wrong CMT number

  os.remove("calibration_targets.py")
  os.remove("calibration_targets.pyc")

def dvmdostemjson2pestobs(outfile, data_root='/tmp/dvmdostem'):

  path = os.path.join(data_root, 'calibration/yearly/')

  NUMPFTS = 8
  files = sorted( glob.glob('%s/*.json' % path) )
  print "Found %s files." % (len(files)) 

  # Open the last file.
  # NOTE: May want to take average of last X files (years)??
  print "Reading from: %s" % (files[-1]) 
  with open(files[-1]) as f:
    fdata = json.load(f)

  print "Writing simplified outputs to: %s" % (outfile) 
  with open(outfile, 'w') as f:
    f.write("Variable,Value\n")

    for key, value in MAPPING2.items():
      if key != 'pftvars':
        f.write('{0:},{1:}\n'.format(key, fdata[value]))
      else:
        pass

    for key, value in MAPPING2['pftvars'].items():
      for i in range(0, NUMPFTS):
        pftkey = 'PFT%s' % i
        key_list = value[:]
        key_list.insert(0, pftkey)
        f.write('{0:}{1:},{2:}\n'.format(key, i, recursive_get(fdata, key_list)))


def build_ins(outfile):

  NUMPFTS = 8
  print "Writing instruction file to: %s" % (outfile)
  print "DOUBLE CHECK! --> instruction file must match simplified outputs!"
  with open(outfile, 'w') as f:
    f.write("pif @\n")
    f.write("l1 @,@ !mdc!\n")
    f.write("l1 @,@ !cshall!\n")
    f.write("l1 @,@ !cdeep!\n")
    f.write("l1 @,@ !cminsum!\n")
    f.write("l1 @,@ !onsum!\n")
    f.write("l1 @,@ !ansum!\n")
    
    for i in range(0, NUMPFTS):
      #f.write("l1 @,@ !gppain%s!\n" % (i))
      #f.write("l1 @,@ !nppain%s!\n" % (i))
      f.write("l1 @,@ !nppa%s!\n" % (i))
      f.write("l1 @,@ !tnup%s!\n" % (i))
      f.write("l1 @,@ !vcl%s!\n" % (i))
      f.write("l1 @,@ !vcs%s!\n" % (i))
      f.write("l1 @,@ !vcr%s!\n" % (i))
      f.write("l1 @,@ !vsnl%s!\n" % (i))
      f.write("l1 @,@ !vsns%s!\n" % (i))
      f.write("l1 @,@ !vsnr%s!\n" % (i))

  # This seems a bit of a hack, but we need to 
  # replace the seconds line of the file with a l2 instead of l1
  # for the pest "line advance" function.
  # So we open the file, read it, modify the data, and write it back
  with open(outfile, 'r') as f:
    data = f.readlines()

  data[1] = "l2 @,@ !mdc!\n"

  with open(outfile, 'w') as f:
    f.writelines(data)

  # Example:
  '''
  pif @
  l2 @,@ !mdc!
  l1 @,@ !cshall!
  ....
  '''


if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
      ???
      ''')
  )
  parser.add_argument('--json-to-obs', nargs=1, metavar=('outputfile'), 
      help=textwrap.dedent('''Translate dvm-dos-tem calibration json file into simplified csv file for parsing with PEST ins file.'''))

  parser.add_argument('--pid-tag', nargs=1, metavar=('PIDTAG'),
      help=textwrap.dedent("""Look for json files in '/tmp/dvmdostem-%(metavar)s'"""))

  parser.add_argument('--build-ins', nargs=1, metavar=('outputfile'),
      help=textwrap.dedent('''Create an instruction file for reading a simplfied csv file.'''))

  parser.add_argument('--targets2obs', nargs=1, metavar=('outputfile'),
      help=textwrap.dedent('''Copy values from a calibration_targets.py file into a .obf file.'''))

  parser.add_argument('--json-location', nargs=1, metavar=('jsonlocation'),
      help=textwrap.dedent('''The root location for the expected json file tree'''))

  args = parser.parse_args()
  print args

  if args.pid_tag and (not args.json_to_obs):
  	print "If you pass a pid tag, you must also use --json-to-obs. Quitting."
  	exit(-1)

  if args.json_to_obs:
    
    if args.json_location:
      root_loc = args.json_location[0]
    else:
      root_loc = '/tmp/'  
    print "Looking to this for root of expected calibraiton json file tree: %s" % (root_loc)
    if args.pid_tag:
      drt = os.path.join(root_loc, 'dvmdostem-%s'%(args.pid_tag[0]))
    else: 
      drt = os.path.join(root_loc, 'dvmdostem')

    dvmdostemjson2pestobs(args.json_to_obs[0], data_root=drt)

  if args.build_ins:
    build_ins(args.build_ins[0])

  if args.targets2obs:
    caltargetvalues2pestobsvalues("../../dvm-dos-tem/calibration/calibration_targets.py", args.targets2obs[0], 5)

# ./pest-helper.py --json2obs 
# ./pest-helper.py --build-ins path/to/??
# ./pest-helper.py --caltargets2obs path

