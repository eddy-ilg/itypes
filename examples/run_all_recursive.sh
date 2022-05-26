#!/bin/bash 

rm out_* -rf 

for file in *.py; do 
	echo Running $file; 
	./$file > /dev/null; 
done

cd filesystem 
./run_all.sh filesystem/
cd .. 

cd struct 
./run_all.sh struct/ 
cd .. 

cd sequence
./run_all.sh sequence/ 
cd .. 
