#!/usr/bin/env Rscript

# Script to translate json dvmdostem output into a 
# csv (text) file that can be read by PEST.

# Currently set up for pft-specific pools only, for a boreal 
# shrub community with 9 pfts. To add soil pools, would need to 
# add code for extracting appropriate variables from the json 
# object then adding appropriate variable names 
# and values to the obs.vals data.frame produced at the end.

# Results are written out into a .txt file comma delimited.
# output can be found in the outdir

library(rjson)
#config <- fromJSON(file="../dvm-dos-tem/config/config.js")

#print(config)

# SET THE CASE NAME HERE:
casename<-"basicpest"

# store the current working directory so we can write the output file here
script_run_from_directory<-getwd()
ofname<-file.path(script_run_from_directory, paste(casename, "simpleoutput.csv", sep=""))

# do the parsing in the the /tmp directory...
setwd('/tmp/dvmdostem/calibration/yearly')

# haven't implemented this yet- want to take the averages of last 10 years model output for comparison.
avg.years=10
jsons=dir(pattern='json')
num.files=length(jsons)
print("Found this many json files:")
print(num.files)
last.jsons=jsons[(num.files-avg.years):num.files]
######################################################

cmtbgc<-fromJSON(file=jsons[num.files]) #extracting last year json file as object 'cmtbgc'

#pftspecific code- generating a matrix with parameters as rows and pfts as columns
# there is also code to label pft-specific target variables with the appropriate pft index
pft.nums<-0:8 #this can be changed to any vector of pft numbers depending on the community

pft.ids<-paste('PFT',pft.nums,sep='')
num.pfts=length(pft.ids)

#the following vector should be changed depending on which veg-specific target variables you are using.
pft.vars<-c('GPPAll','NPPAll','VEGCL','VEGCW','VEGCR','VEGCSUM','VEGNL','VEGNW','VEGNR','VEGNSUM','VEGLBLN')

#this loop extracts pft-specfic output variables from cmtbgc json object.
pft.vals.mat<-matrix(0,length(pft.vars),num.pfts) #values go into this matrix.
for(j in 1:num.pfts) 
{
  pft=pft.ids[j] #getting the pft index number
  pft.dat<-cmtbgc[[pft]] #each pft is a first-level list element.
  
  #currently, variable extraction is hard-coded. Have to specify different variables and create objects for them by hand.
  gppall<-pft.dat$GPPAll
  nppall<-pft.dat$NPPAll
  
  vegc.l<-pft.dat$VegCarbon$Leaf
  vegc.w<-pft.dat$VegCarbon$Stem
  vegc.r<-pft.dat$VegCarbon$Root
  vegc.sum<-vegc.l+vegc.w+vegc.r
  
  veg.strn.l<-pft.dat$VegStructuralNitrogen$Leaf
  veg.strn.w<-pft.dat$VegStructuralNitrogen$Stem
  veg.strn.r<-pft.dat$VegStructuralNitrogen$Root
  veg.strn.sum<-veg.strn.l+veg.strn.w+veg.strn.r
  
  veg.lbln<-pft.dat$VegLabileNitrogen
  
  #pft.vals vector should include all the target variables you care about (all objects in preceeding code block)
  pft.vals<-c(gppall,nppall,vegc.l,vegc.w,vegc.r,vegc.sum,veg.strn.l,veg.strn.w,veg.strn.r,veg.strn.sum,veg.lbln)
 
  #if there is only one pft, the output is a vector instead of a matrix.
  if(length(dim(pft.vals.mat))>1){ 
  pft.vals.mat[,j]=pft.vals} else {
  pft.vals.mat=pft.vals}
}

#creating a dataframe with pft-specfic variable names. will have a column for Variable (eg nppall0), and one for Value
pft.vars.rep<-rep(pft.vars,num.pfts)
vars<-c(pft.vars.rep)
pft.for.df<-c(rep(pft.nums,each=length(pft.vars)))
vars.numd=paste(vars,pft.for.df,sep='')

pft.vals.vec<-c(pft.vals.mat) #converting matrix to a single vector. 
vals<-c(pft.vals.vec)

obs.vals<-data.frame(Variable=vars.numd,Value=vals)

print("Writing file:")
print(ofname)
write.table(obs.vals,ofname,row.names=FALSE,quote=FALSE,sep=',')






