#!/usr/bin/env perl
use strict;
use Cwd;

#remove all files that 
# end in ".err" or ".out" 
# in the cwd.
# which i tend to put in my 
# bsub commands for writing 
# stderr/stdout to files.
#
my $currdir = getcwd;

#fetch .err/.out files
opendir(DIR,$currdir) || die "Cannot inspect this directory.\n";
my @files = grep{(/\.err$/ || /\.out$/)} readdir(DIR);
close(DIR);

foreach my $file (@files){
	chomp($file);
	unlink($file) || warn "Cannot remove file: ".$file."\n";
}

print "cwd=".$currdir."\nrm file: ".join("\nrm file: ",@files)."\ntotal files: ".@files."\ndone.\n";

exit;

