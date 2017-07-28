#!/usr/bin/env perl
use strict;

#remove all hidden non-printed unicode chars

while(<>){
	s/[^!-~\s]//g;
	print;
}

exit;

