#!/usr/bin/env python

import json
import glob
import textwrap
import argparse
import os        # for removing temporarty file
import shutil    # for making temp copy of calibration targets to be imported


def main(args):

  files = sorted( glob.glob('%s/*.json' % '/tmp/dvmdostem/calibration/yearly/') )
  print "Found %s files." % (len(files)) 

  # Open the last file.
  # NOTE: May want to take average of last X files (years)??
  with open(files[-1]) as f:
    fdata = json.load(f)
  print "Writing simplified outputs to: %s" % (args.file) 
  with open(args.file, 'w') as f:
    f.write("Variable,Value\n")
    for i in range(0, 9):
      pftkey = 'PFT%i' % (i)
      f.write('GPPAll%s,%s\n' % (i, fdata[pftkey]['GPPAll']))
      f.write('NPPAll%s,%s\n' % (i, fdata[pftkey]['NPPAll']))
      f.write('VEGCL%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Leaf']))
      f.write('VEGCW%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Stem']))
      f.write('VEGCR%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Root']))
      f.write('VEGCSUM%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Leaf'] + fdata[pftkey]['VegCarbon']['Stem'] + fdata[pftkey]['VegCarbon']['Root']))
      f.write('VEGNL%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Leaf']))
      f.write('VEGNW%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Stem']))
      f.write('VEGNR%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Root']))
      f.write('VEGNSUM%s,%s\n' % (i, fdata[pftkey]['VegStructuralNitrogen']['Leaf'] + fdata[pftkey]['VegStructuralNitrogen']['Stem'] + fdata[pftkey]['VegStructuralNitrogen']['Root']))
      f.write('VEGLBLN%s,%s\n' % (i, fdata[pftkey]['VegLabileNitrogen']))

  if (args.instructionfile is not None):
    print "Writing instruction file to: %s" % (args.instructionfile)
    print "DOUBLE CHECK! --> instruction file must match simplified outputs!"
    with open(args.instructionfile, 'w') as f:
      f.write("pif @\n")
      for i in range(0,9):
        f.write("l1 @,@ !GPPALL%s!\n" % (i))
        f.write("l1 @,@ !NPPALL%s!\n" % (i))
        f.write("l1 @,@ !VEGCL%s!\n" % (i))
        f.write("l1 @,@ !VEGCW%s!\n" % (i))
        f.write("l1 @,@ !VEGCR%s!\n" % (i))
        f.write("l1 @,@ !VEGCSUM%s!\n" % (i))
        f.write("l1 @,@ !VEGNL%s!\n" % (i))
        f.write("l1 @,@ !VEGNW%s!\n" % (i))
        f.write("l1 @,@ !VEGNR%s!\n" % (i))
        f.write("l1 @,@ !VEGNSUM%s!\n" % (i))
        f.write("l1 @,@ !VEGLBLN%s!\n" % (i))

    # This seems a bit of a hack, but we need to 
    # replace the seconds line of the file with a l2 instead of l1
    # for the pest "line advance" function.
    # So we open the file, read it, modify the data, and write it back
    with open(args.instructionfile, 'r') as f:
      data = f.readlines()

    data[1] = "l2 @,@ !GPPALL0!\n"

    with open(args.instructionfile, 'w') as f:
      f.writelines(data)

    # Example:
    '''
    pif @
    l2 @,@ !GPPALL0!
    l1 @,@ !NPPALL0!
    ....
    '''


def targets_to_obs(targetsfile, obsfile, cmtnum):
  '''Total hack function to place target values in an .obf file from the calibration_targets.py file'''

  print textwrap.dedent('''\

    ### WARNING! ###
    --> Not sure if the variable/name mappings are correct between the 
        calibration targets file, the .json files, and the .obf file!!!

    ''')

  # bit of a hack, but allows importing calibration_targets.py as a module
  shutil.copy(targetsfile, "calibration_targets.py")
  import calibration_targets

  # find the right cmt data section, based on number
  for cmtname, data in calibration_targets.calibration_targets.iteritems():
    if data['cmtnumber'] == int(cmtnum):

      # read the obf file
      with open(obsfile, 'r') as ofile:
        obsdata = ofile.readlines()

      # assemble calibraiton targets data
      new_data = ""
      for line in obsdata:

        # Note this will have to be made smarter if/when we add non-pft
        # variables...such as the soil stuff...'cause there won't be a number at the end
        namepftnum, val = line.split()
        name = namepftnum[0:-1]
        pftnum = int(namepftnum[-1:])

        if name == 'gppall':
          new_tar_val = data['GPPAllIgnoringNitrogen'][pftnum]
        if name == 'nppall':
          new_tar_val = data['NPPAll'][pftnum]
        if name == 'vegcl':
          new_tar_val = data['VegCarbon']['Leaf'][pftnum]
        if name == 'vegcw':
          new_tar_val = data['VegCarbon']['Stem'][pftnum]
        if name == 'vegcr':
          new_tar_val = data['VegCarbon']['Root'][pftnum]
        if name == 'vegcsum':
          new_tar_val = data['VegCarbon']['Leaf'][pftnum] + data['VegCarbon']['Stem'][pftnum] + data['VegCarbon']['Root'][pftnum]
        if name == 'vegnl':
          new_tar_val = data['VegStructuralNitrogen']['Leaf'][pftnum]
        if name == 'vegnw':
          new_tar_val = data['VegStructuralNitrogen']['Stem'][pftnum]
        if name == 'vegnr':
          new_tar_val = data['VegStructuralNitrogen']['Root'][pftnum]
        if name == 'vegnsum':
          new_tar_val = data['VegStructuralNitrogen']['Leaf'][pftnum] + data['VegStructuralNitrogen']['Stem'][pftnum] + data['VegStructuralNitrogen']['Root'][pftnum]
        if name == 'veglbln':
          new_tar_val = data['Nuptake'][pftnum]

        newline = "{0}{1} {2:>25}\n".format(name, pftnum, new_tar_val)
        new_data += newline

      # Write it back out to the .obf file...
      with open("%s" % obsfile, 'w') as newfile:
        newfile.write(new_data)

    else:
      pass

  os.remove("calibration_targets.py")


if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
      Generates a simplified version of the model's json files. This
      is helpful for parsing with the PEST instruction files, as the
      PEST instruction files basically involve navigating by line and 
      charachter position.
    ''')
  )

  parser.add_argument('file', 
      help=textwrap.dedent('''The path/name of a simpliflied output file to generate.'''))

  parser.add_argument('instructionfile', nargs="?",
      help=textwrap.dedent("The path/name of a corresponding instruction file."))
 
  parser.add_argument('--targets-to-obs', nargs=3, metavar=('targetfile', 'obffile', 'cmtnumber'), 
      help=textwrap.dedent('''Update a .obf file with values from a calibration_targets file for a given CMT number.'''))

  args = parser.parse_args()
  #print args

  if (args.targets_to_obs):
    #if len(args.targets_to_obs) == 3:
    targets_to_obs(args.targets_to_obs[0], args.targets_to_obs[1], args.targets_to_obs[2])

  else:
    main(args)


# resulting simplified outputs for reference 
'''
GPPAll0,110.7451347285
NPPAll0,55.3725673643
VEGCL0,50.90577375
VEGCW0,87.334353575
VEGCR0,40.0896369243
VEGCSUM0,178.3297642493
VEGNL0,2.1151769691
VEGNW0,1.3782680325
VEGNR0,0.8439923563
VEGNSUM0,4.3374373579
VEGLBLN0,0.9190853995
'''


# Json snippet for reference
'''
{u'GPPAll': 28.1762950271368,
 u'GPPAllIgnoringNitrogen': 28.1762950271368,
 u'InNitrogenUptake': -933324.09375,
 u'LitterfallCarbonAll': 16.7496477663517,
 u'LitterfallNitrogen': {u'Leaf': -933324.09375,
  u'Root': -933324.09375,
  u'Stem': -933324.09375},
 u'LitterfallNitrogenPFT': 0.0,
 u'LuxNitrogenUptake': -933324.09375,
 u'NPPAll': 16.76845213770866,
 u'NPPAllIgnoringNitrogen': 16.76845213770866,
 u'PARAbsorb': 2.737188942392885,
 u'PARDown': 4.587406726596138,
 u'StNitrogenUptake': 0.0,
 u'TotNitrogenUptake': -933324.09375,
 u'VegCarbon': {u'Leaf': 8.41254997253418,
  u'Root': 2.343128681182861,
  u'Stem': 37.53537750244141},
 u'VegLabileNitrogen': 0.001000000047497451,
 u'VegStructuralNitrogen': {u'Leaf': -22399848.0,
  u'Root': -22399848.0,
  u'Stem': -22399848.0}
  }
'''
