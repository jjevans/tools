#!/usr/bin/env perl
use strict;
#use Data::Dumper;print Dumper(config) to get data structure
use YAML::XS ("LoadFile","Dump");

# perl script to read in and print out yaml file
# validates by loading and dumping yaml to screen
# prints data structure to screen using Dumper, 
# alternatively can use Dump to print yaml format again

die "usage: isa_config.pl yaml_file\n" unless @ARGV == 1;

my $config = LoadFile($ARGV[0]);

print &recurse_struct($config,"","")."\n";

exit;


sub recurse_struct{
	#do recursion on structure to print out its key/value pairs
	my $struct = $_[0];
	my $name = $_[1];
	my $retstr = $_[2];

	if(ref($struct) eq "HASH"){

		foreach my $key (keys(%$struct)){
			my $info = &recurse_struct($struct->{$key},$key);
			$retstr .= $info if $info ne "";
		}
	}
	elsif(ref($struct) eq "ARRAY"){
		
		foreach my $item (@$struct){
			my $info = recurse_struct($item,$name,$retstr);
			$retstr .= $info if $info ne "";
		}
	}
	elsif(ref($struct) eq ""){
		return $name."=".$struct.";";
	}
	
	return $retstr;
}