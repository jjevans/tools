#!/usr/bin/env perl
use strict;
 
 ###!!!REQUIRE SORTED!!!
 
# print all samples having the inputted variant position

my $formcol = 9;#format column number

#input is a file is a coordinate or range of coordinates
# chromosome:position or chromosome:positionA-positionB
#output format is position<tab>sample id<nl>
# where position is format chromosome:position
#all ranges will be outputted position by position 
die "usage: vcf_smpl_pull.pl vcf_file coordinate(s) sorted(optional, yes=1)\n  single coordinate or range of format: \n  chromosome:position or chromosome:positionA-positionB\n" unless @ARGV == 2;
my $vcffile = $ARGV[0];
my $coord = $ARGV[1];
my $sorted = $ARGV[2];

#split coordinates into start, stop 
# with stop undef if single position
die "coordinate invalid: ".$coord."\noutput format: chr:pos or chr:posA-posB\n" unless $coord =~ /^(.+?):(\d+)-?(\d*)$/;
my $chr = $1;
my $start = $2;
my $stop = $3;

#a little validity check
my @range;
if(defined($stop) && $stop < $start){
	die "coordinate range must be least to greatest (start <= stop)\n";
}
elsif(defined($stop)){
	@range = [$start..$stop];
}
else{
	@range = ($start);
}
print join(":::",@range)."\n";


open(VCF,$vcffile) || die "Cannot open inputted vcf file.\n";
while(<VCF>){
	s/\n$//;
	my @smpls = split(/\t/,$_);
	my @vcfcol = splice(@smpls,0,$formcol);
	
	if($vcfcol[0] eq $chr){
		
		if(defined($stop)){
			for(my $i=$start;$i<$stop;$i++){
					
			}				
		}
	}
}
close(VCF);

exit;

sub fetch_smpl{
	#return arr of samples in a list of samples
	# pass in arr of all samples with no 
	# other vcf columns (typically 1-10).
	my $smpls = $_[0];
	
	my @present;
	foreach my $smpl (@$smpls){
		push(@present,$smpl) if ($smpl ne "" && $smpl ne ".");
	}
	
	return \@present;
}