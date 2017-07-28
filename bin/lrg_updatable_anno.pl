#!/usr/bin/env perl
use strict;

# from LRG xml from stdin, output only the xml from 
# updatable annotation section (from open tag to end tag)

my $tag_open = "<updatable_annotation>";
my $tag_close = "</updatable_annotation>";

my $print_on = 0;

while(<>){
	
	if(/$tag_open/){#encountered open tag
		$print_on = 1;
	}
	
	if($print_on){#print the section
		print;
	}
	
	if(/$tag_close/){#encountered the closing tag
		$print_on = 0;
	}

}

exit;
