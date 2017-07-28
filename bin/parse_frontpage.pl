#!/usr/bin/env perl
use strict;

my @flds = ("report","gpp","panel","version","patient","variant","pathogenicity","gene"); 
my $char0 = "[";
my $char1 = "]";

open(my $f, $ARGV[0]) || die;
my $allout = "";
foreach my $line (<$f>){
	#my @info=split(/\Q$char0,$char1/, $line); 
	my @info=split(/\Q[/, $line); 
	
#	$info[-1]=~s/\n//;
#	$info[-1]=~s/,+$//;
#	$info[-1]=~s/\Q]//g;
	
	my $counter  = 0;
	foreach my $entry(@info){ 
	$entry=~s/\n//;
	$entry=~s/,+$//;
	$entry=~s/\Q]//g;

		$counter++;
		my @vals=split(/,/, $entry); 
		
		if(@vals==0){ next }
		
		#$vals[-1]=~s/\n$//;
		#$vals[-1]=~s/\Q$char1//; 
		
		my $output;
		for(my $i=0; $i<@flds; $i++){ 
			$output .= ',"'.$flds[$i].'":'.$vals[$i];
		}
		$output =~ s/^,//;
		 print "{".$output."}";
		
#		last if $counter >= 50;

	}
}
$allout =~ s/^,+//;
#print "[".$allout."]\n";

exit;