#!/usr/bin/perl 

#Call examples:
#Note: on Windows, DOS promt "" is needed instead of ''
# perl shmrwww_example.pl --groups '9 5 3 8 8' shmr.ali
# perl shmrwww_example.pl shmr.ali --groups '9 5 3 8 8'
# perl shmrwww_example.pl --groups '9 5 3 8 8' --blast shmr.ali
# perl shmrwww_example.pl --groups '9 5 3 8 8' --refseq_id 'gi|18655485' --pdb_id 1KHX --chain A shmr.ali

use warnings;
use strict;
use LWP::UserAgent;
use HTTP::Request::Common qw(POST);
use Getopt::Long;

my ($pdb_file, $pdb_id, $chain, $refseq_id) = ('') x 4;
my $groups;
my $blast = 0;

my $result = GetOptions(
		"groups=s" => \$groups, 
		"refseq_id=s" => \$refseq_id,
		"pdb_id=s" => \$pdb_id, 
		"chain=s" => \$chain, 
		"pdb_file=s" => \$pdb_file,
		"blast" => \$blast) || die "Could not parse commandline options\n";


my $file = $ARGV[0] or die "Provide the filename of your alignment file as argument:\n perl $0 --groups \"<sizes per group>\" <filename>\n";
die "Supply alignment files and groups" unless $file && $groups;

#See parameters for POST below __END__
my $req = (
POST 'http://www.ibi.vu.nl/programs/shmrwww/index.php?tool=shmr-lwp',
	Content_Type => 'form-data',
	Content => [
		ali_file => [ $file ],
		groups => $groups,
		id_refseq => $refseq_id,
		pdb_id => $pdb_id,
		pdb_file => [ $pdb_file ],
		chain => $chain,
		blast => $blast,
	]
);

my $ua = LWP::UserAgent->new; 
my $response = $ua->request($req);
my $resloc = $response->header("Location");

warn "URL (for $file): $resloc\n";

$response = $ua->get("$resloc/status");

#Wait for completion
my $i = 0; 
while ($response->content !~ /^(?:1|2)/ and $i < 200) {
	sleep 5;
	$response = $ua->get("$resloc/status")
}

sleep 1; #for arrival of job...

# If status 2: problems...
if ($response->content =~ /^2/){ 
	my $str = '';
	$response = $ua->get($resloc);
	if ($response->is_success) {
		$str = join("\n", $response->content =~ /(ERROR:.+)/g);
		$str =~ s/<br>//g;
	}
	die "Your job experienced errors:\n$str\n";
}

$response = $ua->get($resloc);
my $content = $response->content;

#Get HTML page	
if (not $response->is_success or $content =~ /Software error/) { #no status header for error generated!
	warn "Status: ", $response->status_line, "\n";
	die "An error occured with submitting and/or processing your query.\n";
} else {
	print "$content\n";
}

#Get output files... (we do not check if response is successful)
print $ua->get("$resloc/SH.out")->content;
print $ua->get("$resloc/MR.out")->content;



__END__
#PARAMETERS:
# input type="file" name="ali_file"	Alignment file for upload (required)
# input type="file" name="groups_file"  (not used: groups file)
# input type="text" name="id_refseq"	id of reference sequence for output (optional)
# input type="text" name="pdb_id"	id of PDB structure (optional)
# input type="file" name="pdb_file"	PDB structure for upload (optional)
# input type="text" name="chain"	PDB chain id (optional)
# input type="checkbox" name="blast"	blast for matching PDB structure (optional)
# input type="hidden" name="mbjob[method]" value="shmr"
# input type="hidden" name="mbjob[description]" value="step 1"
# textarea name="ali"			(not used: alignment 'paste' field)
# textarea name="groups"		group definition

