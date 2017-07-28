#!/usr/bin/env perl
use strict;
use Math::BigFloat;

#jje16, msl34 05222015
#partners personalized medicine, bioinformatics

#make alternative frequencies from AC (pop size) and AN (alt count) in ExAC VCF.
#takes exac vcf on stdin, outputs vcf on stdout with a new 
# INFO field 'AF_???' substituted for ExAC's allele count 'AC_???'
#will output all AF, AC fields if not $only_subpop (AC_Hemi,AN_Hom,AC,AN)
#alternative freqs is ratio of AC (alt count) and AN (total population observed)
#finds like-population AN, AC on regex (ex. AN_AFR, AC_AFR)
#input is exac vcf file and a file with one column having the 
# INFO fields to extract. output on stdout
#returns a table with these columns
#chrom, pos, ref, alt, subpop_altfreq0, subpop_altfreq1, ...
#ignores all but fields with an "AN_" or "AC_".
my $only_subpop = 1;#no global statistics (only AC_AFR, not AC)
my $div0 = -1;#AN == 0 (div by 0), what should alt freq be

#usage
die "exac_altfreq.pl (exac vcf on stdin, vcf w/ alt freq inserted on stdout)\n" if -t *STDIN;

#INFO definition for alt freq
my $prefix = "AF";
my $sigdig = 0;#significant digits on the frequency, 0=no rounding

my %pops;
my @ordr;

my @head;
while(my $line=<STDIN>){
	#gather all INFO definitions in header and 
	# put them together with the allele freq (AF_) for 
	# each population having a pair AC_ and AN_ or AC/AN.

	if($line =~ /^\#CHROM/){#build, insert new INFO defs
	
		my $pops = gather_pop(\@head,1);

		my $infos = info_def($pops,$prefix);

		splice(@head,-1,0,@{$infos});
		push(@head,$line);

		print join("",@head);
	}
	elsif($line =~ /^\#/){#other header

		push(@head,$line);
	}
	else{#variant line

		my @col = split(/\t/,$line);
		$col[-1] =~ s/\n$//;
    
    	my $icol = $col[7];                          
		my $subpops = match_pop($icol,$only_subpop);#pair ANs with ACs for pops

		foreach my $subpop (keys(%{$subpops})){

			my @alt_cnt = split(/,/,$subpops->{$subpop}[0]);#ACs
			my $size = $subpops->{$subpop}[1];#AN pop size
			
			my $af_val;
			foreach my $cnt (@alt_cnt){#all alts

				my $value;
				if($size == 0){#pop size 0

					if($cnt == 0){
						$value = $div0;
					}
					else{#num alleles>all alleles, error

						die "ERROR: divide by zero, num obs (".$cnt.") > total counted (".$size."), pos: ".$col[0].":".$col[1].", population: ".$subpop."\n";
					}
				}
				else{#alt freq

					my $num = Math::BigFloat->new($cnt/$size);#ratio
					$value = $num->bround($sigdig);
				}
			
				$af_val .= $value.",";
			}
			
			$af_val =~ s/,$//;#trail
			
			#info keyval
			my $af_fld = $prefix."_".$subpop."=".$af_val;

			#add to info col
			$icol .= ";".$af_fld;
			$icol =~ s/^\;//;#lead
		}
		
		$icol =~ s/^\;//;#if leading semi
		
		$col[7] = $icol;
		print join("\t",@col)."\n";
	}
}

exit;

sub gather_pop{
	#from whole vcf header, find INFO definition lines, 
	# pair all populations having a matching allele count 
	# allele number pair for each pop. AC/AN 
	#allele count, allele num are ids having prefix AC_ or AN_, 
	#also finds the whole population 'AC','AN' and uses the 
	# value of 1 as its name
	#returns all pops that were paired in INFO defs in array
	# with no AC_, AN_ or AC, AN
	my $hlines = $_[0];
	my $only_subpop = 0;#all AC, AN values
	$only_subpop = $_[1] if defined($_[1]);#val of 1 only subpopulations	
	
	my %counts;
	my @pops;
	
	foreach my $hline (@{$hlines}){

		#INFO def line
		if($hline =~ /\#\#INFO=\<ID=(.+?),/){
		
			my $id = $1;
			my @parts = split(/_/,$id);
		
			if($parts[0] eq "AC" || $parts[0] eq "AN"){
				#increment num found for pop
			
				next if ($only_subpop && $parts[1] !~ /^[A-Z]{3}$/);
				
				$parts[1] = 1 unless defined($parts[1]);#whole pop
				
				#tally num times population has AC or AN, paired if 2 (both)
				if(!defined($counts{$parts[1]})){#one of AC/AN found previously

					$counts{$parts[1]} = 1;
				}
				elsif($counts{$parts[1]} == 1){#paired, seen 2X
				
					push(@pops,$parts[1]);
				}
				else{#duplicate pop AC/AN
					die "Error: duplicate population AC/AN: ".$id."\n";
				}
			}
		}
	}
	
	return \@pops;
}
		
sub match_pop{
	#from whole INFO col of vcf variant line, match all populations AC, AN
	# by regex.  ex. pairs AC_AFR with AN_AFR
	#returns hash of key subpop (AFR) with value a 2 elem array 
	# having the column number the AC, AN are in for it
	# array elem of undef if no column found
	#population name for whole population (AC, AN) will have the 
	# key of '1'.
	my $icol = $_[0];
	chomp($icol);
	
	my $only_subpop = 0;
	$only_subpop = $_[1] if defined($_[1]);
	
	my @flds = split(/\;/,$icol);
	
	my %pops;
	
	for(my $i=0;$i<@flds;$i++){#each colname
		my $ac = undef;
		my $an = undef;
	
		my($id,$val) = split(/=/,$flds[$i]);
		
		my @parts = split(/_/,$id);

		#subpopulations AC_AFR has two parts by _ and are all uppercase, 3 char
		next if ($only_subpop && $parts[1] !~ /^[A-Z]{3}$/);

		#set pop name to 1 if global population (AC, AN)
		$parts[1] = 1 unless defined($parts[1]);			

		#init arr if not exist
		my @cnt = defined($pops{$parts[1]}) ? @{$pops{$parts[1]}} : [undef] x 2;
		
		#get AC, AN
		if($parts[0] eq "AC"){
			$cnt[0] = $val; 
		}
		elsif($parts[0] eq "AN"){
			$cnt[1] = $val;
		}
		else{ next }#not an AN, AC field

		$pops{$parts[1]} = \@cnt;
		
		#populate
	}
	
	return \%pops;
}

sub info_def{
	#return arr of lines with INFO definitions for all 
	# groups in inputted array. 2nd input is optionally the prefix to 
	# append the population to (ex. AF)
	my $pops = $_[0];#arr

	my $prefix = "AF";#default INFO id
	$prefix = $_[1] if defined($_[1]);
	
	my $template = "Alternate allele frequency (exac AC/AN)";
	
	my @infos;#all new INFO defs
	
	foreach my $pop (@{$pops}){
		my $id = $prefix."_".$pop;
		my $desc = $template.", population: ".$pop;
		
		my $def = '##INFO=<ID='.$id.',Number=.,Type=String,Description="'.$desc.'">'."\n";
	 	push(@infos,$def);
	}

	return \@infos;
}
