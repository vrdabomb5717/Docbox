#!/usr/bin/perl

# Upload Page
# Generates HTML to let user upload file to the server.  
# February 26, 2011
# Author: Jervis

### Test Upload Page ###

## Still to do 
# * still need to add user id when calling upload.pl.cgi script.
# * Need to do User authentication.  
BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use CGI qw/:all/;
use UserDB; 
use HTML;
use HTML::Template; # for creating html from template files.
my $q = CGI->new(); # cgi object


my $template = HTML::Template->new(filename => 'templates/upload.tmpl');

my $uid = $q->param('uid');
UserDB->validateUser($uid); # Check if valid user logged in. 
my $user = UserDB->getUser($uid);


$template->param(userid => $uid);
$q->print(header); # Print HTTP header
print $template->output();
 
#start();
#&uploadForm();
#print &end_html;

sub start{
	print header;
	print start_html(-Title=>"Upload Your File", -BGCOLOR=>'orange');
	print h1('Upload File');
	#HTML->start('Upload File'); 
	#HTMl->h1('Upload a File');
}

sub publicOption{
	print <<EOF;
<select name=public>
                <option>No</option>
                <option>Yes</option>
                </select>

EOF

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