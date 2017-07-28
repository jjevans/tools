#!/usr/bin/env perl
use strict;
use Env ("PATH");

#!!!UNFINISHED!!!
#recurse directory and add all directories 
#to the unix PATH environmental variable
#!BE CAREFUL!

my $path = "/PHShome/jje16/Sandbox";

my @rootdir = [$path];

my @dirs = &id_dir(\@rootdir,$path);

exit;

sub id_dir{
	#return any directories in a passed in directory
	#used to recurse through a directory tree
	my $dirarr = $_[0];
print "@{$dirarr}\n";
	foreach my $subdir (@{$dirarr}){

		opendir(my $handle,$subdir) || die "Cannot open directory: ".$subdir."\n";

		my @moredirs = grep{ !/^\./ && -d "$subdir/$_" } readdir($handle);
		&id_dir(@moredirs);
	}

	print "@$dirarr\n";
	return $dirarr;
}

