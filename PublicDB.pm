#!/usr/bin/perl

# PublicDB
# Contains static methods for accessing Public file SQLite database
# Authors: Jervis
# 26th March 2011

#Note: First argument in a static method call in perl is always the class name. This is what $self refers to. 

## Still to DO:
# * Determine User given user id token.  

package PublicDB;

use strict;
use warnings;
use DBI;
use HTML;
#use diagnostics; # Outputs detailed error msgs

my $dbfile = "public.db";

my $dbh = DBI->connect( "dbi:SQLite:$dbfile", "", "",
	{RaiseError => 1, AutoCommit => 1}) || HTML->Error("connect to DB", "$dbfile - $DBI::errstr");


#takes filepath, filename, whether the uploaded file is public, comments, and tags, and adds it to the database.
#if the file is already in the database, it attempts to update the record.
sub addFile()
{
	my ($self, $filepath, $filename, $owner, $comments, $tags,  $timemodified, $timeadded, $size, $kind) = @_;
	
	# INSERT INTO files (filepath, filename, owner, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
	my $insert = "INSERT OR REPLACE INTO files (filepath, filename, owner, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)";
	my $sth = $dbh->prepare("$insert");
	$sth->execute("$filepath", "$filename", "$owner", "$timemodified", "$timeadded", "$size", "$kind", "$comments", "$tags");

	
}


#removes a file given a filepath and filename, just to be doubly sure
sub removeFile
{
	
	my ($self, $filepath, $filename) = @_;
	 
	my $delete = "DELETE FROM files WHERE filepath = :1 AND filename = :2";
	
	my $sth = $dbh->prepare("$delete");
	$sth->execute("$filepath", "$filename");
}


# returns the owner of the given file path.  
sub getOwner{ 
	
	my ($self, $filepath) = @_;
	
	# SELECT * FROM userpass WHERE password='$passwordhex'
	my $query = "SELECT owner FROM files WHERE filepath=:1";
	
	my $sth = $dbh->prepare("$query");
	$sth->execute("$filepath");

	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	my $href = $sth->fetchrow_hashref;
	
	if(defined($href))
	{
		return $href->{owner}; #need to use deference operator '->' since we've a hash ref 
	}
	else
	{
		return undef; # there is no file with that path 
	}
}



1;
