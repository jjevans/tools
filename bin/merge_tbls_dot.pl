#!/usr/bin/env perl
use strict;

#jje16, msl34	07212015
#from output of merge_tbls.pl change the 
# val0:::val1 pair to "." if val0==val1
#input on stdin, output on stdout
#assumes header present
my $subval = ".";

die "usage: cat mrgtbls_output.tbl | merge_tbls_dot.pl > dot.tbl\n" if -t STDIN;

my $headline = <STDIN>;
print $headline;
#print <STDIN>;#header

while(<STDIN>){
	my @cols = split(/\t/,$_);
	$cols[-1] =~ s/\n$//;
	my $id = shift(@cols);

	for(my $i=0;$i<@cols;$i++){
		my($val0,$val1) = split(/:::/,$cols[$i]);
		
		$cols[$i] = $subval if $val0 eq $val1;
	}
	
	print $id."\t".join("\t",@cols)."\n";
}

exit;
