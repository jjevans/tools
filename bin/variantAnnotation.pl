#!/usr/bin/env perl

# $Id: vA_geisinger.pl 720 2015-05-29 04:09:07Z jje16 $

use strict;
use warnings;
use File::Basename;
use File::Spec;
use Getopt::Long;
use YAML::XS ("LoadFile");
use Data::Dumper;

my $inVcf;
my $configFile;

GetOptions( "input_vcf=s" => \$inVcf, "config=s" => \$configFile );

if(!defined($inVcf)){
	die "Usage: " . $0 . " --input_vcf genome.vcf (vcf/gvcf file with full path) --config (yaml formatted config file)\n";
}
if(!defined($configFile)){
	die "Please provide a configuration file.\n";
}

#filepaths
my $pathToCrudeVcf = File::Spec->rel2abs($inVcf);
my $crudeVcf = basename($pathToCrudeVcf);
my $path_to_accession = dirname($pathToCrudeVcf);
my $tmpFile = "vep.tmpfile.vcf";

#specific to geisinger project
#file extension for file having lsf job name for uploader script
# to be used by another external process
my $upldr_file_ext = "vcfloaderid.txt";

#random number to prepend to job names
my $job_range = 10000;
my $job_random_number = int(rand($job_range));

####
# assign runtime values from inputted configuration file
####
my $config = LoadFile($configFile);

##lsf
my $lsf_queue = $config->{"LSF"}{"queue"};
my $lsf_numproc = $config->{"LSF"}{"num_proc"};
my $lsf_memres = $config->{"LSF"}{"mem_res"};
my $lsf_memlim = $config->{"LSF"}{"mem_limit"};
my $lsf_email = join(",",@{$config->{"LSF"}{"email"}});	#array of people's email
$lsf_email =~ s/\@/\\\@/g;	#escape @
my $lsf_hg = $config->{"LSF"}{"host_group"};
my $lsf_alamut_jg = $config->{"LSF"}{"alamut_job_group"};
my $lsf_vcfupload_jg = $config->{"LSF"}{"vcfupload_job_group"};

##software
#vcf-sort (vcftools)
my $regions = $config->{"Tool"}{"vcf_sort"}{"region"};


##annotation sources
#vep
my $vepConfig = $config->{"Tool"}{"vep"}{"config"};#old version var name
my $vep_cache = $config->{"Tool"}{"vep"}{"cache"};
my $vep_plugin = join(",",@{$config->{"Tool"}{"vep"}{"plugin"}});
my $vep_version = &recurse_struct($config->{"Version"}{"vep"},"","");

#snpeff
my $snpeff_jar = $config->{"Tool"}{"snpeff"}{"software"};
my $snpeff_1000gen = $config->{"Tool"}{"snpeff"}{"1000genome"};
my $snpeff_clinvar = $config->{"Tool"}{"snpeff"}{"clinvar"};
my $snpeff_dbsnp = $config->{"Tool"}{"snpeff"}{"dbsnp"};
#my $snpeff_esp = $config->{"Tool"}{"snpeff"}{"esp"};
my $snpeff_exac = $config->{"Tool"}{"snpeff"}{"exac"};
my $snpeff_version = &recurse_struct($config->{"Version"}{"snpeff"},"","");

#hgmd
my $hgmd_version = &recurse_struct($config->{"Version"}{"hgmd"},"","");
my $hgmd_script = $config->{"Tool"}{"hgmd"}{"script"};

#alamut
my $alamut_ht = $config->{"Tool"}{"alamut"}{"software"};
#my $alamut_exec_in = $config->{"Tool"}{"alamut"}{"format_in"};
#my $alamut_exec_out = $config->{"Tool"}{"alamut"}{"format_out"};
my $alamut_lookup = $config->{"Tool"}{"alamut"}{"field"};
my $alamut_numproc = $config->{"Tool"}{"alamut"}{"num_proc"};
my $alamut_version = &recurse_struct($config->{"Version"}{"alamut"},"","");

##uploader
my $dbupload = $config->{"Tool"}{"uploader"}{"directory"};
my $uploader_host = $config->{"Database"}{"uploader"}{"host"};
my $uploader_port = $config->{"Database"}{"uploader"}{"port"};
my $uploader_service = $config->{"Database"}{"uploader"}{"service"};
my $uploader_user = $config->{"Database"}{"uploader"}{"username"};
my $uploader_password = $config->{"Database"}{"uploader"}{"password"};


##paths; java classpath, perl PERL5LIB, unix PATH
my $java_cp = join(",",@{$config->{"Path"}{"java"}});
my $perl_path = join(":",@{$config->{"Path"}{"perl"}});
my $unix_path = join(":",@{$config->{"Path"}{"unix"}});

####

my @crudeVcfName = split(/\./, $crudeVcf);
my $crudeVcfNameExt = $crudeVcfName[-1];

#determine if bgzipped or uncompressed vcf and set up appropriate 
# cat/zcat
my $cat;
if($crudeVcfName[-1] eq "gz"){
	pop(@crudeVcfName);#drop gz
	$cat = "z";
}
$cat .= "cat";


#situate filepaths
my $genome_accession;
my $genomeName;
my $sampleName;

if($crudeVcfName[-1] =~ /^[g]?vcf$/){
	$genome_accession = $crudeVcfName[0];
	## split the name
	my @genome_acc = split("_", $genome_accession);
	if($#genome_acc > 0) {
		$genomeName = $genome_acc[0];
		$sampleName = $genome_acc[1];
		$genome_accession = "${genomeName}_${sampleName}";
	} else {
		$genomeName = $genome_accession;
		$sampleName = $genome_accession;
	}
	
}
else {
	die "Input crude VCF file must have a '.vcf, .vcf.gz, .gvcf, .gvcf.gz' extension\n";
}

my $logDir = "$path_to_accession/log";	# directory for log files
my $lsfDir = "$path_to_accession/lsf";	# directory for lsf files
my $dbConfig = $path_to_accession . "/" . $genome_accession . ".properties";

system("mkdir -p $logDir");
system("mkdir -p $lsfDir");


#Populate lsf template files of the three annotation processes for a specified genome

#LSF Header and inputs common to all four lsf files
my $lsfHeaderLine1 = "#!/bin/bash\n#\n";

my $lsfQueue = "#BSUB -q ".$lsf_queue."\n";
my $node     = "#BSUB -n ".$lsf_numproc."\n";
my $memres   = "#BSUB -R \'rusage[mem=".$lsf_memres."]\'\n";
my $memlim   = "#BSUB -M ".$lsf_memlim."\n";
my $bsubOut  = "#BSUB -o ";
my $bsubErr  = "#BSUB -e ";
my $sendTo .= "#BSUB -u ".$lsf_email."\n";
my $emailFlag = "#BSUB -N\n";

my $lsfHg = "";
$lsfHg .= "#BSUB -m " . $lsf_hg . "\n" if defined($lsf_hg);

#LSF Header and inputs common to all four lsf files
my $lsf_common = $lsfQueue.$memres.$memlim.$sendTo.$emailFlag;
$lsf_common .=  $lsfHg;

#This is output of vcf-sort and input to all annotation tools
# inserts '.target' for copy of inputted file
my $rawSortedInputVcf = $crudeVcf;

#die if filename conversion doesn't work, avoid using same input filename
if($rawSortedInputVcf !~ s/\.[g]?vcf(\.gz)?$/.target\.vcf/i){
	my $message = "Filename conversion regex unsuccessful for creating input file copy (.target.vcf) for file: ".$crudeVcf."\n";
	die $message;
}


#full path to .target.vcf
$rawSortedInputVcf = $path_to_accession . "/" . $rawSortedInputVcf;


####### Create an lsf file for preprocessing a vcf file: an input to VEP, SNPEFF, HGMD, ALAMUT ##############################
my $prepTemplate = $lsfDir . "/PREP_" . $genome_accession . ".lsf";
my $submitJobID = $job_random_number . "_" . "PREP_" . $genome_accession;
my $outputDir = $path_to_accession;

open(my $submitAnnotFH, "> $prepTemplate") or die "Could not open $prepTemplate -$!";

print $submitAnnotFH $lsfHeaderLine1
  . $lsf_common
  . $node
  . "#BSUB -J $submitJobID\n"
  . $bsubOut . "$logDir/prepareAnnot_%J.out\n"
  . $bsubErr . "$logDir/prepareAnnot_%J.err\n";


my $submitAnnotHereDoc = <<WRAPPER;

export PATH=\$PATH:$unix_path

$cat $pathToCrudeVcf | extract_variants |  vcf_from_gvcf.pl | vcftools --vcf - --bed $regions --stdout --recode-INFO-all --recode | vcf-sort > $rawSortedInputVcf

WRAPPER

print $submitAnnotFH $submitAnnotHereDoc;


###########VEP - Creating and populating lsf file for VEP ###################################

my $vepTemplate = $lsfDir . "/VEP_" . $genome_accession . ".lsf";
my $vepJobID = $job_random_number . "_" . "VEP_" . $genome_accession;
my $vepOut    = $path_to_accession . "/" . $genome_accession . ".annot.vep.vcf";

open(my $vepTemplateFH, "> $vepTemplate") or die "Could not open $vepTemplate -$!";

print $vepTemplateFH $lsfHeaderLine1
  . $lsf_common
  . $node
  . "#BSUB -J " . $vepJobID . "\n"
  . $bsubOut . "$logDir/vep_%J.out\n"
  . $bsubErr . "$logDir/vep_%J.err\n"
  . "#BSUB -w \'done($submitJobID)\'\n";

#VEP -config $vepConfig --input $rawSortedInputVcf --out  $vepOut --force_overwrite --plugin $vep_plugin --cache --dir $vep_cache

my $submitVepHereDoc = <<VAREP;

export PATH=\$PATH:$unix_path
export PERL5LIB=\$PERL5LIB:$perl_path

cat $rawSortedInputVcf | vcf_sub_ref.pl > $tmpFile

variant_effect_predictor.pl -config  $vepConfig  --input  $tmpFile --out  $vepOut  --force_overwrite --plugin $vep_plugin --cache --dir $vep_cache

#cat $vepOut | vcf_sub_nonref.pl > $tmpFile
#mv $tmpFile $vepOut

sed -i s\/\"\#CHROM\"\/\"\#\#ANNOTATION_VERSION_LOG=\\"$vep_version\\"\\n#CHROM\"\/g $vepOut


NUM_IN=\`grep -vc \"\^\#\" $rawSortedInputVcf\`
NUM_OUT=\`grep -vc \"\^\#\" $vepOut\`

if [ \"\$NUM_IN\" -ne \"\$NUM_OUT\" ]; then
    echo ERROR: VEP did not have the same number of variants in output as did its input.
    exit 100
fi


VAREP

print $vepTemplateFH $submitVepHereDoc;



##################SNPEFF - Creating and populating lsf file for SnpEff ##################################

my $snpEffTemplate = $lsfDir . "/SNPEFF_" . $genome_accession . ".lsf";
my $snpEffJobID = $job_random_number . "_" . "SNPEFF_" . $genome_accession;
my $snpEffOut = $path_to_accession . "/" . $genome_accession . ".annot.snpeff.vcf";

open(my $snpEffTemplateFH, "> $snpEffTemplate") or die "Could not open $snpEffTemplate -$!";

print $snpEffTemplateFH $lsfHeaderLine1
  . $lsf_common
  . $node
  . "#BSUB -J $snpEffJobID\n"
  . $bsubOut . "$logDir/snpeff_%J.out\n"
  . $bsubErr . "$logDir/snpeff_%J.err\n"
  . "#BSUB -w \'done($submitJobID)\'\n";

#substituted ExAC vcf for ESP vcf below, 07132015, jje16
my $submitSnpEffHereDoc = <<SNPEFF;

java -Xmx4g -jar $snpeff_jar annotate $snpeff_1000gen \\
$rawSortedInputVcf \\
| java -Xmx4g -jar $snpeff_jar annotate $snpeff_clinvar - \\
| java -Xmx4g -jar $snpeff_jar annotate $snpeff_dbsnp - \\
| java -Xmx4g -jar $snpeff_jar annotate $snpeff_exac - \\
> $snpEffOut

sed -i s\/\"\#CHROM\"\/\"\#\#ANNOTATION_VERSION_LOG=\\"$snpeff_version\\"\\n#CHROM\"\/g $snpEffOut


NUM_IN=\`grep -vc \"\^\#\" $rawSortedInputVcf\`
NUM_OUT=\`grep -vc \"\^\#\" $snpEffOut\`

if [ \"\$NUM_IN\" -ne \"\$NUM_OUT\" ]; then
    echo ERROR: snpEff did not have the same number of variants in output as did its input.
    exit 100
fi


SNPEFF

print $snpEffTemplateFH $submitSnpEffHereDoc;


##################HGMD - Creating and populating lsf file for HGMD ##################################

my $hgmdTemplate = $lsfDir . "/HGMD_" . $genome_accession . ".lsf";
my $hgmdJobID = $job_random_number . "_" . "HGMD_" . $genome_accession;
my $hgmdOut = $path_to_accession . "/" . $genome_accession . ".annot.hgmd.vcf";

open(my $hgmdTemplateFH, "> $hgmdTemplate") or die "Could not open $hgmdTemplate -$!";

print $hgmdTemplateFH $lsfHeaderLine1
  . $lsf_common
  . $node
  . "#BSUB -J $hgmdJobID\n"
  . $bsubOut . "$logDir/hgmd_%J.out\n"
  . $bsubErr . "$logDir/hgmd_%J.err\n"
  . "#BSUB -w \'done($submitJobID)\'\n";

my $submitHgmdHereDoc = <<HUGMD;

export PATH=\$PATH:$unix_path

$hgmd_script $rawSortedInputVcf $hgmdOut $configFile

sed -i s\/\"\#CHROM\"\/\"\#\#ANNOTATION_VERSION_LOG=\\"$hgmd_version\\"\\n#CHROM\"\/g $hgmdOut

HUGMD

print $hgmdTemplateFH $submitHgmdHereDoc;

################## ALAMUT - Creating and populating lsf file for ALAMUT #######################################################
#NOTE: turning on gene splicer causes multiple threads to be generated that crash the job
my $alamuTemplate = $lsfDir . "/ALAMUT_" . $genome_accession . ".lsf";
my $alamutJobID = $job_random_number . "_" . "ALAMUT_" . $genome_accession;
my $formatAlamutOut = $genome_accession . ".annot.ala_input_vcf";
my $alaAnnotFile = $genome_accession . ".annot.ala_ann";
my $alaUnannLog = $genome_accession . ".annot.ala_unann";
my $alamutOut = $path_to_accession . "/" . $genome_accession . ".annot.ala.vcf";

open(my $alamuTemplateFH, "> $alamuTemplate") or die "Could not open $alamuTemplate -$!";

print $alamuTemplateFH $lsfHeaderLine1
  . $lsf_common
  . "#BSUB -n " . $alamut_numproc . "\n"
  . "#BSUB -J $alamutJobID\n"
  . $bsubOut . "$logDir/alamut_%J.out\n"
  . $bsubErr . "$logDir/alamut_%J.err\n"
  . "#BSUB -w \'done($submitJobID)\'\n";

print $alamuTemplateFH "#BSUB -g ".$lsf_alamut_jg."\n" if defined($lsf_alamut_jg);

my $submitAlamutHereDoc = <<ALAMUT;

set -e

export PATH=$unix_path:\$PATH

#convert raw vcf to alamut-ht friendly vcf
cat $rawSortedInputVcf | vcf_from_gvcf.pl 0 | vcf_wide_to_tall.pl | vcf_ala_id.pl > $formatAlamutOut

#call alamut-ht
$alamut_ht --in $path_to_accession/$formatAlamutOut --ann $path_to_accession/$alaAnnotFile --unann $path_to_accession/$alaUnannLog --nogenesplicer --processes $alamut_numproc --alltrans --nonnsplice --nomispred --outputannonly

#parse output to vcf for uploader
parse_alamut_fieldbyname_v2.pl $path_to_accession/$alaAnnotFile $alamut_lookup | vcf-sort -c > $alamutOut


#add version string
sed -i s\/\"\#CHROM\"\/\"\#\#ANNOTATION_VERSION_LOG=\\"$alamut_version\\"\\n#CHROM\"\/g $alamutOut

rm $path_to_accession/$formatAlamutOut
rm $path_to_accession/$alaUnannLog
rm $path_to_accession/$alaAnnotFile

ALAMUT

print $alamuTemplateFH $submitAlamutHereDoc;


############# Create db config file #############################################################

my $jdbc_url = "jdbc:oracle:thin:\@".$uploader_host.":".$uploader_port."/".$uploader_service;

open(my $dbconfigFH, "> $dbConfig") or die "Could not open $dbConfig -$!";

my $dbConfigHereDoc = <<DBUPLOAD;

jdbcUrl=$jdbc_url
jdbcUsername=$uploader_user
jdbcPassword=$uploader_password

vepVcfFile=$vepOut
snpEffVcfFile=$snpEffOut
alamutVcfFile=$alamutOut
hgmdVcfFile=$hgmdOut

genomeName=$genomeName
sampleName=$sampleName

DBUPLOAD

print $dbconfigFH $dbConfigHereDoc;

####### Create an lsf file for vcf-uploader ##############################
my $uploaderTemplate = $lsfDir . "/VCFUPLOADER_" . $genome_accession . ".lsf";
my $uploaderJobID = "#BSUB -J " . $job_random_number . "_vcf_load_" . $genome_accession . "\n";

open(my $uploaderTemplateFH, "> $uploaderTemplate") or die "Could not open $uploaderTemplate -$!";

print $uploaderTemplateFH $lsfHeaderLine1
  . $lsf_common
  . $node
  . $uploaderJobID
  . $bsubOut . "$logDir/vcfUploader_%J.out\n"
  . $bsubErr . "$logDir/vcfUploader_%J.err\n"
  . "#BSUB -w \'done($snpEffJobID) && done($alamutJobID) && done($hgmdJobID) && done($vepJobID)\'\n";

print $uploaderTemplateFH "#BSUB -g ".$lsf_vcfupload_jg."\n" if defined($lsf_vcfupload_jg);

my $submitUploaderHereDoc = <<UPLOADER;
set -e

echo Time started: \$\(date +\%Y-\%m-\%d" "\%H:\%M:\%S\)
echo "Uploading genomes and variants to database"

$dbupload/run.sh $dbConfig

echo Time completed: \$\(date +\%Y-\%m-\%d" "\%H:\%M:\%S\)

UPLOADER

print $uploaderTemplateFH $submitUploaderHereDoc;


######################### End - creating vcf loader lsf file ########################
# actually submit the bsub jobs

system("bsub<$prepTemplate >> $logDir/bsub.log");
system("bsub<$alamuTemplate >> $logDir/bsub.log");
system("bsub<$hgmdTemplate >> $logDir/bsub.log");
system("bsub<$snpEffTemplate >> $logDir/bsub.log");
system("bsub<$vepTemplate >> $logDir/bsub.log");
sleep(5);
#system("bsub<$uploaderTemplate >> $logDir/bsub.log");
sleep(5);

#print uploader job id for file for caller script to pick up - filtration job will follow this
##make file to indicate lsf job name for uploader job
my $upldr_file = $path_to_accession . "/" . $genome_accession . "." . $upldr_file_ext;
open(my $upldr_fh,">".$upldr_file) || die "Cannot open file to print uploader jobid ".$upldr_file." at ".$0."\n";
print $upldr_fh $uploaderJobID;
close($upldr_fh);

# we are done.

exit;

sub recurse_struct{
	#jje, 03112014
	#create versioning string
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
