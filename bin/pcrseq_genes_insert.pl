#!/usr/bin/env perl
use strict;
use DBI;
use DBD::Oracle;

##jje16, msl34 01152015
#partners personalized medicine
#insert new gene names in pcrseq_genes table (gpadprod)
#path to M_DBIinfo.pm in /udd/genome/sequence/lib
my $doit = 0;#do not insert/update by default


##insert statement
my $sql_insert = "insert into pcrseq_genes_trial3 (gene_name,organism,chromosome,collaborator,gene_description,accession,project,note) values (?,'Human','null','null','null','null','null','null')";


##usage
my $usage = "usage: pcrseq_genes_insert.pl genes_1col.lst serviceid:user:passwd(GPADPROD:chr12:raju) execute_true_execute(optional,any value)\n";

die $usage unless @ARGV > 1;
my $lst = $ARGV[0];#list of gene names
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
my $sth_insert = $dbh->prepare($sql_insert);


##insert genes
open(my $fh,$lst) || die "ERROR: cannot open input list file: ".$lst."\n";
while(<$fh>){
	chomp;
	$sth_insert->execute(($_)) || warn $DBI::errstr;
}
close($fh);


##commit or no
if($doit){$dbh->commit()}
else{$dbh->rollback()}


$dbh->disconnect();

exit;
