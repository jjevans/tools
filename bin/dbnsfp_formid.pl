#!/usr/bin/env perl
use strict;

#!!!skips first line header!!!
#from a list of files (stdin), 
# create new file with 1st four 
# cols joined together as an 
# id (same table, but id inserted).
# output file = "id.".$infile ($_);
my $delim = "::";

die "usage: form_id_dbnsfp.pl  ((filenames on stdin))\n" if -t STDIN;

while(<>){
	chomp;

	open(my $db,$_) || die "Cannot open infile: ".$_."\n";
	<$db>;#header

	my $outfile = $_.".id.tbl";
	open(my $out,">$outfile") || die "Cannot open output file: ".$outfile."\n";

	print "processing...\n";
	print "\tinput file: ".$_."\n\toutput file: ".$outfile."\n";

	while(my $variant=<$db>){
		my @col = split(/\t/,$variant);
		print $out join($delim,@col[0..3])."\t".$variant;
	}

	close($out);
	close($db);

	print "\tfile complete.\n";
}

print "done.\n";

exit;

