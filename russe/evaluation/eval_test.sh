#!/bin/bash

for submission in `find $1 -type d | sort` ; do
	testcsv="$submission/test.csv"
	if [ -a $testcsv ] ; then
		echo $testcsv
		./eval_test.py $testcsv > $submission/report.txt 2> $submission/results.txt
	fi    
done

echo "===================================================="
find $1 -iname "results.txt" -exec ls '{}' \; -exec echo "" \; -exec cat '{}' \;



