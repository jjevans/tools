#!/usr/bin/env sh

cat $1 | vcf_valid_form.pl > $1.valid.vcf
