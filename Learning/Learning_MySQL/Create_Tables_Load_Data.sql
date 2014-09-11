CREATE TABLE `DnaE_sequences`.`Fasta Sequences` (
  `Header` VARCHAR(100) NOT NULL DEFAULT 'Empty',
  `Sequence` VARCHAR(3000) NOT NULL DEFAULT 'A',
  PRIMARY KEY (`Header`));