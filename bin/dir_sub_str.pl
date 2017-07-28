#!/usr/bin/env perl
use strict;
use Cwd;
use File::Copy;
use File::Find;
###!!!DOESN'T WORK YET!!!

#finds all filenames with an inputted 
# string (string1) and renames same filename, but 
# with string1 substituted for a 
# second inputted string, string2.
#also opens all text files and substitutes 
# any instance of string1 with string2
my @todel;
my @tomove;

#arg0 is a string to substitute with another string (arg1)
#optional 3rd arg supplies a directory to traverse 
# (default cwd)
die "usage: dir_sub_str.pl string1 string2 dir_to_traverse (optional, default cwd)\n" unless @ARGV > 1;
my $str_old = $ARGV[0];
my $str_new = $ARGV[1];
my $dir = $ARGV[2];#supplied or cwd


#dir
if(defined($dir)){#if provided, make sure dir exists
	die "ERROR: directory does not exist: ".$dir."\n" unless -d $dir;
}
else{#cwd unless provided
	$dir = getcwd()
}


#find files, modify text, copy orig file/tmpfile to new file
find(\&mod_file,$dir);

#move all files
move_file(\@tomove);

#remove all flatfiles with changes
# in case where filename mod and content mod 
# the new tmpfile is copied to new name and 
# requires the original file to be deleted separated
#delete original files
foreach my $rm_this (@todel){
	print "DELETING FILE: ".$rm_this."\n";
	unlink($rm_this) || die "Cannot remove file: ".$rm_this."\n";
	print "deletion complete.\n";
}


exit;

sub mod_file{
	#open all text files and substitute string1 for string2 
	# within it.  flag files for from&to filenames for copy (move)
	my $cp_pair;
	
	#default filenames to copy from and to
	#does nothing if from ends up the same as to
	my $from = $File::Find::name;
	my $to = $File::Find::name;
	
	#modify content
	if(-T){#flatfile
		my @content;#lines of text to write to file if change necessary
		my $change_made = 0;
		
		open(my $in,$from) || die "Cannot open text file for processing: ".$File::Find::name."\n";			
		while(my $line=<$in>){#find necessary modifications to file contents

			$change_made = 1 if $line =~ s/$str_old/$str_new/g;#mod

			push(@content,$line);
		}
		close($in);


		#write output if modification, flag for move
		if($change_made){
			my $tmpfile = "/tmp/".time()."-".rand(1000000000)."_temporary.txt";#hopefully uniq

			open(my $out,">$tmpfile") || die "Cannot open temporary file: ".$tmpfile."\n";
			foreach my $line (@content){
				print $out $line;
			}
			close($out);

			$from = $tmpfile;
		
			#push(@todel,$File::Find::name);
		}
	}	


	#filename mod
	if(s/$str_old/$str_new/g){
		$to = $File::Find::dir."/".$_;
	}
	
	$cp_pair = $from.":::".$to;

	#from&to filenames for copy in proper order 
	# of text files moved first and then dirs renamed
	if(-d){#directory (appends)
		push(@tomove,$cp_pair);#append
	}
	elsif(-T){#flatfile (prepend)
		unshift(@tomove,$cp_pair);
	}


	return \@tomove
}

sub move_file{
	#move files from hash of keys (old filenames) with 
	# values being the new filenames.  
	#!!!moves not copies!!!
	my $files = $_[0];
	
	foreach my $file (@{$files}){

		my($from,$to) = split(/:::/,$file);

		next if $from eq $to;#no changes

#		if($from eq $to){#no mods so do nothing
#			warn "yo: from same as to- ".$from."\n";
#			next;
#		}

		print "#MOVING FILE:\n\tfrom: ".$from."\n\tto: ".$to."\n";
		copy($from,$to) || die "ERROR: cannot move file\n\tfrom: ".$from."\n\tto: ".$to."\n";
		unlink($from);
		print "move done#\n";
	}

	return;
}
