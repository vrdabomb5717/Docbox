#!/usr/bin/perl

# Search
# Performs a search to which files match given query  
# Authors: Jervis
# March 26, 2011

### Currently Incomplete. Methods still need to be fully implemented. ###

# Still to Do:
# * Add a hidden form that will be used to maintain user state.  

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 
use PublicDB;  # use public file database


my $q = CGI->new();
my $uid = $q->param('uid'); # user id (token) of current user.
$uid = $q->url_param('uid') if (!defined($uid)); # for when we have mixed post/get data

my $query = $q->param('query');  # get user query.
my $search_type = $q->param('searchtype'); # Can either be 'Filenames' OR 'Documents' 
my $search_scope = $q->param('scope'); # Can either be 'Personal' OR 'Public'

my $valid = UserDB->validateUser($uid); # validate user correctly logged in, redirect to homepage otherwise. 
if($valid == 0){
	exit; # stop running of user is not logged in. 
}

my $user = UserDB->getUser($uid); # store current user
my $template = HTML::Template->new(filename => 'templates/search.tmpl');


if($search_type eq 'Filenames'){
	
	
	
} else{
	
	
		
}
