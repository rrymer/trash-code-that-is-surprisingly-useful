#TRUNCATE `DnaG_sequences`.`Test`;
#select Output_Header, Aligned_seq as a from(
#select Output_Header, Phylum, Aligned_seq as b from `DnaG_sequences`.`All_DnaG_sequences` where
#group by Phylum) as seqs
#470 < cast(Length as unsigned) < 770 and `Pol-type` like 'iDnaG' and
#Phylum in (select Phylum as c from `DnaG_sequences`.`All_DnaG_sequences` group by Phylum having count(*) > 2 ))


#select Phylum, count(*) from `DnaG_sequences`.`All_DnaG_sequences` as b group by Phylum into outfile '/tmp/coverage.txt'
#fields terminated by '\t';

#load data local infile '/tmp/coverage.txt'
#into table `DnaG_sequences`.`Test`
#(Header, Coverage);

#update `DnaG_sequences`.`All_DnaG_sequences` a, `DnaG_sequences`.`Test` b set a.Coverage=b.Coverage where a.Phylum=b.Header;

#select * from `DnaG_sequences`.`All_DnaG_sequences` where Coverage is not Null;

select * 
from (
(select concat('Group:Reference', '|', Accession_Number, '|', Phylum), Aligned_seq from `DnaG_sequences`.`All_DnaG_sequences` where 
470 < cast(Length as unsigned) < 770 and `Pol-type` like 'iDnaG' and Phylum not like 'Firmicutes'
order by rand()
limit 400)
union all
#(select Output_Header, Aligned_seq from `DnaG_sequences`.`All_DnaG_sequences` where 
#470 < cast(Length as unsigned) < 770 and `Pol-type` like 'iDnaG' and Phylum='Bacteroidetes'
#order by rand()
#limit 100)
#union all
(select Output_Header, Aligned_seq from `DnaG_sequences`.`All_DnaG_sequences` where 
470 < cast(Length as unsigned) < 770 and `Pol-type` like 'iDnaG' and Phylum='Firmicutes'
order by rand()
limit 100)
#union all
#(select Output_Header, Aligned_seq from `DnaG_sequences`.`All_DnaG_sequences` where 
#470 < cast(Length as unsigned) < 770 and `Pol-type` like 'iDnaG' and Phylum='Proteobacteria'
#order by rand()
#limit 100)
) a
into outfile '/tmp/iDnaG_alignment_firms2.fasta'
fields terminated by '\n'
lines starting by '>';

#select Phylum, count(*) from `DnaG_sequences`.`All_DnaG_sequences` as b group by Phylum having count(*) > 100