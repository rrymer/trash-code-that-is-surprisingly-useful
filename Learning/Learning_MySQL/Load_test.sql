load data local infile '~/Downloads/tax_report-4.txt' 
	replace
	into table DnaE_sequences.Test
		fields
			terminated by '\t'
			escaped by '|'
		lines
			terminated by '\n'
(@dummy,Organism_ID,Organism,Lineage);