#!/bin/bash


cd ~/s2 && pestpp tussock_full.pst /H localhost:5050 > ~/s2.log 2>&1 &
cd ~/s3 && pestpp tussock_full.pst /H localhost:5050 > ~/s3.log 2>&1 & 
cd ~/s4 && pestpp tussock_full.pst /H localhost:5050 > ~/s4.log 2>&1 &
cd ~/s5 && pestpp tussock_full.pst /H localhost:5050 > ~/s5.log 2>&1 &
cd ~/s6 && pestpp tussock_full.pst /H localhost:5050 > ~/s6.log 2>&1 &





