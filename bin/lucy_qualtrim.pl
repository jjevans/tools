#!/usr/bin/env perl
use strict;
use Getopt::Long;
#use washu_util;

####
#jason evans, 01102015
#matt lebo
#bioinformatics
#partners personalized medicine
####

#from fasta of sequence (.seq) and qualities (.qual),
# trim ends based on a dual sliding window for proper 
# quality sequence
#input is a fasta of seqs and quals (2) 
# and optionally are lengths of the small and 
# big windows
my $file_seq;
my $file_qual;
my $file_out;
my $fh_out = \*STDOUT;#default res to stdout

my $cutoff = 10;#phred 20 threshold
my $over_short = 4;#num good scores before considered good seq
my $over_long = 20;
my $size_short = 10;#window sizes
my $size_long = 50;

##run vals
GetOptions('s|seq=s'=>\$file_seq,
			'q|qual=s'=>\$file_qual,
			'o|out:s'=>\$file_out,
			'c|cut:i'=>\$cutoff,
			'n1|num-short:i'=>\$over_short,
			'n2|num-long:i'=>\$over_long,
			'w1|size-short:i'=>\$size_short,
			'w2|size-long:i'=>\$size_long);

#usage
#requires both phred seq and qual file
if(!defined($file_seq) || !defined($file_qual)){
	die "usage: lucy_qualtrim.pl -s seq.fasta -q qual.fasta\n
	Required args:
		-s phred_sequence_fasta
		-q phred_quality_fasta
	Optional args:
		-o output_file(default stdout)
		-c phred_score_cutoff(default 20)
		-w1 short_window_length(default 10)
		-w2 long_window_length(default 50)\n";
}


#handles
open(my $fh_seq,$file_seq) || die "ERROR: cannot open the phred sequence file (.seq): ".$file_seq."\n";
open(my $fh_qual,$file_qual) || die "ERROR: cannot open the phred quality file (.qual): ".$file_qual."\n";

#assign output to file if provided
if(defined($file_out)){
	open($fh_out,">$file_out") || die "ERROR: cannot open file to write output: ".$file_out."\n";
}

#change record delimiter to a full fasta record
my $rec_delim_orig = $/;
$/ = "\n>";

#process
while(my $seq=<$fh_seq>){
	
	#sequence
 	my($id_seq,$nt_seq) = groom_record($seq);
 	$$nt_seq =~ s/[\s ]+//g;#remove any weird space from seq
	my @calls = split("",$$nt_seq);
	
	#qualities
	my $qual = <$fh_qual>;
	my($id_qual,$nt_qual) = groom_record($qual,1);
	my @scores = split(" ",$$nt_qual);


	#confirm proper params
	die "ERROR: length of read shorter than long win.\nsequence id: ".$$id_seq."\nread len: ".@scores."\nwindow size: ".$size_long."\n" if @scores < $size_long;
	die "ERROR: SHORT WINDOW - required number of good scores exceeds length of window.\nrequired number: ".$over_short.", window length: ".$size_short."\n" if $size_short < $over_short;
	die "ERROR: LONG WINDOW - required number of good scores exceeds length of window.\nrequired number: ".$over_long.", window length: ".$size_long."\n" if $size_long < $over_long;


	#locate locations of seq to be trimmed
	my $index_f = trim(\@scores,$cutoff,$over_short,$over_long);

	my @score_r = reverse(@scores);
	my $index_r = trim(\@score_r,$cutoff,$over_short,$over_long);

	#make sure found location, otherwise poor quality read
	if(!defined($index_f) || !defined($index_r)){#move on
		print STDERR "Low quality read: ".$$id_seq."\n";
		next;
	}
	
	#start and stop of substr in a 2elem arr
	my $trim_coord = [$index_f,@scores-$index_r];
	my $goodseq = substr($$nt_seq,$trim_coord->[0],($trim_coord->[1]-$trim_coord->[0]));


	#output	
	print $fh_out ">".$$id_seq."\n".$goodseq."\n";
	
}
$/ = $rec_delim_orig;#assign orig rec. delim. for good measure

close($fh_out) if defined($file_out);
close($fh_seq);
close($fh_qual);

exit;


sub groom_record{
	#format the fasta record into id and single string values (seq,qual)
	my $treat_as_qual = 0;
	my $record = $_[0];
	$treat_as_qual = 1 if defined($_[1]);
	
	$record =~ s/\>//g;
	
	my @lines = split(/\n/,$record);
	
	my $id_rec = shift(@lines);
	$id_rec =~ s/^(.+?)\s.*$/\1/;

	my $nt_rec = join("",@lines);
	$nt_rec =~ s/\n//g;
	$nt_rec =~ s/ +$// unless $treat_as_qual;#trailing space
	
	return \$id_rec,\$nt_rec;
}

sub trim{
	#from an array of bases(nt) and respective scores, 
	#remove first base from array if num_good isn't 
	# greater than that required
	my $arr_score = $_[0];
	my $cutoff = $_[1];
	my $over_short = $_[2];
	my $over_long = $_[3];

	#init wins
	my @win_short = @$arr_score[0..$size_short-1];
	my @win_long = @$arr_score[0..$size_long-1];
	
	#slide
	for(my $i=0;$i<@$arr_score;$i++){
		my $good_short = num_good(\@win_short,$cutoff);	
		my $good_long = num_good(\@win_long,$cutoff);

		#evaluate if meets criteria
		if(($$good_short > $over_short) && ($$good_long > $over_long)){#done

			return $i;#trimmed arr and num bp trimmed
		}
		else{#slide again

			#drop current nt if not good
			shift(@win_long);
			shift(@win_short);

			#break out if not enough nt to add another to long win
			if(@$arr_score-$i<$size_long){
				$i=@$arr_score;
			}
		
			#slide
			my $next_long = $arr_score->[$i+$size_long];
			push(@win_long,$next_long);

			my $next_short = $arr_score->[$i+$size_short];
			push(@win_short,$next_short);
		}
	}
	
	return undef;
}

sub num_good{
	#counts the number of element ints exceed 
	# the inputted cutoff, returns num over thresh
	my $arr_score = $_[0];
	my $cutoff = $_[1];

	my $num_over = 0;

	map{$num_over++ if $_ > $cutoff} @{$arr_score};

	return \$num_over;
}
