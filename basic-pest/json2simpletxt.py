#!/usr/bin/env python

import json
import glob

files = sorted( glob.glob('%s/*.json' % "/tmp/dvmdostem/calibration/yearly/") )

with open(files[-1]) as f:
  fdata = json.load(f)

# PFT variables
pftvars = ['GPPAll','NPPAll','VEGCL','VEGCW','VEGCR','VEGCSUM','VEGNL','VEGNW','VEGNR','VEGNSUM','VEGLBLN']
pftvarskeys = ['GPPAll', 'NPPAll', 'VEGCarbon']

with open('basicpestsimpleoutput.csv', 'w') as f:
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
    f.write('VEGNSUM%s,%s\n' % (i, fdata[pftkey]['VegCarbon']['Leaf'] + fdata[pftkey]['VegCarbon']['Stem'] + fdata[pftkey]['VegCarbon']['Root']))
    f.write('VEGLBLN%s,%s\n' % (i, fdata[pftkey]['VegLabileNitrogen']))
    

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
# for i in range(0,9):
#   pftkey = 'PFT%s' % (i)
#   for var in pftvars:
#     print fdata[pftkey][var]

from IPython import embed; embed()