#!/usr/bin/perl

# Download.pl.cgi
# Downloads the given file to the user's browser. 
# Authors: Jervis
# March 19, 2011


## Still to DO:
# * add user checking of file name supplied. (taint mode ??)

use strict;
use CGI qw/:standard/; 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 

my $user; # store current user
my $uid; # user id (token) of current user. 

my $q = CGI->new();
#print $q->header(); # Print HTML Headers
#my $template = HTML::Template->new(filename => 'templates/editfile.tmpl');
#my $op_template = HTML::Template->new(filename => 'templates/fileop.tmpl'); # for making html for successful operation

$uid = $q->param('uid'); # because uid is passed over query string.
$uid = $q->url_param('uid') if(!defined($uid)); # for when uid is in post data and we're have mixed post/get.
UserDB->validateUser($uid); # Check if valid user logged in. Redirect to login page otherwise.

$user = UserDB->getUser($uid); # get username of current logged in user.

#get currently working directory path for the file. 
my $dirpath = $q->param('directorypath');  # dirpath shouldn't NOT containing trailling '/'

## Define source file path for current user. 
# Will need to add directory path, after enabling grouping funtionality. 
my $sourcefilepath = "files/$user/$dirpath" ; 

my $filename = $q->param('filename');
my $filepath = "$sourcefilepath/" . "$filename";

open(FH, $filepath) || die Error('open',$filepath); # opens file for reading. 
#my @file = <FH>;
#close FH; 
 
#switch both input and output handles to binary mode to ensure proper file transfer.
binmode STDOUT; 
binmode FH; 

## Download the file.
# The Headers below will force browse to show save as dialog rather than 
# showing/vieweing the file.  


#print "Content-Type:application/x-download\n";   
#print "Content-Disposition:attachment;filename=$filename\n\n";

print $q->header(-type            => 'application/x-download',
                 -attachment      => $filename,
                 'Content-length' => -s $filepath,
   				);

print while(<FH>); 
close FH;

#my $buffer;
#while(read(FH, $buffer, 1024)){ # serve file in 1K bits, otherwise download prompt will take time to appear. 
#	print $buffer;
#}


#print "Content-type: image/jpeg\n\n";
#print @file; 


sub Error{  
   print "Content-type: text/html\n\n";  
   print "The server can't $_[0] the $_[1]: $! \n";  
   exit;  
 }
