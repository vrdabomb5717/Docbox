#!/usr/bin/perl

# Upload Page
# Generates HTML to let user upload file to the server.  
# February 26, 2011
# Author: Jervis

### Test Upload Page ###

##TBD - still need to add user id when calling upload.pl.cgi script. 

use strict;
use CGI qw/:all/;

my $q = CGI->new(); # cgi object


&start();
&uploadForm();
print &end_html;

sub start{
	print header;
	print start_html("Upload Your File");
	print h1('Upload File');
}

sub uploadForm{
	my $method = 'POST';
	my $action = 'upload.pl.cgi';
	my $enc = &CGI::MULTIPART();
	
	print start_form($method,$action,$enc);
	print filefield('uploaded_file','starting value',50,80);
	print submit('Upload to Server');
	print end_form;
}
