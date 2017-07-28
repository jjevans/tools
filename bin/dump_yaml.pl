#!/usr/bin/env perl
use strict;
use Data::Dumper;
use YAML::XS ("LoadFile","Dump");

# perl script to read in and print out yaml file
# validates by loading and dumping yaml to screen
# prints data structure to screen using Dumper, 
# alternatively can use Dump to print yaml format again

die "usage: dump_yaml.pl yaml_file dump_data_or_yaml (optional;data=0,default;yaml=1)\n" unless @ARGV > 0;

my $conf = LoadFile($ARGV[0]);

if(defined($ARGV[1]) && $ARGV[1]){# dump yaml
	print Dump($conf)."\n";
}
else{#default data dumper
	print Dumper $conf;
}

exit;
