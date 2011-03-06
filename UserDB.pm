#!/usr/bin/perl

# UserDB
# Contains static methods for accessing UserPass SQLite database
# Authors: Jervis and Varun
# 3rd March 2011

#Note: First argument in a static method call in perl is always the class name. This is what $self refers to. 

## Still to DO:
# * Determine User given user id token.  

package UserDB;

use strict;
use warnings;
use DBI;
#use diagnostics; # Outputs detailed error msgs

my $dbfile = "userpass.db";

my $dbh = DBI->connect( "dbi:SQLite:$dbfile", "", "",
	{RaiseError => 1, AutoCommit => 1}) || die "Cannot connect: $DBI::errstr";

#takes username and hashed password, and checks if they are within the userpass database
sub authenticate
{
	my ($self, $username, $password) = @_;
	
	# SELECT * FROM userpass WHERE username='$user' AND password='$password'
	my $sth = $dbh->prepare("SELECT * FROM userpass WHERE username=:1 AND password=:2");
	$sth->execute("$username", "$password");

	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	# Since the user and password combo we're searching is unique, can use this to
	# validate if user exists in database or not.
	 
	my $result = $sth->fetchrow_hashref; 
	
	if(defined($result))
	{
		return 1; # successful authentication
	}
	else
	{
		return 0;
	}
}

# returns username whose has the given user id token.
# Still to be implemented. 
sub getUser{ 
	
	my ($self, $passwordhex) = @_;
	
	# SELECT * FROM userpass WHERE password='$passwordhex'
	my $sth = $dbh->prepare("SELECT * FROM userpass WHERE password=:1");
	$sth->execute("$passwordhex");

	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	my $href = $sth->fetchrow_hashref;
	
	if(defined($href))
	{
		return $href->{username}; #need to use deference operator '->' since we've a hash ref 
	}
	else
	{
		return undef; # there is no user with that id. 
	}
}

sub register
{
	
	my ($self, $username, $password, $email, $firstname, $middlename, $lastname) = @_; 
		
	if(!defined($firstname) )
	{
		$firstname = "NULL";
	}
	
	if (!defined($middlename))
	{
		$middlename = "NULL";
	}
	
	if(!defined($lastname))
	{
		$lastname = "NULL";
	}
	
	# INSERT INTO userpass (username, password, email) VALUES ($username, $password, $email, $firstname, $middlename, $lastname);
	my $insert = "INSERT INTO userpass (username, password, email, firstname, middlename, lastname) VALUES (:1, :2, :3, :4, :5, :6)";
	my $sth = $dbh->prepare("$insert");
	$sth->execute("$username", "$password", "$email", "$firstname", "$middlename", "$lastname");	
}


1;