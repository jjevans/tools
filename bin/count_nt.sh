
find . -name '*.fa' -exec cat {} \; | fasta2tbl.pl | perl -Mstrict -ne 'chomp;my($id,$seq)=split(/\t/,$_);  my $nn=$seq=~s/([Nn])/\1/g;my $cc=$seq=~s/([Cc])/\1/g;my $aa=$seq=~s/([Aa])/\1/g;my $gg=$seq=~s/([Gg])/\1/g;my $tt=$seq=~s/([Tt])/\1/g;print $id."\t".$aa."\t".$tt."\t".$cc."\t".$gg."\t".$nn."\t".length($seq)."\n";'
