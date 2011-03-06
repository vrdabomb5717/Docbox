#!/usr/bin/perl

# Upload Page
# Generates HTML to let user upload file to the server.  
# February 26, 2011
# Author: Jervis

### Test Upload Page ###

## Still to do 
# * still need to add user id when calling upload.pl.cgi script.
# * Need to do User authentication.  

use strict;
use CGI qw/:all/;
use UserDB; 

my $q = CGI->new(); # cgi object


my $uid = $q->param('uid');
UserDB->validateUser($uid); # Check if valid user logged in. 
my $user = UserDB->getUser($uid);

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
	my $action = "upload.pl.cgi?uid=$uid";
	my $enc = &CGI::MULTIPART();
	
	print start_form($method,$action,$enc);
	print filefield('uploaded_file','starting value',50,80);
	#print hidden('uid',"$uid"); # Pass the uid in a hidden field.  
	print submit('Upload to Server');
	print end_form;
}
