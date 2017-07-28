#!/usr/bin/env perl
use strict;
use DBI;
use DBD::Oracle;

##jje16, msl34 01152015
#partners personalized medicine
#path to M_DBIinfo.pm in /udd/genome/sequence/lib
#update templates that already exist in 
# table pcrseq_templates
my $doit = 0;#do not insert/update by default
#my $db_tbl = "pcrseq_templates";
my $db_tbl = "pcrseq_templates_stage";

##update statement
my $sql_update = "update ".$db_tbl." set template_name=?,gene_name=?,exon_name=?,sequence=?,position=?,length=?,analysis_complete=?,serial_number=?,target_start=?,target_length=?,lmm_target_start=?,lmm_target_length=? where template_name=?";


##usage
my $usage = "usage: pcrseq_templates_update.pl templates.12col.tbl serviceid:user:passwd(GPADPROD:chr12:raju) execute_true_execute(optional,any value,default rollback)\n";

die $usage unless @ARGV > 1;
my $tbl = $ARGV[0];#table of exon data
my $cred = $ARGV[1];#service:user:pass
$doit = 1 if defined($ARGV[2]);#actually update/insert


##init db
#get credentials
my $ohome = $ENV{ORACLE_HOME};
my($sid,$user,$passwd) = split(":",$cred);
my $source = "dbi:Oracle:".$sid;

#connect
my %attr = (PrintError=>1,RaiseError=>1,AutoCommit=>0);
my $dbh = DBI->connect($source, $user, $passwd, \%attr);
my $sth_update = $dbh->prepare($sql_update);


##insert templates
open(my $fh,$tbl) || die "ERROR: cannot open input table file: ".$tbl."\n";
while(<$fh>){
	my @vals = split(/\t/,$_);
	chomp($vals[-1]);

	if(length($vals[3])> 10000){#no super long seq, not sure cutoff strlen
		warn "WARNING: ultra-long sequence skipped: ".$vals[0]."\n";
		next;
	}
	else{
		push(@vals,$vals[0]);#where template_name
		$sth_update->execute(@vals) || warn $DBI::errstr;
	}
}
close($fh);


if($doit){$dbh->commit()}
else{$dbh->rollback()}


$dbh->disconnect();

exit;
