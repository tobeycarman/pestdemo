# Basic tutorial for putting together a pest run

* Original Author: Vijay Patil, Oct 11 2015
* Modified/Expanded: Tobey Carman, Dec 10 2015

## Background

This presumes that you have downloaded pest from www.pesthomepage.org, installed and compiled the program, and worked through some of the documents in the pestdocs folder that I distributed:

1. `unixpest.pdf` - instructions for compiling under linux.
2. `pestman` - comprehensive manual by the creators of the software.
3. `starting_pest.pdf` and `pest_settings.pdf` - good overviews, with some 'recipes' for setting up a set of pest files that will perform well. Both contain detail on the underlying algorithims that pest uses.
4. `TM-7-C5.pdf` - A USGS report with some additional suggestions for pest optimization and background on pest algorithim.

Included are a set of files for an example pest run that is trying to calibrate vegetation-specific parameters for 9 pfts in a boreal deciduous-shrub community. These files will need to be modified carefully to fit your needs.

> Note: It seems like file locations have to be specified with absolute, non-symbolic paths to work. 
This was the case for me. so: `/home/vijay/Desktop/pest/shrub_veg/shrub_veg.pst` for the relevant pest control file.
> Note: If path + filename is too long, pest may throw an error. Try shortening file names.

> Update - oct 11 2015. now pest commands are running from every directory. Don't know what happened differently. If this is the case for everyone, then we can do away with the obnoxious long path names.

## Steps to creating a pest run

### Naming conventions
Pest requires a number of special files, and we have found it helpful to group the files for a certain calibration run by using a naming convention. So for example pre-fixing each file with something like `shrub_vegonly_`. Then all files for a certain run will also go into a named sub-folder within your working directory (pest folder).

### Files

File | Required | Generated | Helper Scripts
-----|----------|-----------|---------------
runname-prefix.ins | X  | |
runname-prefix_<cmt_bgcvegetation>.tpl | X  | |
runname-prefix_create_ins.r | | X |
.??? | X  | |
.??? | X  | |
.??? | X  | |
.??? | X  | |



### Required Files
1. `.tpl` - the pest "template file(s)"; tells pest how to read the parameters from the models parameter input files and which values to replace (parameterize)
2. `.ins` - the pest "instruction file(s?)"; tells pest how to read the model's output files and find values that it will check against observations or desired values.
3. `??` - ??

### Helper Scripts
1. `.R` - an R script (that we wrote) that helps translate our outputs into an easier format for creating the pest template file.
2.
3.

### Generated files

-----------------------

### Workflow

1. Decide which value / parameters you'd like to calibrate. In general, these will be select values that you find in the `dvmdostem/parameters/cmt_calparbgc.txt` file, although due to the architecture of PEST and `dvmdostem`, there are actually many other things that can be treated as parameters, such as the calibration directives.

2. Write the template file(s) (`.tpl`). 
3. Check the template file(s) using 


1. make sure that pest_processing_xx.r creates desired summary of output vals from data
this file should have two columns- Variable, and Value (comma delimmited). 
Variable names should include pft numbers if pft-specific.

2. make sure that pest_ins_create_xx.r creates instruction file that matches output variable names as shown in the output.txt file

3. run inschek /home/vijay/Desktop/pest/xx/tem_xx.ins to make sure instructions are well formed.
4. make observations file by copying output.txt but replacing model values with observed (target) values
	This will have same name but saved as csv (TEM_Pest_Output_xx.csv).

5. make output file from .ins and observations file in output.csv > .obf
	inschek /home/vijay/Desktop/pest/xx/tem_xx.ins /home/vijay/Desktop/pest/xx/TEM_Pest_Output_xx.csv
	
	will create tem_xx.obf file
  
6. make .tpl (template files) 
	first line is ptf % (pest template file , delimiter character)-can use any charcter, but it shouldn't be a comment character in the corresponding TEM config file.
	the .tpl file will mirror a model config file (like calparbgc.txt)
	but the parameters to modify will be replaced with paramater names surrounded by delimiters
	parameter names should be pft-specifc.

7. create executable batch file for model runs. 
My batch file does two things- runs the model and invokes the post-processing script to create model text output file.
Note that to run the model in batch mode you have to turn off the automatic pause at 100 years in cal-mode.

Currently, this can be done by commenting out ~line 334 RunCohort.cpp and re-compiling.
may be possible in calibration directives eventually. 

the calibration directives file is used to specify when modules turn on and off. This behavior can be modified by pest if you wish- you just need to create a corresponding template file, with time on as a parameter.

8. create .par file with precision, decimal point on top line (double point). then par names (from .tpl files), starting value, scale (1) and offset (0)

9. make basic control file > pestgen tem_xx tem_xx.par tem_xx.obf . specify absolute paths to files. will create tem_xx.pst

10. edit control file .pst - set number of template files - 2nd row of #, first column in control data section. Also change scale adjustment first number in parameter groups. 

- Two important adjustments- specify the possible range of parameter values and specify any transformations/weights for the target variables- weighting is probably the way to simultaneously calibrate pools differing by several orders of magnitude (soil and veg pools) but I haven't gotten it figured out yet. 
- check pest settings doc for suggestions. this still requires a bunch of cut and paste. 

-the bottom section is where you specify the names and paths of all other relevant files.
   -specify batch file in model command line
   -specify tpl files and corresponding config files, separated by a space.
   next line is path to .ins - space- modeloutput.txt

see example files.

11. check pst file with pstchek path/tem_xx.pst
12. run pest with pest path/tem_xx.pst

model will produce a lot of files including results .res, sensitivity .sens, record of parameter combinations .rec.

Take some time to go through the output files and see what kind of data they contain.
###########################################################
###########################################################
#optimization notes from pest settings:
weight observations appropriately- weight smaller observations higher so they are visible
log-transform all parameters whose lower bound is greater than 0

set RLAMDA1 = 10.0
set RLAMFAC = -3

make SVD section- makes sure it maintains numerical stability.
SVDMODE = 1;
MAXSING = # of adjustable parameters;
EIGTHRESH = 5x10-7;
EIGWRITE = 0;

in control data section:
NOPTMAX = zero

- then run model once.
- then run PWTADJI - creates new pest control file.

add Tikhonov regularization to pest control file by running addreg1 utility

then later you can set PHIMLIM to value slightly higher than lowest achievable objective function

- so either the weighting will balance out the size of observations, or the log-transformation will. I am inclined to try the log-transformation first.
