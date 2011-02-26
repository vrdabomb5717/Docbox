#!/usr/bin/perl

# Register.pl.cgi
# Registers new user and adds to the database. 
# Currently uses a simple password.txt flat file db
# February 26, 2011

## Input data will be via POST and the keys will be 'user' and 'pass'

use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 

my $q = CGI->new();

my $user = $q->param('user'); #username
my $pass = $q->param('pass'); #password
my $passhex = sha1_hex($pass); # encrypted password

&register(); # register user
&gotoLogin(); # return to login page


# Registers User
# Currently uses a simple password file. 
sub register{ # add user login data to passwords.txt file
	
	open (FILE, ">>passwords.txt"); # Open file for appending. Note this will create the file if it does not exist already. 
	flock(FILE, LOCK_EX); # get file lock handle  
	{ 
		print (FILE "$user = $passhex \n"); #Append the password to text file	
	}
	
	close FILE; # save changes
}


sub gotoLogin{ # return to homepage
	
	print <<EOF;
Status: 302 Relocate status
Location: index.html
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Registration Complete</TITLE>
</HEAD>
<BODY>
<H1>Registeration Complete !</h1>
<p> You will automatically be redirected soon to the login page. <a href=index.html>Click here</a> to manually return to the home page</p>
</BODY>
</HTML>

EOF
} 