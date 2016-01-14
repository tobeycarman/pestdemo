# Basic tutorial for putting together a dvmdostem pest run

* Original Author: Vijay Patil, Oct 11 2015
* Modified/Expanded: Tobey Carman, Dec 10 2015

## General Idea

<img src="https://docs.google.com/drawings/d/1LM48CXqLutErYPl2DqqH-e82QBFT0R6leX6oLdmGYOM/pub?w=770&amp;h=851">

## Background

This presumes that you have downloaded PEST from www.pesthomepage.org, installed and compiled the program, and worked through some of the documents in the `pestdocs/` folder:

1. `unixpest.pdf` - instructions for compiling under linux.
2. `pestman` - comprehensive manual by the creators of the software.
3. `starting_pest.pdf` and `pest_settings.pdf` - good overviews, with some 'recipes' for setting up a set of pest files that will perform well. Both contain detail on the underlying algorithims that pest uses.
4. `TM-7-C5.pdf` - A USGS report with some additional suggestions for pest optimization and background on pest algorithim.

Included are several sets of files for some example pest runs that are trying to calibrate various thing. The `shrub_vegonly` example is attempting to calibrate vegetation-specific parameters for 9 pfts in a boreal deciduous-shrub community. The `basic-pest` example is a much simpler setup that simply tries to calibrate cmax for the PFTs in one of the communities. To createyour own calibration, you will need to carefully follow the pattern here, but creating your own template and instruction files for your specific use case.

> Note: In the `dvmdostem` documentation, we distinguish between model input for driving data vs parameters: the driving data is generally held in the `dvm-dos-tem/DATA/` directory and the parameter inputs are held in the `dvm-dos-tem/parameters/` directory. The authors of the PEST documentation use "Model Input Files" to refer to both parameter and driving data (excitation) inputs. In this document, we tend to make the distinction between driving inputs and parameter inputs, and generally modifications to inputs for PEST will be to the parameter inputs instead of the driving inputs.

## Naming conventions

Each PEST run will have a `case-name`. Generally any generated files will have the `case-name-` as a pre-fix to the filename. This `case-name-` should also be used for the directory holding all the files related to a PEST run or use case.

This convention is partially enforced by PEST - the name of the PEST control file (with extension `.pst`) is used as the `case-name-` and all PEST-generated files are named using this `case-name-`. We have attemted to follow the convention for files that are generate by any of our helper scripts.

<hr>
<hr>

## Steps to creating a pest run (workflow)

These steps describe how to create a run from scratch. The examples provided with the repo (`basic-pest` and `shrub_vegonly`) already have the files created so you can use them for reference. After following the steps you should understand how the files in this repository work together.

For the examples below, it is assumed that you have cloned this `pestdemo` repository and that you have the `pestdemo` repository next to your `dvmdostem repo:

        ├── dvm-dos-tem
        │   ├── ...
        │   
        ├── pestdemo
            ├── basic-pest
            ├── json2simpletxt.py
            ├── json2simpletxt.r
            ├── pestdocs
            ├── README.md
            └── shrub_vegonly

#### WARNING: PEST itself (and possibly the helper scripts) will overwrite some of the parameter files in the dvm-dos-tem! You should make sure that you have stashed or committed your changes before playing around with PEST so that you don't lose any modifications!

1. Choose a 'case-name', such as "shrub_vegonly" and make a folder to hold the PEST files for this PEST run case.

2. Decide which values/parameters you'd like to calibrate. In general, these will be select values for a single community type (number) that you find in the `dvm-dos-tem/parameters/cmt_calparbgc.txt` file. 
  
  > Note that due to the architecture of PEST and `dvm-dos-tem`, there are actually many other things that can be treated as parameters, such as the calibration directives, and any of the other values found in any of the files in the `dvm-dos-tem/parameters/` directory.

3. Write the template file(s) (`.tpl`). The template files are used by PEST as it is running to try out different parameter values. A template file has `ptf %` on the first line. `ptf` stands for "pest template file" and the `%` sign is a delimiter used to denote fields that PEST will treat as parameters. You can use other charachters for a delimiter; see the `pestman.pdf` for more info.

4. Check the template file(s) using `TEMPCHEK`.

        $ tempchek basic-pest/cmt_calparbgc.tpl 
         TEMPCHEK Version 13.4. Watermark Numerical Computing.

         Errors in file basic-pest/cmt_calparbgc.tpl ----->
         No errors encountered.

         9 parameters identified in file basic-pest/cmt_calparbgc.tpl: these are 
           listed in file basic-pest/cmt_calparbgc.pmt.


5. (Optional) Further check your template file by letting `TEMPCHEK` write a "model input" file (parameter file), and then running the model with the generated file to make sure that values are being substitued into the template correctly. To do this, you must also supply some initial parameter values that should be substituted into the template. The easiest way to do this is to copy the `.pmt` file generated by the first run of `TEMPCHEK` to a `.par` file and add the parameter values, scales and offsets to the `.par` file. You also must add the variables for DPOINT and PRECS at the top. So you should end up with a file something like this:

        $ head basic-pest/cmt_calparbgc.par
        double point
         cmax0   255.0    1.0  0.0
         cmax1   625.0    1.0  0.0 
         cmax2   83.0     1.0  0.0 
         cmax3   23.9     1.0  0.0 
         cmax4   45.0     1.0  0.0 
         cmax5   66.8     1.0  0.0 
         cmax6   27.8     1.0  0.0 
         cmax7   38.8     1.0  0.0 
         cmax8   86.1     1.0  0.0

 To run `TEMPCHEK` in this mode, provide a path to the template file and a path to the model input (parameter) file that should be written by `TEMPCHEK`. `TEMPCHEK` will look for a `.par` file in the same location as the template file, and using the same name as the template file. (You may also specify the `.par` file as the third argument to `TEMPCHEK`).

        $ tempchek basic-pest/cmt_calparbgc.tpl ../dvm-dos-tem/parameters/cmt_calparbgc.txt 
         TEMPCHEK Version 13.4. Watermark Numerical Computing.

         Errors in file basic-pest/cmt_calparbgc.tpl ----->
         No errors encountered.

         Errors in parameter value file basic-pest/cmt_calparbgc.par ----->
         No errors encountered.

         Writing model input file ../dvm-dos-tem/parameters/cmt_calparbgc.txt ----->
         File ../dvm-dos-tem/parameters/cmt_calparbgc.txt written ok.

 Then check that the ../dvm-dos-tem/parameters/cmt_calparbgc.txt file looks ok, and rum the model to make sure it can read the file alright.

6. Figure out which "model outputs" you are interested in calibrating to. In the PEST manual, these outputs are called "observations". In the terminolgy we use with `dvm-dos-tem` we call these "target values". So the model outputs you are interested in are most likely going to come from the calibration `.json` files and will also most likely be values found in the `calibration_targets.py` file.

 > Note: It might be the case that we use the same calibration targets for all PEST runs, in which the `json2simpletxt.py` file described in the next steps is already written for you.

7. (Technically optional, but highly reccommended) Write a script that can parse a `.json` file and create a simpler output file that will be easier to parse with the PEST instruction file. There is a provided helper script named `json2simpletxt.py` that should work for most cases.

 > This step is not strictly necessary, but because of the tedious methods available in the PEST instruction file (navigating by line and charachter position), it will probbaly be easier and more reliable to parse a simplifed text file rather than the `.json` files.

8. Test run the `json2simpletxt.py` script to read the model outputs, (`.json` files generated when running `dvmdostem` in calibration mode), and create a simplified version of the outputs. Note that you must have run the model recently and there must be `.json` files in the `/tmp` directory.

        $ ./json2simpletxt.py basic-pest/simplified-outputs.txt
        Namespace(file='basic-pest/simplified-outputs.txt', instructionfile=None)
        Found 20 files.
        Writing simplified outputs to: basic-pest/simplified-outputs.txt

  Variable names should include pft numbers if the variable is pft-specific. One possibility for the simplified output format is like this (as generated by the `json2simpletxt.py` script):

        $ head basic-pest/simplified-outputs.txt 
        Variable,Value
        GPPAll0,31.7222430706
        NPPAll0,21.517536521
        VEGCL0,11.0686264038
        VEGCW0,7.01341104507
        VEGCR0,5.2543387413
        VEGCSUM0,23.3363761902
        VEGNL0,-18666504.0
        VEGNW0,-18666504.0
        VEGNR0,-18666504.0

 > ###### Please note: the `json2simpletxt.py` script is fairly crude! Depending on which CMT you are working with, you will need to adjust the indexing in the script so that it only operates over the PFTs that are defined in the community type you are working with!

9. Write the instruction (`.ins`) file(s). The instruction file(s) could be written by hand, but it is probably easier to using the `json2simpletxt.py` helper script (this will re-run the output to simple-output conversion; this is not a problem):

        $ ./json2simpletxt.py basic-pest/simplified-outputs.txt basic-pest/read-simple-outputs.ins
        Namespace(file='basic-pest/simplified-outputs.txt', instructionfile='basic-pest/read-simple-outputs.ins')
        Found 20 files.
        Writing simplified outputs to: basic-pest/simplified-outputs.txt
        Writing instruction file to: basic-pest/read-simple-outputs.ins
        DOUBLE CHECK! --> instruction file must match simplified outputs!

8. Check the instruction file with `INSCHEK`:

        $ inschek basic-pest/read-simple-outputs.ins 
         INSCHEK Version 13.4. Watermark Numerical Computing.

         Errors in file basic-pest/read-simple-outputs.ins ----->
         No errors encountered.

         99 observations identified in file basic-pest/read-simple-outputs.ins: these 
           are listed in file basic-pest/read-simple-outputs.obf.

9. Check the instruction file again with `INSCHECK`, but this time providing a model output file to be parsed by the instruction file:

        $ inschek basic-pest/read-simple-outputs.ins basic-pest/simplified-outputs.txt 
         INSCHEK Version 13.4. Watermark Numerical Computing.

         Errors in file basic-pest/read-simple-outputs.ins ----->
         No errors encountered.

         Reading model output file basic-pest/simplified-outputs.txt ----->
         No errors encountered.

         99 observations identified in file basic-pest/read-simple-outputs.ins: these 
           are listed in file basic-pest/read-simple-outputs.obf together with their 
           values as read from file basic-pest/simplified-outputs.txt.

10. Write a wrapper script, `dvmdostem-pest-wrapper.sh`. This script wraps `dvmdostem` and the `json2simpletxt.py` helper script so that PEST can make one call to the wrapper script instead of having to invoke the model *and* the post-processing output-simplifying step. Here is an example wrapper script; you will likely need to change the paths:

        $ cat basic-pest/dvmdostem-pest-wrapper.sh 
        #!/bin/bash

        # Could look this up based on directory name? or pass in an argument?
        CASE_NAME="basic-pest"

        # Run the model
        cd ~/dvm-dos-tem/
        ./dvmdostem --cal-mode -log-level note -p 10 -m 100

        # Create the simplified output 
        cd "~/pestdemo/$CASE_NAME"
        rm -f simplified-outputs.txt
        ./json2simpletxt.py simplified-outputs.txt

9. Use `PESTGEN` to create a start at a control file (`.pst`). `PESTGEN` will fill out the control file with initial parameter values and observations that it finds in the `.par` and `.obf` files respectively.

        $ pestgen basic-pest basic-pest/cmt_calparbgc.par basic-pest/read-simple-outputs.obf 
         PESTGEN Version 13.4. Watermark Numerical Computing.

         Checking parameter value file basic-pest/cmt_calparbgc.par ----->
         No errors encountered.

         Checking observation value file basic-pest/read-simple-outputs.obf ----->
         No errors encountered.

         Writing PEST control file basic-pest.pst ----->
         File written ok.

 You may have to move the `.pst` file into the case directory:

        $ mv basic-pest.pst basic-pest/

10. Modify the `.pst` control file so that it has the correct paths for running the wrapper script and finding the template, parameter, instruction, and observations files. The lines you will need to modify are toward the end of the file in the "`* model command line`" and "`* mode input/output`" sections.

11. Make sure that the "post warm up pause" is disabled in the `dvm-dos-tem`. This is required for PEST to be able to automatically start consecutive model runs without user intervention. To do this, set the "pwup" variable to "false" in the `dvm-dos-tem/config/calibration-directives.txt` file.

11. Finally, run PEST!

        $ cd basic-pest
        $ pest basic-pest.pst

 You should see the model begin to run:


        $ pest basic-pest.pst
         PEST Version 13.4. Watermark Numerical Computing.

         PEST is running in parameter estimation mode.

         PEST run record: case basic-pest
         (See file basic-pest.rec for full details.)

         Model command line: 
         ./dvmdostem-pest-wrapper.sh

         Running model .....

            Running model 1 time....
        Setting up logging...
        (000000xc76) [note] [] Checking command line arguments...
        (000000xc76) [warn] [] Argument validation/verification NOT IMPLEMENTED YET!
        (000000xc76) [note] [] Turn floating point exceptions on?: false
        (000000xc76) [note] [] Reading controlfile into main(..) scope...
        (000000xc76) [note] [] Creating a ModelData object based on settings in the control file
        (000000xc76) [note] [] Creating a fresh 'n clean NEW output file...
        (000000xc76) [note] [] Start dvmdostem @ Fri Jan  8 16:47:56 2016

        (000000xc76) [note] [] --> CLIMATE --> empty ctor
        ...

 To stop or pause the model, you will have to open a separate terminal window, change into the `pestdemo/basic-pest` directory and use the various PEST commands: PPAUSE, PUNPAUSE, PSTOP or PSTOPST.

When the PEST run completes, there will be a bunch of files with various info that will help to interpert and 

That is all for now! The shrub_vegonly example is similar to the basic-pest example, but has siginificantly more parameters and may be a bit trickier to get running.

## Ideas for Expansion / To-Do lists

* expand the json2simpletxt.py file so that is can handle soil variables
* generalize the wrapper script?
* Work on optimization notes from Vijay (below)
* finish up the table of files



<hr>
<hr>
<hr>
<hr>
### OLD STUFF; will clean up

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


</hr>
</hr>


## Table of files

File                           | Input Files      | Generated | Helper Scripts|
-------------------------------|------------------|-----------|---------------|
`parameters/cmt_calparbgc.txt` |   required       |           |               |
`cmt_calparbgc.tpl`            |   required       |           |               |
`cmt_calparbgc.pmt`            |                  |     X     |               |
`<case-name>.par`              |                  |     X     |               |
`json2simpletxt.r`             |                  |           |       X       |
`<case-name>-simpletxt.csv`    |                  |     X     |               |
`create_instruction-file.r`    |                  |           |       X       |
`read-simpletxt.ins`           |   required       |     X     |               |
`<case-name>.pst`              |   required       |     X*    |               |
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
`<case-name>.rst`              |                  |     X     |               |
`<case-name>.rmf`              |     optional     |     X     |               |
`<case-name>.hld`              |     optional     |     X     |               |
`generate-pest-case.py`        |                  |           |        X      |


> *The pest control file can be generated using the `PESTGEN` utility program or written by hand.

### Required Input Files
1. `cmt_calparbgc.tpl` - The pest "template file(s)"; tells pest how to read the parameters from the model's parameter-input files and which values to replace (parameterize). There could be more than one template file, if for example you decided to calibrate a value in one of the other `parameters/cmt_xxxx.txt` files.
2. `read-simpletxt.ins` - The pest "instruction file(s?)"; tells pest how to read the model's output files and find values that it will check against observations or desired values.
3. `<case-name>.pst` - The pest control file; tells pest how to run the model and contains much information for "tuning" pest's operation.
4. `parameters/cmt_calparbgc.txt` - The dvmdostem parameter file holding values that should be calibrated. You shouldn't need a duplicate of this file - you will tell pest where to look for the parameter file (which is typically in `dvmdostem`'s `parameters/` directory).

### Optional Input Files
1. `<case-name>.rmf` - Parallel PEST run management file; user supplied input file.
2. `<case-name>.hld` - The “parameter hold file”; user supplied input file.


### Helper Scripts
1. `json2simpletxt.r` - an R script (that we wrote) that helps translate our model outputs (the `.json` files generated when the model is run in calibration mode) into an easier format for creating the pest template file. This script could be written in with Python or bash, or any number of other languages. 
2. `create-instruction-file.r` - Tells pest how to interpret an output file and how to extract values associated with output variables.
3. `generate-pest-case.py` (NOT IMPLEMENTED YET) - This utility could generate a folder with a bunch of appropriately named files for a particular pest case.

### Generated files
1. `<case-name>-simpletxt.csv` - The simplified model outputs containing just the values to be compared against observed values; this file is generated by the `json2simpletxt.r` script after the model runs. 
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
13. `<case-name>.par` - The best parameter values achieved. ?? Or are these input/initial values???
14. `cmt_calparbgc.pmt` - Contains the variable/substitution names from the template file(s). Generated by `TEMPCHEK`.

</hr>
</hr>




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
