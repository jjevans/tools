use strict;
use Data::Dumper;

####
#jason evans, 05-29-2014
#matt lebo
#bioinformatics
#partners personalized medicine
####

####
#NCBI e-PCR
#DERIVES FROM PDP POST-PROCESS ALIGNMENT (pdp_aln.pm)
#runs e-PCR on the inputted reference seq 
#outputs each primer pair and their positions
##
#main routine is &align_primer which 
# converts the uploadfrm/report into the 
# e-PCR sts format, runs e-PCR, 
#returns genomic coordinates in bed format
#input files to &align_primer:
#	PDP final uploadForm.txt (upload form)
#	PDP report file (intermediate)
##
#!!!This does create one intermediate file for e-PCR input
#make sure to manage the files either by 
# using &cleanup which rm the file on success 
# or rm manually, self.
####

package epcr_util;
sub new{ 
	# requires a reference sequence. margin default 2000
	my($class,$atts) = @_;
	
	my $self = {
		reference => $atts->{reference},
		epcr_in => $atts->{input_file} || "pdp_epcr_in.tbl",
		epcr_out => $atts->{output_file} || "pdp_epcr_out.tbl",
		verb => $atts->{verbose},
		mask => $atts->{mask_lowercase},
		epcr_margin => $atts->{margin} || 2000,
		epcr_ampl_len => $atts->{ampl_len} || 1000,
		epcr_print_cmd => $atts->{print_cmd} || 0,
		delim => $atts->{delimiter} || "|",
		shift_left => $atts->{shift_left} || 0,
		cleanup => $atts->{cleanup} || 1
	};
		
	return bless $self,$class;
}

sub dump{
	my $self = shift;
	
	print Data::Dumper->Dump([$self]);
	
	return;
}

sub align_primer{
	#run epcr on primers
	#input is arr ref of lines of the input file
	# if key "upload_form" is 1, then parses 
	# the input at a pdp output uploadForm file.
	# otherwise, assumes a report file. 
	# (Final_report_for_project_....csv) 
	#!temporary file for epcr sts output written 
	# and removed is defined in constructor
	#returns hash of primer pairs and their coords
	#if no match found the value of that pair 
	# in the hash will be undef.
	my $self = shift;
	my $infile = $_[0];


	my $sts_lines;
	if($self->{"upload_form"}){#pdp uploadForm

		$sts_lines = $self->upload_to_sts($infile);
	}
	else{#report file

		$sts_lines = $self->report_to_sts($infile);
	}

	my $epcr_sts = $self->{"epcr_in"};
	my %pairs;
	my @ids;
	
	open(STS,">$epcr_sts") || die "ERROR: pdp_aln->align_primers()\nCannot open temporary file: ".$epcr_sts."\n";	
	foreach my $sts_line (@$sts_lines){

		print STS $sts_line;
		
		#track id
		my($pair_id,$rest) = split(/\t/,$sts_line,2);
		$pairs{$pair_id}++;

	}
	close(STS);


	my $gcoord = $self->epcr_gcoord($self->{"epcr_in"});
	
	#doublecheck all pairs align
	#remove those ids where alignment found
	foreach my $id (keys(%{$gcoord})){
		delete($pairs{$id});
	}
	
	#unaligned primer pairs
	# add to gcoord hash with value undef
	foreach my $noaln (keys(%pairs)){
		$gcoord->{$noaln} = undef;
	}
		
	return $gcoord;
}

sub report_to_sts{
	#convert the csv (read into array)
	# into an epcr sts (also in array)
	#amplicon length already set in constructor
	#!!!reads from a filehandle!!!
	my $self = shift;
	my $report = $_[0];

	#pair id delimiter
	my $delim = $self->{"delim"};
	
	my @sts;
	
	open(RPRT,$report) || die "pdp_aln->report_to_sts: cannot open report file: ".$report."\n";
	while(my $pair = <RPRT>){
		chomp($pair);
		my @vals = split(/\,/,$pair);

		#skip the ones without designs (have 0s in 4th col)
		next if $vals[3] eq "0";

		#make pair id, delim from construct
		# f and r id and len joined by delimiter defined above
		my $pair_id = $vals[2].$delim.length($vals[3]).$delim.$vals[4].$delim.length($vals[5]);

		my $sts_entry = $pair_id."\t".$vals[3]."\t".$vals[5]."\t".$self->{"epcr_ampl_len"}."\n";

		push(@sts,$sts_entry);
	}
	close(RPRT);
	
	return \@sts;
}

sub upload_to_sts{
	#convert the old (orig version) uploadForm 
	# table into epcr sts format
	#amplicon length already set in constructor
	#!!!reads from a filehandle!!!
	my $self = shift;
	my $upload = $_[0];

	#pair id delimiter
	my $delim = $self->{"delim"};
	
	my @sts;

	open(UPLD,$upload) || die "pdp_aln->upload_to_sts: cannot open upload file: ".$upload."\n";
	<UPLD>;#skip header
	while(my $pair = <UPLD>){
		chomp($pair);

		my @vals = split(/\t/,$pair);

		#no designs (have 0s in 8th col)
		if($vals[7] eq "0"){

			#print stdout no design if set in constructor
			if($self->{"print_nodesign"}){
				print STDERR "No design for target: ".$vals[0].", exon ".$vals[4]."\n";
			}
		}
		else{#proper design

			#make pair id, delim from construct
			# f and r id and len joined by delimiter defined above
			my $id_l = $vals[0].".".$vals[2].".".$vals[6];
			my $id_r = $vals[0].".".$vals[2].".".$vals[8];

			my $pair_id = $id_l.$delim.length($vals[7]).$delim.$id_r.$delim.length($vals[9]);
		
			my $sts_entry = $pair_id."\t".$vals[7]."\t".$vals[9]."\t".$self->{"epcr_ampl_len"}."\n";

			push(@sts,$sts_entry);
		}
	}
	close(UPLD);

	return \@sts;
}

sub epcr_gcoord{
	#run epcr on the inputted epcr sts input file
	#optional input is path to epcr, default e-PCR in path
	#epcr margin, mask lowercase, temp sts file 
	# and sequence reference file set in constructor
	#uses a command pipe to run epcr with a system call
	#returns hash of primer pairs with the col2 pair id 
	# as key and value of arr with cols
	# chr, start, stop, strand
	#if construct shift_in is 1 then shifts coords to 3' primer
	my $self = shift;
	my $sts_file = $_[0];
	my $epcr_cmd = $_[1];#optional epcr path
	$epcr_cmd = "e-PCR" unless defined($epcr_cmd);#default in PATH

	my $format = 3;#epcr output
	
	#$epcr_cmd .= " -o ".$self->{'epcr_out'};
	$epcr_cmd .= " -t ".$format;

	#epcr range of amplicon lengths for each pair
	$epcr_cmd .= " -m ".$self->{'epcr_margin'} if defined($self->{'epcr_margin'});

	#mask 5' lowercase (T3/T7)
	$epcr_cmd .= " -x ".$self->{'mask'} if defined($self->{'mask'});
	
	$epcr_cmd .= " ".$self->{'epcr_in'}." ".$self->{'reference'};
	
	print $epcr_cmd."\n" if $self->{"epcr_print_cmd"};
	
	my %pairs;

	open(my $epcr_pipe,"-|",$epcr_cmd) || die "pdp_aln->epcr_gcoord: cannot open command pipe for epcr.\n";
	while(<$epcr_pipe>){
		my @col = split;

		#shift coord to left side of primer coordinate 
		# this makes it so on match + strand, 
		# the reverse end of both primers 
		#amplicon doesn't include primers
		if($self->{"shift_left"}){
			my($lid,$llen,$rid,$rlen) = split(quotemeta($self->{"delim"}),$col[1]);

			my $lnew;
			if($col[2] eq "+"){
				$lnew = $col[4] - $rlen;
			}
			else{
				$lnew = $col[4] - $llen;
			}

			$col[4] = $lnew;
		}
		
		$pairs{$col[1]} = [$col[0],$col[3],$col[4],$col[2]];
	}
	close($epcr_pipe);

	#rm intermediate file if designated
	if($self->{'cleanup'}){
		$self->cleanup;
	}
	
	return \%pairs;
}

sub cleanup{
	#remove epcr input and output files
	my $self = shift;

	#do filecheck
	unlink($self->{"epcr_in"}) || warn "Cannot remove epcr file: ".$self->{"epcr_in"};

	return;
}

1;

#example e-PCR command
#e-PCR -m 1750 -t 3 -x + -o oms_f_r.epcr.tbl -v + oms_f_r.sts hg19.fa
