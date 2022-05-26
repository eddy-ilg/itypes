#!/bin/bash 

rm out_* -rf 

for file in *.py; do 
	echo Running $1$file; 
	./$file > /dev/null; 
done
