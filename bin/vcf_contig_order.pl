#!/usr/bin/env perl
use strict;

#from a list of contig ids in correct sort order, 
# reorder the header in the inputted (stdin) vcf 
# and output the contig order in that sort order.
#appends any contigs not in reference list to end
#output is not sorted, but has the order in the 
# header to correctly sort using vcftools sort
#input is vcf on stdin and argument of list of 
#contig ids (match vcf) in a 1 col file

die "usage: cat file.vcf | vcf_contig_order.pl list_file_of_correctly_sorted_contig_ids\n" if @ARGV != 1;
my $order_file = shift(@ARGV);


#read new sort order
open(my $order_fh,$order_file) || die "Cannot open list file with correctly sorted contig ids: ".$order_file."\n";
my @sort_order = <$order_fh>;
close($order_fh);


#gather contig declarations from header, resort, reinsert
my %contig;
while(<STDIN>){
	

	if(/^\#CHROM/){#last header line, sort, print contig

		my $sorted = reorder_contig(\%contig,\@sort_order);
		
		print join("",@{$sorted}).$_;		
	}
	elsif(/^\#\#contig=\<ID=(.+?),.*$/){
		$contig{$1} = $_;
	}
	else{
		print;
	}

}

exit;

sub reorder_contig{
	#reorder values of hash based on key order
	my $data_hsh = shift;#hash
	my $order_arr = shift;#arr
	
	my @reorder;
	foreach my $order (@{$order_arr}){
		chomp($order);
		
		if(defined($data_hsh->{$order})){
			push(@reorder,$data_hsh->{$order});
			delete($data_hsh->{$order});
		}
		else{
			die "ERROR: Contig does not exist in VCF: ".$order."\n";
		}
	}
	
	return \@reorder;
}