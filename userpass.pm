#!/usr/bin/perl

package Docbox;

use strict;
use warnings;
use DBI;

my $dbfile = "userpass.db";

my $dbh = DBI->connect( "dbi:SQLite:$dbfile", "", "",
		{RaiseError => 1, AutoCommit => 1}) || die "Cannot connect: $DBI::errstr";

#takes username and hashed password, and checks if they are within the userpass database
sub authenticate
{
	my ($username, $password) = @_;
	
	# SELECT * FROM userpass WHERE username='$user' AND pass='$password'
	my $sth = $dbh->prepare("SELECT * FROM userpass WHERE username=':1' AND pass=:'2'");
	$sth->execute("$username", "$password");
	
	if(defined($sth))
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

sub register
{
	my ($username, $password, $email, $firstname, $middlename, $lastname) = @_;
	
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
	
	# INSERT INTO userpass (username, password, email) VALUES ($username, $password, $email);
	my $insert = "INSERT INTO userpass (username, password, email) VALUES (:1, :2, :3)";
	my $sth = $dbh->prepare("$insert");
	$sth->execute("$username", "$password", "$email");
	
}

1;