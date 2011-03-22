#!/usr/bin/perl

# Reset.pl.cgi
# Resets the password of a user.  
# Authors: Jervis
# March 21, 2011

use strict;
use CGI qw/:standard/; 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files.
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1

my $q = CGI->new();
print $q->header(); # Print HTTP Header
 
my $uid = $q->param('uid'); # get user id. (Comes in thru POST)
UserDB->validateUser($uid); # checks if user valid. otherwise redirectts to homepage

my $user = UserDB->getUser($uid);
my $email = UserDB->getEmail($uid);
my $newpass = $q->param('password');# new plain text password from user
my $passhex = sha1_hex("$user"."$newpass"); # encrypt  password
my $template = HTML::Template->new(filename => 'templates/success.tmpl');


$template->param(passwordreset => 1); # toggle successful reset page. 

# change password takes the following arguments:
# $username, $email, $newpass. 
UserDB->change_password($user,$email,$passhex); # change user password. 

print $template->output(); 