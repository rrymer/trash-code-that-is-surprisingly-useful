#!/bin/zsh

working_dir='/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/':$working_dir
names=('DnaA' 'DnaB' 'DnaCI' 'SSB')
echo $working_dir
for n in $names ;
do 
echo $n;
mkdir $working_dir$n;
mkdir $working_dir$n$'/Data';
mkdir $working_dir$n$'/Analysis';
done
