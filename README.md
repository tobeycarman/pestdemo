# Basic tutorial for putting together a pest run

* Original Author: Vijay Patil, Oct 11 2015
* Modified/Expanded: Tobey Carman, Dec 10 2015

## Background

This presumes that you have downloaded pest from www.pesthomepage.org, installed and compiled the program, and worked through some of the documents in the `pestdocs/` folder:

1. `unixpest.pdf` - instructions for compiling under linux.
2. `pestman` - comprehensive manual by the creators of the software.
3. `starting_pest.pdf` and `pest_settings.pdf` - good overviews, with some 'recipes' for setting up a set of pest files that will perform well. Both contain detail on the underlying algorithims that pest uses.
4. `TM-7-C5.pdf` - A USGS report with some additional suggestions for pest optimization and background on pest algorithim.

Included are a set of files for an example pest run that is trying to calibrate vegetation-specific parameters for 9 pfts in a boreal deciduous-shrub community. These files will need to be modified carefully to fit your needs.

> Note: It seems like file locations have to be specified with absolute, non-symbolic paths to work. So: `/home/vijay/Desktop/pest/shrub_veg/shrub_veg.pst` for the relevant pest control file.
> Note: If path + filename is too long, pest may throw an error. Try shortening file names.

> Update - Oct 11 2015. Now pest commands are running from every directory. Don't know what happened differently. If this is the case for everyone, then we can do away with the obnoxious long path names.

> Note: The convention we use for `dvmdostem` is that "input files" are the NetCDF files while "parameter files" are the text files in the `parameters` directory. This can me confusing when reading the Pest documentation because they use "Model Input Files" to refer to what we call "parameter files".

## Naming conventions

Pest requires a number of special files, and we have found it helpful to group the files for a certain calibration run by using a naming convention. So for example pre-fixing each file used in a particular calibration run or suite of runs with some kind of `case-name`. In fact, this convention is partially enforced by PEST - the name of the "control file" (with extension `.pst`) is used as the "case name" and all the output files are named using this "case name". We have extended the pattern to mark the input files and the helper script files that we created for running pest.

Additionally, all files for a certain run will go into a named folder within your working directory (pest folder?). 

## Table of files

File                           | Input Files      | Generated | Helper Scripts|
-------------------------------|------------------|-----------|---------------|
`<case-name>_create_ins.r`     |                  |           |       X       |
`<case-name>.ins`              |   required       |     X     |               |
`<case-name>_cmt_calparbgc.tpl`|   required       |           |               |
`parameters/cmt_calparbgc.txt` |   required       |           |               |
`<case-name>.pst`              |   required       |     X*    |               |
`<case-name>_pest_processing.r`|                  |           |       X       |
`<case-name>_output.csv`       |                  |     X     |               |
`<case-name>.rec`              |                  |     X     |               |
`<case-name>.jac`              |                  |     X     |               |
`<case-name>.jst`              |                  |     X     |               |
`<case-name>.sen`              |                  |     X     |               |
`<case-name>.jco`              |                  |     X     |               |
`<case-name>.prf`              |                  |     X     |               |
`<case-name>.rei`              |                  |     X     |               |
`<case-name>.res`              |                  |     X     |               |
`<case-name>.mtt`              |                  |     X     |               |
`<case-name>.obf`              |                  |     X     |               |
`<case-name>.par`              |                  |     X     |               |
`<case-name>.rst`              |                  |     X     |               |
`<case-name>.rmf`              |     optional     |     X     |               |
`<case-name>.hld`              |     optional     |     X     |               |
`generate-pest-case.py`        |                  |           |        X      |


> *The pest control file can be generated using the `PESTGEN` utility program or written by hand.

### Required Input Files
1. `<case-name>_cmt_calparbgc.tpl` - The pest "template file(s)"; tells pest how to read the parameters from the model's parameter input files and which values to replace (parameterize). There could be more than one template file, if for example you decided to calibrate a value in one of the other `parameters/cmt_xxxx.txt` files.
2. `<case-name>.ins` - The pest "instruction file(s?)"; tells pest how to read the model's output files and find values that it will check against observations or desired values.
3. `<case-name>.pst` - The pest control file; tells pest how to run the model and contains much information for "tuning" pest's operation.
4. `parameters/cmt_calparbgc.txt` - The dvmdostem parameter file holding values that should be calibrated. You shouldn't need a duplicate of this file - you will tell pest where to look for the parameter file (which is typically in `dvmdostem`'s `parameters/` directory).

### Optional Input Files
1. `<case-name>.rmf` - Parallel PEST run management file; user supplied input file.
2. `<case-name>.hld` - The “parameter hold file”; user supplied input file.


### Helper Scripts
1. `<case-name>_pest_processing.r` - an R script (that we wrote) that helps translate our model outputs (the `.json` files generated when the model is run in calibration mode) into an easier format for creating the pest template file. This script could be written in with Python or bash, or any number of other languages. 
2. `<case-name>_create_ins.r` - Tells pest how to interpret an output file and how to extract values associated with output variables.
3. `generate-pest-case.py` (NOT IMPLEMENTED YET) - This utility could generate a folder with a bunch of appropriately named files for a particular pest case.

### Generated files
1. `<case-name>_output.csv` - The simplified model outputs containing just the values to be compared against observed values; this file is generated by the `<case-name>_pest_processing.r` script after the model runs. 
2. `<case-name>.rec` - The "run record file".
3. `<case-name>.jac` - The Jacobian matrix for a possible restart.
4. `<case-name>.jst` - The same file from the previous optimisation iteration.
5. `<case-name>.sen` - The parameter sensitivities.
6. `<case-name>.jco` - The Jacobian matrix pertaining to the best parameters for access by the JACWRIT utility.
7. `<case-name>.prf` - A special Parallel PEST restart file.
8. `<case-name>.rei` - Interim observation residuals.
9. `<case-name>.res` - Tabulated observation residuals.
10. `<case-name>.mtt` - Interim covariance matrix and related matrices.
11. `<case-name>.obf` - The observation sensitivities.
12. `<case-name>.rst` - The restart information stored at the beginning of each optimisation iteration.
13. `<case-name>.par` - The best parameter values achieved.


<hr>
<hr>

## Steps to creating a pest run (workflow)

1. Decide which value / parameters you'd like to calibrate. In general, these will be select values that you find in the `dvmdostem/parameters/cmt_calparbgc.txt` file, although due to the architecture of PEST and `dvmdostem`, there are actually many other things that can be treated as parameters, such as the calibration directives, and any of the other values found in any of the files in the `dvmdostem/parameters/` directory.
1. Choose a 'case name'.
2. Make a folder to hold the pest files for this pest run, and generate the required input files.
2. Write the template file(s) (`.tpl`). 
3. Check the template file(s) using `TEMPCHEK`.
4. Further check your template file by supplying `TEMPCHEK` with a set of parameter values and letting `TEMPCHEK` write an 'model input' (parameter) file. Then you can run dvmdostem with this file to make sure that the values are being substituted into the template correctly.
5. Use the `<case-name>-pest-processing.r` script to read the model outputs, (`.json` files generated in when running in calibration mode), and create a simplified version of the outputs that will be easier to parse with in the pest instruction file. Variable names should include pft numbers if pft-specific. One possibility for the simplified output format is like this:
```
Variable,Value
GPPAll0,110.7451347285
NPPAll0,55.3725673643
...
```
> Note, this step is not strictly necessary, but because of the rather primitive and tedious methods available in the pest instruction file (navigating by line and characther position), it will probbaly be easier and more reliable to parse a simplifed text file rather than the `.json` files.
6. Write the instruction file(s) (`.ins`). This can be written by hand or generated using our helper script `<case-name>-create-pest-ins.r`, or another helper script that you may write. Make sure that the instruction file matches the output file
7. Check the instruction file with `PESTCHEK` and `INSCHEK`.

```bash
# generates a `.obf` file with just the observation names
$ inschek <case-name>.ins 

# generates an `.obf` file with obs names/values
$ inschek <case-name>.ins <model output csv>
```

8. Use `PESTGEN` to create a start at a control file (`.pst`).


<hr>



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
