#!/usr/bin/perl

# Edit File
# Manipulates A File for the user. 
# Can Copy, Delete, Rename and Download
# Authors: Jervis
# March 16, 2011

### Currently Incomplete. Methods still need to be fully implemented. ###

use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 

my $user; # store current user
my $uid; # user id (token) of current user. 

my $q = CGI->new();
my $template = HTML::Template->new(filename => 'templates/editfile.tmpl');


my $uid = $q->param('uid'); # because uid is passed over query string.
$uid = $q->url_param('uid') if(!defined($uid)); # for when uid is in post data and we're have mixed post/get.
UserDB->validateUser($uid); # Check if valid user logged in. Redirect to login page otherwise.

my $filename = $q->param('filename');
$filename = $q->url_param('filename') if(!defined($filename));# for when uid is in post data and we're have mixed post/get.


 sub delete{
 	
 }
 
 
 sub rename{
 	
 }

sub copy{
	
}


