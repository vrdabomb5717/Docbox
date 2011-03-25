#!/usr/bin/perl

# genstat.pm
# Contains methods for accessing user SQLite database
# Authors: Varun
# 17th March 2011

#Note: First argument in a static method call in perl is always the class name. This is what $self refers to. 

## Still to DO:
# * Create tables for each file, creating word counts

package Genstat;

use strict;
use warnings;
use DBI;

my $dbfile = ".user.db";

my $dbh = DBI->connect( "dbi:SQLite:$dbfile", "", "",
	{RaiseError => 1, AutoCommit => 1}) || die "Cannot connect: $DBI::errstr";


#takes filepath, filename, whether the uploaded file is public, comments, and tags, and adds it to the database.
#if the file is already in the database, it attempts to update the record.
sub addFile()
{
	my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	
	my ($permissions, $timemodified, $timeadded, $filesize, $kind);
	
	#	Chart:
	#	$dev         - the file system device number
	#	$ino         - inode number
	#	$mode     - mode of file
	#	$nlink     - counts number of links to file
	#	$uid         - the ID of the file's owner
	#	$gid         - the group ID of the file's owner
	#	$rdev       - the device identifier
	#	$size        - file size in bytes
	#	$atime     - last access time
	#	$mtime    - last modification time
	#	$ctime     - last change of the mode
	#	$blksize  - block size of file
	#	$blocks    - number of blocks in a file
	
	my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat($filepath);
	
	$filesize = $size;
	$timeadded = localtime;
	$timemodified = $mtime;
	
	#getting permissions; $mode is in octal
	$permissions = sprintf("%o", $mode & 07777);
	
	#extracts filetype from the filename	
	my @suffix = split('\.', $filename);
	my $length = scalar(@suffix);
	
	if($length > 0)
	{
		$kind = "txt"
	}
	else
	{
		$kind = $suffix[$length - 1];
	}
	
	# INSERT INTO userpass (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
	my $insert = "INSERT OR REPLACE INTO files (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)";
	my $sth = $dbh->prepare("$insert");
	$sth->execute("$filepath", "$filename", "$public", "$permissions", "$timemodified", "$timeadded", "$size", "$kind", "$comments", "$tags");

	
	my $create = "CREATE TABLE $filepath (id INTEGER PRIMARY KEY, word TEXT NOT NULL COLLATE NOCASE, count INTEGER NOT NULL, UNIQUE(word))";
	my $cth = $dbh->prepare("$create");
	$cth->execute();


	$insert = "INSERT INTO :1 (word, count) VALUES (:2, :3)";
	$sth = $dbh->prepare("$insert");

	if(-T "$filepath")
	{
	    my $words = `"cat $filepath | perl -ne 'print join("\n", split(/\\W+/, $_))' | sort | uniq -c | sort -nr"`;
	    my @splitted = split(/'\n'/, $words);

	    foreach my $line(@splitted)
	    {
		my @counts = split($line);
		$sth->execute($filepath, $counts[1], $counts[0]);
	    }

	}
	else
	{
	    my $words = `strings $filepath | perl -ne 'print join("\n", split(/\\W+/, $_))' | sort | uniq -c | sort -nr`;
            my @splitted = split(/'\n'/, $words);

            foreach my $line(@splitted)
            {
		my @counts = split($line);
                $sth->execute($filepath, $counts[1], $counts[0]);
            }

	}

}

#removes a file given a filepath and filename, just to be doubly sure
sub removeFile
{
	my ($self, $filepath, $filename) = @_;
	my $delete = "DELETE FROM files WHERE filepath = :1 AND filename = :2";
	
	my $sth = $dbh->prepare("$delete");
	$sth->execute("$filepath", "$filename");
	
	my $drop = "DROP TABLE :1";
	$sth = $dbh->prepare("$drop");
	$sth->execute($filepath);
}

#returns reference to a hash that contains each row, with the id used as the hash's key
sub get_public
{
    #SELECT * FROM files WHERE public != 0
    my $public = "SELECT * FROM files WHERE public != 0";
    my $sth = $dbh->prepare("$public");
    $sth->execute();

    return $sth->fetchall_hashref('id');
}

sub average_size
{
    #SELECT AVG(size) FROM files
    my $average = "SELECT AVG(size) FROM files";
    my $sth = $dbh->prepare("$average");
    
    #not sure if the execute is needed
    $sth->execute();

    my @row_array = $sth->fetchrow_array;
    return $row_array[0];
}

sub num_files
{
    #SELECT COUNT(filename) FROM files
    my $count= "SELECT COUNT(filename) FROM files";
    my $sth = $dbh->prepare("$count");

    #not sure if the execute is needed
    $sth->execute();

    my @row_array = $sth->fetchrow_array;
    return $row_array[0];
}

sub search_filenames
{
    my ($self, $query) = @_;

    #SELECT * FROM files WHERE filenames LIKE '$query'

    my $search = "SELECT * FROM files WHERE tags LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub search_kind
{
    my ($self, $query) = @_;

    #SELECT * FROM files WHERE kind LIKE '$query'
                                                                                                                                                                                                                            
    my $search = "SELECT * FROM files WHERE kind LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub search_comments
{
    my ($self, $query) = @_;

    #SELECT * FROM files WHERE comments LIKE '$query'
                                                                                                                                                                                                                    
    my $search = "SELECT * FROM files WHERE comments LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub search_tags
{
    my ($self, $query) = @_;

    #SELECT * FROM files WHERE tags LIKE '$query'
    my $search = "SELECT * FROM files WHERE tags LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub top30
{
    my ($self, $filepath) = @_;

    my $select = "SELECT * FROM :1 LIMIT 30 ORDER BY count DESC";
    my $sth = $dbh->prepare($select);
    $sth->execute($filepath);
    return $sth->fetchall_hashref('id');
}

1;
