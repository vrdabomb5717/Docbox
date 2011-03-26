#!/usr/bin/perl

# Login
# Authenticates user and directs them to home page
# Authors: Jervis and Varun. 
# February 26, 2011

### Still To Do 
# Need to use SQLite DB. 
# Currently reads password.txt
# Post User ID in a hidden form field

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1
use UserDB; 

my $user; # username
my $passhex; # encrpted password. This is a hash of username concatenated with password w/o spaces. 
my $uid;
my $q = CGI->new(); # get new CGI object for parsing input data

&getlogin(); # get user & pass

if(validlogin()){
	logLogin();
	redirectHome(); # go to home.pl.cgi
}
else{
	logFailedLogin();
	redirectLogin(); # go to login_failed.html
}

# Logs failed login attempt
sub logFailedLogin{
	open (FILE, ">>Logs/logins.txt"); # Open file for appending. Note this will create the file if it does not exist already. 
	my $ip = $ENV{'REMOTE_ADDR'};
	
	flock(FILE, LOCK_EX); # get file lock handle  
	{ 
		print (FILE "$user login attempt failed from IP address $ip \n"); #Append to login file	
	}
	close FILE; # save changes	
}



# Logs successful login attempt
sub logLogin{
	open (FILE, ">>Logs/logins.txt"); # Open file for appending. Note this will create the file if it does not exist already. 
	my $ip = $ENV{'REMOTE_ADDR'};
	
	flock(FILE, LOCK_EX); # get file lock handle  
	{ 
		print (FILE "$user logged in successfully from IP address $ip \n"); #Append to login file	
	}
	
	close FILE; # save changes	
}

sub redirectLogin{ # go to failed login page
#Space above EOF (i.e. new-line) is Necessary for the Apache webserver to follow redirect.
	print <<EOF;
Status: 302 Moved Temporarily
Location: login_failed.html
Content-type: text/html

EOF
}

sub redirectHome{ # go to homepage
	$uid = "$user = $passhex";
	$uid = sha1_hex($uid);
	
	print <<EOF;
Status: 302 Moved Temporarily
Location: home.pl.cgi?uid=$passhex
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

sub getlogin{ # get login from POST/GET data and do the necessary hashing. 
	$user = $q->param('username'); # get username
	my $pass = $q->param('password'); # get cleartext password
	$passhex = sha1_hex($user.$pass); # encrypt password. This is a hash of username concatenated with password w/o spaces.
}



sub validlogin{ # Validate login using SQL database.  
	 
	my $login = UserDB->authenticate($user,$passhex);
	return $login;
}

sub validLoginFile{ # Validate login by using password file. Deprecated
	
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

		
	
		


