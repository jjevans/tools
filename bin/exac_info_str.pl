#!/usr/bin/env perl
use strict;

#from a set of INFO field ids (1col file) pull out 
# values and pair all fields for each variant
#ex.	input INFO: FLD0=0,0,0;FLD1=0,0.8,1;FLD2=1,2,3
#		output INFO: STR0=0|0|1;STR1=0|0.8|2;STR2=0|1|3
		