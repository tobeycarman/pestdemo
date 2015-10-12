#this creates a pest instruction file- this tells pest how to interpret an output file and how to extract values associated with 
#output variables.

#make vars vector reflect variables in output file created by pest_processing_xx.r
vars<-c('GPPALL','NPPALL','VEGCL','VEGCW','VEGCR','VEGCSUM',
'VEGNL','VEGNW','VEGNR','VEGNSUM','VEGLBLN')
pft.nums<-0:8

#instruction file lines tell pest
#1) how to move through the file (l1 means move 1 line)
#2) what to look for based on delimiters (@ in this case)
#3) so here pest is looking for values after a comma (@,@)
#4) first line contains a header that identifies as a pest instruction file (pif) then lists the delimiter character (@ in this case)
firstline="pif @"

#this code simplifies the creation of an input file based on the number of pfts and the variable names above.
pft.ids=paste('l1 @,@ !',sep='')

p.num.rep=rep(pft.nums,each=length(vars))
vars.rep=rep(vars,length(pft.ids))
vars.rep=paste(vars.rep,p.num.rep,"!",sep='')

lines<-paste("l2 @,@ !",vars.rep[1],sep="") #first line starts with l2 because
#the first line of the output file TEM_Pest_Output_xx.txt is a header. So you move two lines to get to the first variable value.
lines<-c(lines,paste("l1 @,@ !",vars.rep[2:length(vars.rep)],sep="")) #all other lines start with l1 because the variables
# in the output file are given one per line.

#this needs to be modified with soil variables (which don't need pft-specific names) if appropriate

file=cbind(c(firstline,lines))
print(file) #check to make sure it looks right.
write.table(file,"tem_shrub_vegonly.ins",row.names=FALSE,col.names=FALSE,quote=FALSE) #write out tem_xx.ins (instruction file)

