#!/bin/bash

paths="DnaA DnaB DnaC DnaG"

basedir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/"

for p in $paths;
do echo $basedir$p-alignment;
done

for p in $paths;
	do 
		rm $basedir$p-alignment/Scratch/compiled_trees.txt;
		echo $p > $basedir$p-alignment/Scratch/compiled_trees.txt
		echo "tmp" > $basedir$p-alignment/Scratch/tmp.txt
done

for p in $paths;
    do for i in $basedir$p-alignment/Scratch/RAxML_bestTree*
    	do
        cat $basedir$p-alignment/Scratch/compiled_trees.txt $i > $basedir$p-alignment/Scratch/tmp.txt
        cat $basedir$p-alignment/Scratch/tmp.txt > $basedir$p-alignment/Scratch/compiled_trees.txt
    done
done

# cat fin fout > tmp
# tmp > fout