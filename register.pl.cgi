#!/usr/bin/perl

# Register.pl.cgi
# Registers new user and adds to the database. 
# Currently uses a simple password.txt flat file db
# February 26, 2011

### Still TO DO
# * Validate user input; if invalid, stop registration
# * Handle case when user tries to double register or chooses a username, that's already taken.
# * Create new directory for new User. 

## Input data will be via POST

use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML; # generate docbox specific HTML
use userDB; # connects to user Database

my $q = CGI->new();

my $user = $q->param('username'); #username
my $pass = $q->param('password'); #password
my $email = $q->param('email'); #email
my $firstname = $q->param('firstname'); #first name
my $lastname = $q->param('lastname'); #last name


# Password hash will be hash of username concatenated with cleartext password without any spaces
# NB: This will also be used as the user ID and passed around as user browses site.  
my $passhex = sha1_hex("$user"."$pass"); # encrypt  password

if($ENV{REQUEST_METHOD} eq 'POST'){
	&register(); # register user
	&gotoLogin(); # return to login page	
}
else {
	HTML->start('Register Page');
	&register_form();
	HTML->end(); 
}



# Generates Register HTML Form
sub register_form{
	print <<EOF;
<h1> DocBox Account Registration </h1>
<h2>Please fill out the information below to register your account</h2>

<p> After you register, you will be automatically redirected back to the login page</p>
<form action = "register.pl.cgi" method="POST">
First Name: <input type="text" name="firstname">
<br>
Last Name: <input type="text" name="lastname">
<br>
Username: <input type="text" name="username">
<br>
Email: <input type="text" name="email">
<br>
Password: <input type="password" name="password">
<input type="submit" value="Register">
EOF
}


# Registers User to UserDB SQLite database
sub register{
	
	#Arguments for UserDB Registers are as follows: 
	# $username, $password, $email, $firstname, $middlename, $lastname
	UserDB->register($user,$passhex,$email,$firstname,"",$lastname);
	
	`mkdir ./files/$user`;
	
	`sqlite3 ./files/$user/user.db "CREATE TABLE files ( id INTEGER PRIMARY KEY,
                        filepath TEXT NOT NULL COLLATE NOCASE,
                        filename TEXT NOT NULL,
                        public INTEGER NOT NULL,
                        permissions INTEGER NOT NULL,
                        timemodified TEXT NOT NULL,
                        timeadded TEXT NOT NULL,
                        size REAL NOT NULL,
                        kind TEXT NOT NULL COLLATE NOCASE,
                        comments TEXT COLLATE NOCASE,
                        tags TEXT COLLATE NOCASE,
                        UNIQUE (filepath) );"`;
}


# Registers User to password file. 
# Deprecated. 
sub registertofile{ # add user login data to passwords.txt file
	
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