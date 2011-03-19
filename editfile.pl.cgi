#!/usr/bin/perl

# Edit File
# Manipulates A File for the user. 
# Can Copy, Delete, Rename and Download
# Authors: Jervis
# March 16, 2011

### Still To DO  ###
## * Add Safety checking to user input. e.g. user gives same filename for copy opertaion etc
## * Add Full FIle PAths so that ops will work inside directories

use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 
use File::Copy; # provides functionality to copy and rename files

my $user; # store current user
my $uid; # user id (token) of current user. 

my $q = CGI->new();
print $q->header(); # Print HTML Headers
my $template = HTML::Template->new(filename => 'templates/editfile.tmpl');
my $op_template = HTML::Template->new(filename => 'templates/fileop.tmpl'); # for making html for successful operation

$uid = $q->param('uid'); # because uid is passed over query string.
$uid = $q->url_param('uid') if(!defined($uid)); # for when uid is in post data and we're have mixed post/get.
UserDB->validateUser($uid); # Check if valid user logged in. Redirect to login page otherwise.

$user = UserDB->getUser($uid); # get username of current logged in user. 

my $filename = $q->param('filename');
$filename = $q->url_param('filename') if(!defined($filename));# for when filename is in post data and we're have mixed post/get.

## Save Filename and user id in hidden form field to preserve user state
$template->param(userid => $uid); 
$template->param(filename => $filename);

my $renamedfilename = $q->param('renamedfile'); # comes thru post 
my $copyfilename = $q->param('copyfilename'); # comes thru post

my $prevlink; # stores link back to directory/file listing
my $prevlink_form = $q->param('prevlink'); #  

if(!defined($prevlink_form)){
	$prevlink = $ENV{'HTTP_REFERER'}; # get previous page's link	
}else{
	$prevlink = $prevlink_form;
}
 
$template->param(prevlink => $prevlink); # write link to return to previous page.
$op_template->param(prevlink => $prevlink);

my $badinput; 
### Check for Bad User Input
if ( $renamedfilename eq '' && $copyfilename eq ''){ # if both fields empty
	$badinput = 1;
}
elsif($renamedfilename ne '' && $copyfilename ne ''){ # if both field defined
	$badinput = 1;
} elsif($copyfilename eq $filename || $renamedfilename eq $filename){ # copy/rename filename is same as actual copy of file. 
	$badinput = 1;
}



# special case for when, user first visits editfile page. In that case, 
# copyfilename & renamedfile nameare undefs.
if(!defined($copyfilename) || !defined($renamedfilename)){ 
	$badinput = 0; 
}

if($badinput){ ## Stop if bad input
	$template->param(badinput => 1);
	print $template->output();
	exit;
}


if($renamedfilename){ # if renmaedfilename field specified
	my_rename($renamedfilename); 
}

if($copyfilename){ # if copyfilename field specified
	#my_copy($renamedfilename);
	my $sourcefilepath = "files/$user/";
	
	my $source = "$sourcefilepath" . "$filename"; 
	my $dest = "$sourcefilepath" . "$copyfilename";
	
	copy($source, $dest);
	$op_template->param(operation => 'Copy');
	print $op_template->output();
	exit;
}


# print the template
print $template->output;




 sub my_delete{
 	
 }
 
 
 sub my_rename{
 	return; 
 }

sub my_copy{
	return;
}


