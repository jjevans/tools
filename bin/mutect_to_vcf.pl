#!/usr/bin/env perl
use strict;

while(<>){
	
	my @col=split(/\t/,$_);print $col[0]."\t".$col[1]."\t".$col[5].":".$col[0].":".$col[1].":".$col[3].":".$col[4]."\t".$col[3]."\t".$col[4]."\t.\t.\t.\t.\n";
}

exit;

