#!/usr/bin/perl

# Home
# Home page for a user. 
# Lists all files currently owned by the user.
# Authors: Jervis and Varun
# February 26, 2011

use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 

my $q = CGI->new();

### Currently Incomplete. Methods still need to be fully implemented. ###


sub listFiles{ # Should Produce HTML output of user's current files
	
}

sub getUser{ # should return user name of currently logged in user. 
	my $uid = $q->param('uid'); # gets the UID being passed along. UID is a SHA1 hash of the string "Useranme = PasswordHEX"
	
	### TBD need to look up UID to get username
	
}


sub getFiles{ # should return list of Files belonging to user 
	
}
