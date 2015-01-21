#!/bin/bash

for submission in `find $1 -maxdepth 1 -type d | sort` ; do
	testcsv="$submission/test.csv"
	if [ -a $testcsv ] ; then
		echo $testcsv
		./evaluate_test.py $testcsv > $submission/report.txt 2> $submission/results.txt
	fi    
done

i=0
for submission in `find $1 -maxdepth 1 -type d | sort` ; do
    results="$submission/results.txt"
	if [ -a $results ] ; then
        if [ "$i" -eq "0" ] ; then
            printf "id\t"
            head -1 $results
        fi
        ((i++))

        printf "`basename $submission`\t"
        tail -1 $results
	fi    
done | sort -n # | column -t

