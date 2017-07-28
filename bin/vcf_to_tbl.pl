#!/usr/bin/env perl
use strict;

#!!!not bug (don't think) as it looks like an 
# artifact that I left prior in the process.
#!!!has bug in some cases a .: will 
# not parse right leaving an INFO column 
# name like ".:AC" and won't populate right.
#!!!

#separate vcf into a table
#puts INFO fields in separate columns 
# taking the definitions from the header 
# and then putting the appropriate values 
# for each variant in those columns
#Input is a VCF and optional filename to output 
# the table.  By default prints to stdout.
#Header fields are INFO field ids 
#Prints to stderr the definitions of each 
# INFO field in the form of abbrev<tab>def<nl>
#INFO field values (if present) inserted between 
# FILTER column and FORMAT column.
#no value for a column is left empty in output
#logic: splice out INFO column and separate 
# into array of length determined by the number 
# of INFO fields defined in header.
# later inserted back into column array

##DEFAULT
#throw err and possibly die (default, proceed anyways)
#warn on err (undef),
# die on any err(1), 
# suppress all warnings(0) and proceed
my $die = 0;#warn/die, default only warn so watch output

my $print_desc = 1;#print INFO descriptions to stdout (1=yes)
my $flag_value = "TRUE";#value for a flag in info field
my $vcf_info_col = 7;#INFO col num

my $tbl;#output file (or stdout if undef)

##INPUT
die "usage: vcf_to_tbl.pl vcf_file_input tbl_file_output (optional,default=stdout)\n" unless @ARGV > 0;
my $vcf = $ARGV[0];
$tbl = $ARGV[1] if defined($ARGV[1]);


##OUTPUT provided file or stdout
##output, stdout or output file
my $out_fh;
if(defined($tbl)){
	open($out_fh,">$tbl") || die "Cannot open output file: ".$tbl."\n";
}
else{
	$out_fh = \*STDOUT;
}


##POPULATE FIELDS
#keeps all output in array of lines and prints at end
my @variantoutput;

my $head;
my @head_names;#array of column names
my $info_lookup;#hash ref of INFO field column numbers and descriptions
my $num_info;#number of INFO fields sep into cols

open(VCF,$vcf) || die "Cannot open vcf file.\n";
while(<VCF>){

	if(/\#\#/){#header definitions
		$head .= $_;
	}
	elsif(/\#CHROM/){#end of header
	#keep header names to insert INFO column names into		

		@head_names = split(/\t/,$_);
		$head_names[0] =~ s/^\#//;#remove initial pound
		$head_names[-1] =~ s/\n$//;
		
		#parse header for info fields
		$info_lookup = &header_lookup($head);
	}
	else{#variant lines

		#columns
		my @cols = split(/\t/,$_);
		$cols[-1] =~ s/\n$//;
	
		#separate INFO fields into its array
		#pull out info column to be parsed separately
		my @infos = split(/\;/,splice(@cols,$vcf_info_col,1));

		#initialize info array with empty elements
		my @info_cols = ("") x keys(%{$info_lookup});

		for(my $i=0;$i<@infos;$i++){
	
			#fields with equals sign (WHATUVA=blah)
			if($infos[$i]=~/^(\w+?)=(.+)$/){
			
				#Error from extraneous, undefined tag
				if(!defined($info_lookup->{$1})){			
					throw("ERROR: INFO field not defined in header: ".$1." ... skipping.\n");
				}
		
	 			$info_cols[$info_lookup->{$1}[0]] = $2;#populate INFO element value
			}
			elsif(defined($info_lookup->{$infos[$i]})){#flag=true
				$info_cols[$info_lookup->{$infos[$i]}[0]] = $flag_value;
			}
			else{#error, either id not in header or just loose value with no id at all
				throw("ERROR: INFO field with no id or not defined in header: ".$infos[$i]." ... skipping.\n");
			}
		}

			
		#insert info columns in 8th column (at vcf INFO)
		splice(@cols,$vcf_info_col,0,@info_cols);
	
		#add variant to table output array
		my $row = join("\t",@cols);
		push(@variantoutput,$row);
	}
}
close(VCF);

##HEADER
#create header by inserting INFO field names info regular header
# organize INFO names properly in array by going through each 
# field in the lookup
my @outhead = ("") x keys(%{$info_lookup});

if($print_desc){#print INFO descriptions to stderr
	print STDERR "##INFO fields:\n#ID\tTYPE\tNUMBER\tDESCRIPTION\n";
}

foreach my $name (keys(%{$info_lookup})){
	$outhead[$info_lookup->{$name}[0]] = $name;
	
	#print INFO descriptions to stderr
	if($print_desc){
		print STDERR $name. "\t" .$info_lookup->{$name}[1] . "\t" . $info_lookup->{$name}[2] ."\t". $info_lookup->{$name}[3]."\n";
	}
}

splice(@head_names,$vcf_info_col,1,@outhead);#removes "INFO"


##OUTPUT
print $out_fh join("\t",@head_names)."\n";#header
foreach my $outline (@variantoutput){
	print $out_fh $outline."\n" unless $outline eq "";
}

close($out_fh) if defined($tbl);

exit;

sub header_lookup{
	#creates a hash of INFO field 
	# abbreviation and the associated 
	# data for that field.
	#data associated is an array 
	# of 3 elements having these items:
	#	1. column number the field will 
	#		have in the table
	#	2. type of value (flag, number, etc)
	#	3. number of values possible in field
	#	4. description of that field
	#returns a hash of arrays having the 
	# field abbreviation as key
	#input is a vcf header 
	my $head = $_[0];
	
	my @lines = split(/\n/,$head);
	
	my %lookup;
	my $colnum = 0;
	foreach my $line (@lines){
		
		#if($line =~ /^\#\#INFO=.*?ID=(.+?),.*Type=(.+?),.*Description="(.+)".*$/){
		if($line =~ /^\#\#INFO=\<ID=(.+?),Number=(.+?),Type=(.+?),Description="(.+)"\>$/){
		
			my @fieldinfo = ($colnum,$3,$2,$4);

			$lookup{$1} = \@fieldinfo;

			$colnum++;
		}
		elsif($line =~ /^\#\#INFO/){
			#die if INFO parsed wrong in header, 
			# something is very wrong
			throw("ERROR: problem parsing INFO field:\n".$line,1);#die
		}
	}
	
	return \%lookup;
}

exit;

sub disassmbl_meta{
	#from vcf data definitions (FORMAT,INFO)
	return;
}

sub throw{
	#error handle
	#counts on global variable "$throw"
	#if value 0, warns or dies based 
	# on error.
	#if value 1, dies on any error.
	#if value 2, suppresses all 
	# warnings and proceed through errors
	#input is an error string to print to STDERR 
	# and optionally a 2nd arg (any, but undef) 
	# that, if present, dies.  otherwise warning.
	#var $die is global (our), but overridden 
	# with arg here
	my $err_str = $_[0];
	$die = $_[1] if defined $_[1];

	#make sure string ends up with one newline
	$err_str =~ s/\n+/\n/;
	
	if(defined($die)){
		#skips any value that != 1 (suppress)

		if($die){#always die (1)
			die $err_str;
		}
	}
	else{#warn
		warn $err_str;
	}
	return;
}