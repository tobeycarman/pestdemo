#!/usr/bin/env python

import json
import glob
import textwrap
import argparse
import os        # for removing temporarty file
import shutil    # for making temp copy of calibration targets to be imported


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

        # Non pft stuff
        f.write('{0:<10} {1:>20}\n'.format('mdc', data['MossDeathC'])) # is MossdeathCarbon in calibration json files
        f.write('{0:<10} {1:>20}\n'.format('cshall', data['CarbonShallow'])) 
        f.write('{0:<10} {1:>20}\n'.format('cdeep', data['CarbonDeep']))
        f.write('{0:<10} {1:>20}\n'.format('cminsum', data['CarbonMineralSum']))
        f.write('{0:<10} {1:>20}\n'.format('onsum', data['OrganicNitrogenSum']))
        f.write('{0:<10} {1:>20}\n'.format('ansum', data['AvailableNitrogenSum']))

        # pft stuff
        for i in range(0, NUMPFTS):
          #f.write('gppain{0:<10} {1:>20}\n'.format(i, data['GPPAllIgnoringNitrogen'][i])) 
          #f.write('nppain{0:<10} {1:>20}\n'.format(i, data['NPPAllIgnoringNitrogen'][i]))
          f.write('nppa{0:<10} {1:>20}\n'.format(i, data['NPPAll'][i]))
          f.write('tnup{0:<10} {1:>20}\n'.format(i, data['Nuptake'][i]))
          f.write('vcl{0:<10} {1:>20}\n'.format(i, data['VegCarbon']['Leaf'][i]))
          f.write('vcs{0:<10} {1:>20}\n'.format(i, data['VegCarbon']['Stem'][i]))
          f.write('vcr{0:<10} {1:>20}\n'.format(i, data['VegCarbon']['Root'][i]))
          f.write('vsnl{0:<10} {1:>20}\n'.format(i, data['VegStructuralNitrogen']['Leaf'][i]))
          f.write('vsns{0:<10} {1:>20}\n'.format(i, data['VegStructuralNitrogen']['Stem'][i]))
          f.write('vsnr{0:<10} {1:>20}\n'.format(i, data['VegStructuralNitrogen']['Root'][i]))

    else:
      pass

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

    # Non pft stuff
    f.write('mdc,%s\n' % (fdata['MossdeathCarbon'])) # is MossDeathC in calibration_targets.py
    f.write('cshall,%s\n' % (fdata['CarbonShallow']))
    f.write('cdeep,%s\n' % (fdata['CarbonDeep']))
    f.write('cminsum,%s\n' % (fdata['CarbonMineralSum']))
    f.write('onsum,%s\n' % (fdata['OrganicNitrogenSum']))
    f.write('ansum,%s\n' % (fdata['AvailableNitrogenSum']))

    # pft stuff
    for i in range(0, NUMPFTS):
      pftkey = 'PFT%i' % (i)
      #f.write('gppain%s,%s\n' % (i, fdata[pftkey]['GPPAllIgnoringNitrogen']))
      #f.write('nppain%s,%s\n' % (i, fdata[pftkey]['NPPAllIgnoringNitrogen']))
      f.write('nppa%s,%s\n' % (i, fdata[pftkey]['NPPAll']))
      f.write('tnup%s,%s\n' % (i, fdata[pftkey]['TotNitrogenUptake'])) # is Nuptake in calibration_targets.py
      f.write('vcl%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Leaf']))
      f.write('vcs%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Stem']))
      f.write('vcr%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Root']))
      f.write('vsnl%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Leaf']))
      f.write('vsns%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Stem']))
      f.write('vsnr%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Root']))


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

