load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Actinobacteria_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Actinobacteria_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Bacteroidetes_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Bacteroidetes_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Chlamydiae_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Chlamydiae_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Cyanobacteria_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Cyanobacteria_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Fermicutes_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Fermicutes_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Fusobacteria_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Fusobacteria_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Spirochaetes_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Spirochaetes_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Tenericutes_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Tenericutes_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byphyla/Thermotogae_etal_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.Thermotogae_etal_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);
load data local infile '/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byPoltype/PolC_nr_sequences.fasta' 
	ignore
	into table DnaE_sequences.PolC_sequences
		fields
			terminated by '\n'
		lines
			starting by '>'
(Header,Sequence);