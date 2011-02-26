#!/usr/bin/perl

# Login
# Authenticates user and directs them to home page
# Authors: Jervis and Varun. 
# February 26, 2011

### TBD
# Need to use SQLite DB. 
# Currently reads password.txt


use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 

my $user; # username
my $passhex; # encrpted password
my $uid;
my $q = CGI->new(); # get new CGI object for parsing input data

&getlogin(); # get user & pass

if(validlogin()){
	redirectHome(); # go to home.pl.cgi
}
else{
	redirectLogin(); # go to login_failed.html
}


sub redirectLogin{ # go to failed login page
	
	print <<EOF;
Status: 302 Relocate status
Location: login_failed.html
Content-type: text/html
EOF
}

sub redirectHome{ # go to homepage
	$uid = "$user = $passhex";
	$uid = sha1_hex($uid);
	
	print <<EOF;
Status: 302 Relocate status
Location: home.pl.cgi?u=$passhex
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Login Successful</TITLE>
</HEAD>
<BODY>
<H1>Login Success !</h1>
<p> You will automatically be redirected soon to the home page. <a href= home.pl.cgi?uid=$uid>Click here</a> to manually go to the home page</p>
</BODY>
</HTML>

EOF
}

sub getlogin{ # get login from POST/GET data
	$user = $q->param('user'); # get username
	my $pass = $q->param('pass'); # get password
	$passhex = sha1_hex($pass); # encrypt password
	
	
}

sub validlogin{ # Validate login by using password file
	
	my $uid = "$user = " . $passhex; # get hashed user login

	my $successLogin = 0; #boolean value to indicate if login valid
	
	open (FILE, "passwords.txt") || die "Password File Not Found";# Open file for reading. Warn if file not found
	flock(FILE, LOCK_EX); # get file lock handle
	{
		while(my $login = <FILE>){ #check all logins saved in password file	
			if($login =~ m/^$uid/){
				$successLogin = 1;
				last; #exit loop
			}
		}
	}
	close FILE; #close file handle
	return $successLogin;
}

		
	
		


