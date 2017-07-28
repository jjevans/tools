use strict;

###simple logger lib
# jje16, msl34 01302014
#DERIVES FROM PDP LOGGING LIB (pdp_log.pm)

package biofx_log;
sub new{ 
	# accepts a log filename (file) or default "run.log"
	my($class,$atts) = @_;
	
	my $self = {
		file => $atts->{file} || "run.log",
		log_fh => *STDERR,
		to_stderr => 1
	};
	
	my $message = ":::WARNING---++ cannot open file for logging: ".$self->{"file"}." ...logging to STDERR\n";
	open(my $log_fh,">>$self->{'file'}") || print STDERR $message;
	
	#log file opened successful
	$self->{"log_fh"} = $log_fh if -w $log_fh;
	
	return bless $self,$class;
}

sub log_it{#log to file and return
	#all messages communicated through this subroutine
	#arg is a message
	my $self = shift;
	my $message = $_[0];
	
	print {$self->{"log_fh"}} $message;
	print STDERR $message if $self->{"log_fh"} ne *STDERR && $self->{"to_stderr"};
	
	return;
}

sub log_error{#error, log and die
	#arg is a message
	my $self = shift;
	my $message = $_[0];	
	
	my $full = ":::ERROR--- ".$0.": ".$message;
	$self->log_it($full);
	
	close($self->{"log_fh"}) if $self->{"log_fh"} ne *STDERR;
	die "!!!CRASH---: exiting.\n";
}
			
sub log_success{#success, log and return
	#args are filehandle and message
	my $self = shift;
	my $message = $_[0];
	
	my $full = ":::SUCCESS::: ".$0.": ".$message;
	$self->log_it($full);
	
	return;
}

sub log_init{
	#create logger, log begin of process 
	#return logger filehandle, if can't open fh, returns *STDERR
	#no args
	my $self = shift;

	my $message = "===INIT===: ".$0."\t".localtime()."\n";
	$self->log_it($message);

	return ;
}

sub log_done{#log end of process, close logger filehandle
	#no args
	my $self = shift;
	
	my $message = "====DONE====: ".$0."\t".localtime()."\n";
	$self->log_it($message);

	close($self->{"log_fh"}) if $self->{"log_fh"} ne *STDERR;
	
	return;
}

1;
