use strict;
use Data::Dumper;


####
#jason evans, 11-19-2014
#matt lebo
#bioinformatics
#partners personalized medicine
####

####
#module for working with bedtools
##
# !!!runs bedtools through system
####

package bt_util;
sub new{ 
	# requires a reference sequence. margin default 2000
	my($class,$atts) = @_;
	
	my %types = {"bed"=>["a","b"],"bam"=>["abam","b"]};
	
	my $self = {
		#reference => $atts->{reference},
		#epcr_in => $atts->{input_file} || "pdp_epcr_in.tbl",
		executable => $atts->{executable} || "bedtools",
		tool => $atts->{tool} || undef,
#		tool_cov => $atts->{coverage} || "coverage",
#		tool_gcov => $atts->{genomecov} || "genomecov",
#		tool_isec => $atts->{intersect} || "intersect",
		bed => $atts->{bed} || undef,
		file => $atts->{file} || undef,
		type => $atts->{filetype} || "bed",
		ref => $atts->{reference} || undef
	};
		
	return bless $self,$class;
}

sub dump{
	my $self = shift;
	
	print Data::Dumper->Dump([$self]);
	
	return;
}

sub build_cmd{
	my $self = shift;
	my $tool
	my $cmd = $self->{};
	
	return;
}

1;
