#!/bin/bash

paths="DnaA DnaB DnaC DnaG"

basedir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/"

for p in $paths; do for i in $basedir$p-alignment/Scratch*_aligned.fasta; do mv $i $basedir$p-alignment/Scratch/$i_aligned.fasta; done; done