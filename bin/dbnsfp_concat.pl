#!/usr/bin/env perl
use strict;

my $chunk_len = 40000000;#4GB read/write chunk

#from a list of dbnsfp filenames on stdin 
# concatenate them all into one text 
# file, optional bgzip, tabix index
#input is a list of filenames on stdin 
# and argument of an output filename, 
# any 2nd argument provided will skip  
# bgzip and tabix
my $ex = "X";#x chr
my $why = "Y";#Y chr

die "usage: ls files | dbnsfp_concat.pl output_filename tabix_index(optional, default 0, no)\n" if -t STDIN || !defined($ARGV[0]);
my $outfile = $ARGV[0];
my $no_index = $ARGV[1];#bgzip/tabix unless defined

#list of sorted files
my %files;

#figure filenames
while(<STDIN>){
	chomp;
	
	#get chr num from ext, hash of chr # key, value filename
	if(/\.chr(.+)$/){
		my $chr = $1;
		
		if(exists($files{$chr})){#somethings wrong
			die "chromosome file already exists.\n\tthis file: ".$_."\n\texisting file: ".$files{$chr}."\n";
		}
		else{
			$files{$chr} = $_;
		}
	}
	else{
		warn "file extension didn't parse, chromosome number unknown: ".$_."\n\tskipping...\n";
	}

}

#get X and Y filenames to append at end
my($x,$y);
if(exists($files{$ex})){#X chr
	$x = $files{$ex};
	delete($files{$ex});
}
else{
	warn "No X chromosome file found.\n";
}

if(exists($files{$why})){#Y chr
	$y = $files{$why};
	delete($files{$why});

}
else{
	warn "No Y chromosome file found.\n";
}

#sort filenames
my @ordered = sort numerically (keys(%files));

#print header boo
my $header_already = 0;

#output file
open(my $out_fh,">$outfile") || die "Cannot open output file to write: ".$outfile."\n";

print "begin.\n";

#concatenate files
foreach my $order (@ordered){
	
	open(my $in_fh,$files{$order}) || die "Cannot open input file: ".$order."\n";
	
	my $header = <$in_fh>;#take off header
	
	unless($header_already){
		print $out_fh $header;
		print "finished writing header.\n";
		$header_already = 1;
	}
	
	process_file($in_fh,$out_fh,$chunk_len);

	close($in_fh);

	print "completed processing: ".$files{$order}."\n";

}

#print X and Y
if(defined($x)){
	open(my $in_fh,$y) || die "Can't open X chromosome file: ".$x."\n";
	<$in_fh>;#rm header
	
	process_file($in_fh,$out_fh,$chunk_len);
	
	close($in_fh);
	print "completed processing: ".$x."\n";
}
if(defined($y)){
	open(my $in_fh,$y) || die "Can't open Y chromosome file: ".$y."\n";
	<$in_fh>;#rm header

	process_file($in_fh,$out_fh,$chunk_len);
	
	close($in_fh);
	print "completed processing: ".$y."\n";
}

close($out_fh);

unless(defined($no_index)){
	print "indexing file: ".$outfile."\nexecuting bgzip and tabix...\n";
	my $bgzip = tabix($outfile);
	print "completed index.\ncreated files:\n\t".$bgzip."\n\t".$bgzip.".tbi\n";
}

print "done.\n";

exit;

sub process_file{
	#read and write chunks to output file
	#input is an input filehandle, 
	#output filehandle, and chunk size (optional, default 500MB)
	my $chunk_len = 500000;#500MB default
	my $in_fh = $_[0];
	my $out_fh = $_[1];
	$chunk_len = $_[2] if defined($_[2]);

	my $chunk;
	while(read($in_fh,$chunk,$chunk_len)){
		print $out_fh $chunk;
	}

	return;
}

sub tabix{
	#bgzip and tabix index inputted file
	my $file = $_[0];
	my $bgzip = $file.".gz";#returned, but not specified to bgzip

	my $cmd = "bgzip ".$file;
	system($cmd);# || die "could not execute bgzip command: ".$cmd."\n";
	
	$cmd = "tabix -s 1 -b 2 -e 2 $bgzip";
	system($cmd);# || die "could not execute tabix command: ".$cmd."\n";;
	
	return $bgzip;
}
	
sub numerically { $a <=> $b }
