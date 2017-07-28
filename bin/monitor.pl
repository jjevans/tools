#!/usr/bin/env perl
use strict;

#loop over bjobs and print to screen every 2 seconds
#ONLY PRINTS RUNNING JOBS if arg provided with value 'RUN'.
#otherwise prints all jobs
#shows all of pcpgm's jobs (whole group) if 
# arg exists and has the value 'ALL'

#one optional args
# any value in argv[0] shows all jobs otherwise just running

my $only_run=0;
$only_run = 1 if $ARGV[0] eq "RUN";

my $show_grp=0;
$show_grp = 1 if $ARGV[0] eq "ALL";


#args
my $numsec = 3;#num sec between iterations

my $cmd = "bjobs";#start of cmdline
$cmd .= " -u all | grep pcpgm" if $show_grp;#show all queued biofx jobs


while(1){

    print "### ".localtime()."\n";

    my $response=`$cmd`;
    
    my $run = 0;
    my $pend = 0;
    my $susp = 0;
    my $tot_job = 0;
    my $other = 0;#not susp, pend, run, its some other status
	
    my @lines = split(/\n/,$response);
    shift(@lines);#pop of header
    
    foreach my $line(@lines){
		
		$tot_job++;

		if($line =~ /PEND/){#pending jobs
       	    $pend++;
       	    next if $only_run;
       	}
		elsif($line =~ /SUSP/){#suspended jobs
       	    $susp++;
       	    next if $only_run;
       	}
		elsif($line =~ /RUN/){#weird state, not pend, susp, run
			$run++;
		}
		else{
			$other++;
			next if $only_run;
		}
		
		print $line."\n";
    }
	
	print "############\n##Stats\n";
	print "#Jobs Running: ".$run."\n";
    print "#Jobs Pending: ".$pend."\n";
    print "#Jobs Suspended: ".$susp."\n";
    print "#Jobs in Other State: ".$other."\n";
    print "#Jobs Total: ".$tot_job."\n";
    print "############\n\n";
    
    sleep($numsec);
}

exit;
