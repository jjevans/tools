#!/usr/bin/env perl
use strict;

#pull out value of INFO field tag inputted on cmd line
#append to sample field, put tag in format field.
#outputs converted vcf to stdout, 
# but with tag removed from INFO and
# value to sample data
#puts value in sample col. null value 
# gets $na (default ".") so possible to 
# have sample col of ".:2:.:.".

##DEFAULTS
my $na = "NA";
my $rm_tag_info = 0;
my $sub_head_def = 0;#boo to say the FORMAT is not INFO in header
my $line1 = 1;#checks for tag in FORMAT in 1st variant only


##INPUT
die "usage: info_tag.pl file.vcf DP\n" unless @ARGV == 2;
my $vcf = $ARGV[0];
my $tag = $ARGV[1];


##ERROR strings for parse/sub field problem
# errors: 1. tag def cannot be sub from FORMAT to INFO (invalid output vcf)
#		2. tag of INFO field exists in variant INFO, but not defined in header
my $tagdef_err = "ERROR: Tag \"".$tag."\" not defined in header.\nAttempt to convert tag definition from INFO to FORMAT failed.\nOutput will not be valid VCF.\n"; 
my $notag_err = "ERROR: Inputted tag \"".$tag."\" isn't found in INFO column.\n";


##CONVERT	
my $header;#contains header to print only if conversion good

open(VCF,$vcf) || die "cannot open vcf file.\n";
while(<VCF>){
	my $output;
	
	if(/^\#/){#gather header
		$header .= $_;
	}
	else{#variant line	
	
		##Evaluate presence of tag
		#dies if can't substitute tag def from FORMAT to INFO in header
		#if($line1 && $header=~s/\#\#INFO=\<ID/\#\#FORMAT/){
		#if($line1 && $header=~s/\#\#INFO(=\<ID=$tag\,)/\#\#FORMAT\1/){
		#if($line1 && $header =~ s/\#\#INFO(=\<ID=$tag.*?\n)/\#\#FORMAT\1/g){
		#if($line1 && $header =~ s/\#\#FORMAT(=\<ID=$tag.*?\n)/\#\#INFO\1/){
		if($line1 && $header =~ /\#\#FORMAT(=\<ID=$tag.*?\n)/){#\#\#INFO\1/){
			print $1." ho\n";
			print $header;#on 1st line print header since no err
			$line1 = 0;
		}
		else{
		print $1." yo\n";
			die $tagdef_err;
		}
		
		chomp;
		my @col = split(/\t/,$_);
		my @newcol = @col;

		
		#make sure on first variant to 
		# die if tag not in FORMAT col
		#if($line1 && $col[8] !~ /$tag/){
		#	die $notag_err;
		#}
		#else{#good input so print header
		#	$line1 = 0;
			
		#	print $header;
		#}

		my $fld_ref = info_arr($col[7]);
		
		my $res;
		if(defined($fld_ref->{$tag})){#assign and rm from INFO
			$res = $fld_ref->{$tag};

			delete($fld_ref->{$tag});
		}
		else{#default no value
			$res = $na;
		}
		
		#piece together INFO col
		my $info;
		for my $key (keys(%{$fld_ref})){
			$info .= ";".$key."=".$fld_ref->{$key};
		}
		
		$info =~ s/^\;//;
		$newcol[7] = $info;

		$newcol[8] .= ":".$tag;
		$newcol[9] .= ":".$res;

		$output = join("\t",@newcol)."\n";
	}
	
	print $output;
}
close(VCF);

exit;


sub tag_id{
	#from a FORMAT or INFO header definition, 
	# return the tag id
	#return 0 if no tag retrieved
	
	if(/\#\#.+?=\<ID=(\w+?)\,/){
		return $1;
	}
	
	return 0;
}

sub tagdef_arr{
	#parse header to get the columns for each INFO field
	return;
}

sub info_arr{
	#make hash with tag as id and value as value
	# from the info column. each tag has own elem.
	my $info = $_[0];

	my @entries = split(/\;/,$info);
	
	my %fields;
 	for my $entry (@entries){
 		my($tag,$val)=split(/=/,$entry);
 		$fields{$tag} = $val;
 	}
 	
	return \%fields;
}

