#!/bin/bash

for submission in `find $1 -maxdepth 1 -type d | sort` ; do
	testcsv="$submission/test.csv"
	if [ -a $testcsv ] ; then
		echo $testcsv
		./evaluate_test.py $testcsv > $submission/report.txt 2> $submission/results.txt
	fi    
done

echo "===================================================="
find $1 -maxdepth 2 -iname "results.txt" -exec echo "" \; -exec ls '{}' \; -exec cat '{}' \;



