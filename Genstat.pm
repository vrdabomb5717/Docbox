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
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1
use PublicDB;

my $dbh; #declare db handle.  

#takes filepath, filename, whether the uploaded file is public, comments, and tags, and adds it to the database.
#if the file is already in the database, it attempts to update the record.
sub addFile()
{
	my ($self, $dbfile, $filepath, $filename, $public, $comments, $tags) = @_;
	
	Genstat->connect($dbfile); #connect to specific user db
	
	#HTML->Error("READ Comment: ", $comments);
	  
	my $fph = getTableHash($filepath); # File path hash
	if(!defined($comments)){
		$comments = ""; 
	}
	if(!defined($tags)){
		$tags = "";
	}
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
	
	if(-T "$filepath") # if file is a text file
	{
		$kind = "txt";
	}
	else
	{
		$kind = $suffix[$length - 1]; #use extension to determine type. 
	}
	
	# INSERT INTO userpass (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
	my $insert = "INSERT OR REPLACE INTO files (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)";
	my $sth = $dbh->prepare("$insert");
	$sth->execute("$filepath", "$filename", "$public", "$permissions", "$timemodified", "$timeadded", "$size", "$kind", "$comments", "$tags");

	
	## Insert into Public DB if file is Public
	# Argments are formt: $filepath, $filename, $owner, $comments, $tags,  $timemodified, $timeadded, $size, $kind) = @_;
	my @l = split(/\//, $dbfile);
	my $username = $l[1]; # get username 
	PublicDB->addFile($filepath, $filename, $username, $comments, $tags, $timemodified, $timeadded, $size, $kind);
	 
	my $table_exists = Genstat->existsTable($fph);
	
	if($table_exists){ # if table already exists, DELETE it first
		my $drop = "DROP TABLE $fph";
		$sth = $dbh->prepare("$drop");
		$sth->execute();
	} 
	
	my $create = "CREATE TABLE $fph (id INTEGER PRIMARY KEY, word TEXT NOT NULL COLLATE NOCASE, count INTEGER NOT NULL, UNIQUE(word))";
	my $cth = $dbh->prepare("$create");
	$cth->execute();


	$insert = "INSERT INTO $fph (word, count) VALUES (:2, :3)";
	$sth = $dbh->prepare("$insert");

	if(-T "$filepath")
	{
		 
		my @splitted = getWordCountText($filepath);
	    foreach my $line(@splitted)
	    {
			my @counts = split(' ', $line); # List has format: aWord itsCount
			$sth->execute($counts[0], $counts[1]);
	    }

	}
	else
	{
	    my $text = `strings $filepath`;  
        my @splitted = getWordCount($text); 

        foreach my $line(@splitted)
        {
			my @counts = split(' ', $line);
            $sth->execute($counts[0], $counts[1]);
        }
	}
}

## Checks if given table name already exists
# Internal method only 
sub existsTable{
	#my($self, $dbfile, $tn) = @_; # tn is table name
	#Genstat->connect($dbfile);
	
	my($self, $tn) = @_; # tn is table name
	 
	
	my $query ="SELECT name FROM sqlite_master WHERE type='table' AND name=:1"; 
	
	my $sth = $dbh->prepare("$query");
	$sth->execute($tn);
	
	
	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	# Since the table name is unique , we can use this to
	# check if that table already exists in database or not.
	 
	my $result = $sth->fetchrow_hashref; 
	
	if(defined($result))
	{
		return 1; # table exists
	}
	else
	{
		return 0;
	}
}

# Connects to user database
# Internal Method - should not be used publicly
sub connect{
	my ($self, $dbfile) = @_; 

	$dbh = DBI->connect( "dbi:SQLite:$dbfile", "", "",
	{RaiseError => 1, AutoCommit => 1}) || die HTML->Error("connect to DB", "$dbfile - $DBI::errstr");
}


# Takes a string and Returns words in a sorted order list including word count like shown below. 
# List contains string of format: aWord itsCount
# Internal method - don't use publicly
sub getWordCount{
	
	my $input = $_[0]; 
	
	my @output; 
	my %word_list; #hash table to store words
	$input = lc($input); #convert to lowercase
	my @words = split(/\W+/, $input); # get all words
	foreach my $word (@words){
		$word_list{$word}++; # store word and increment count. 
	}
	
	my @sorted_list = sort{$word_list{$b} <=> $word_list{$a}} keys %word_list; #sort hash table on key value counts in descending order
	
	my $count; 
	foreach my $word(@sorted_list){
		$count = $word_list{$word}; # get word count 
		push(@output, "$word $count\n");
	}
	return @output;
}

# Takes a plain text file Returns words in a sorted order list including word count like shown below. 
# List contains string of format: aWord itsCount
# Internal method only
sub getWordCountText{
	
	my $filepath = $_[0];
	my %word_list; #hash table to store words
	my @output;
	open(FILE, "$filepath") || die HTML->Error("opening", $filepath);	 
	
	while( my $line = <FILE>){
		chomp($line);
		$line = lc($line); #convert to lowercase
		my @words = split(/\W+/, $line); # get all words in line
		foreach my $word (@words){
			if($word eq ''){ # don't add empty strings 
				next; 
			}
			$word_list{$word}++; # store word and increment count. 
		}	
	}
	
	my @sorted_list = sort{$word_list{$b} <=> $word_list{$a}} keys %word_list; #sort hash table on key value counts in descending order
	
	my $count; 
	foreach my $word(@sorted_list){
		$count = $word_list{$word}; # get word count 
		push(@output, "$word $count\n");
	}
	return @output;
}

# Returns SHA hash of file path given.
# This is to be used in naming the tables to be created when a user adds a new file. 
#NOTE: In generating the tablenames, I take the filepath hash and a pre-append the letter "a"
#This is to please DBI becasue it can't process table names starting with numbers.
# Also, this is an internal method - dont use publicly. 
sub getTableHash{ 
	my ($filepath) = @_;
	my $fph = sha1_hex($filepath); # File path hash : This will used as the name of the table.
	$fph = "a" . "$fph"; #append a letter to guranteee that first character is always a letter.
	return $fph; 
}

#removes a file given a filepath and filename, just to be doubly sure
sub removeFile
{
	
	my ($self, $dbfile, $filepath, $filename) = @_;
	
	Genstat->connect($dbfile); #connect to specific user db
	my $fph = getTableHash($filepath); # File path hash
	 
	my $delete = "DELETE FROM files WHERE filepath = :1 AND filename = :2";
	
	my $public_file = Genstat->isPublic($filepath);
	if($public_file){ 
		PublicDB->removeFile($filepath, $filename); # Remove from Public DB if public file.  
	} 
	
	my $sth = $dbh->prepare("$delete");
	$sth->execute("$filepath", "$filename");
	
	my $drop = "DROP TABLE $fph";
	$sth = $dbh->prepare("$drop");
	$sth->execute();
}

# Checks if a filename is public
# internal method only 
sub isPublic{
	#Genstat->connect("Files/user/.user.db");
	
	my ($self, $filepath) = @_;
	
	my $query ="SELECT * FROM files WHERE filepath=:1"; 
	
	my $sth = $dbh->prepare("$query");
	$sth->execute($filepath);
		
	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	 
	my $href = $sth->fetchrow_hashref; 
	
	if(defined($href))
	{
		return $href->{public}; #need to use deference operator '->' since we've a hash ref
	}
	else
	{
		return 0;
	}
	
	
}

#returns reference to a hash that contains each row, with the id used as the hash's key
sub get_public
{
    
    my ($self, $dbfile) = @_;
    Genstat->connect($dbfile); #connect to specific user db
  
    #SELECT * FROM files WHERE public != 0
    my $public = "SELECT * FROM files WHERE public != 0";
    my $sth = $dbh->prepare("$public");
    $sth->execute();

    return $sth->fetchall_hashref('id');
}

# Returns ID number of file, given full path
sub getFileID{
	
	my ($self, $dbfile, $filepath) = @_;
	
	Genstat->connect($dbfile); #connect to specific user db
	
	my $query ="SELECT * FROM files WHERE filepath=:1"; 
	
	my $sth = $dbh->prepare("$query");
	$sth->execute($filepath);
		
	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	 
	my $href = $sth->fetchrow_hashref; 
	
	if(defined($href))
	{
		return $href->{id}; #need to use deference operator '->' since we've a hash ref
	}
	else
	{
		return -1;
	}
}

sub average_size
{
    my ($self, $dbfile) = @_;
    Genstat->connect($dbfile); #connect to specific user db
    
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
    my ($self, $dbfile) = @_;
    Genstat->connect($dbfile); #connect to specific user db
    
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
    my ($self, $dbfile, $query) = @_;
    Genstat->connect($dbfile); #connect to specific user db
	
    #SELECT * FROM files WHERE filenames LIKE '$query'

    my $search = "SELECT * FROM files WHERE tags LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub search_kind
{
    my ($self, $dbfile, $query) = @_;
    Genstat->connect($dbfile); #connect to specific user db
    
    #SELECT * FROM files WHERE kind LIKE '$query'
                                                                                                                                                                                                                           
    my $search = "SELECT * FROM files WHERE kind LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub search_comments
{
    my ($self, $dbfile, $query) = @_;
    Genstat->connect($dbfile); #connect to specific user db
    #SELECT * FROM files WHERE comments LIKE '$query'
                                                                                                                                                                                                                    
    my $search = "SELECT * FROM files WHERE comments LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub search_tags
{
    my ($self, $dbfile, $query) = @_;
    Genstat->connect($dbfile); #connect to specific user db
    
    #SELECT * FROM files WHERE tags LIKE '$query'
    my $search = "SELECT * FROM files WHERE tags LIKE '%:1%";
    my $sth = $dbh->prepare($search);
    $sth->execute($query);
    return $sth->fetchall_hashref('id');
}

sub top30
{
    my ($self, $dbfile, $filepath) = @_;
    Genstat->connect($dbfile); #connect to specific user db
	my $fph = getTableHash($filepath); # File path hash
	
	#my $fph = sha1_hex($filepath); # File path hash
    #$fph = "a" . "$fph"; #append a letter to guranteee that first character is always a letter.
    
    #my $select = "SELECT * FROM $fph LIMIT 30 ORDER BY count DESC";
    my $select = "SELECT * FROM $fph ORDER BY count DESC LIMIT 30";
    my $sth = $dbh->prepare($select);
    #$sth = $dbh->prepare("ORDER BY count");
    $sth->execute();
    return $sth->fetchall_hashref('id');
}


# Returns full file path, given a file ID
sub getFilePathByID{
	
	my ($self, $dbfile, $id) = @_;
	Genstat->connect($dbfile); #connect to specific user db
	
	# SELECT * FROM files WHERE password='$passwordhex'
	my $query = "SELECT * FROM files WHERE id=:1";
	
	my $sth = $dbh->prepare("$query");
	$sth->execute("$id");

	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	my $href = $sth->fetchrow_hashref;
	
	if(defined($href))
	{
		return $href->{filepath}; #need to use deference operator '->' since we've a hash ref 
	}
	else
	{
		return undef; # there is no file with that path 
	}	
}

# Returns full file name, given a file ID
sub getFileNameByID{

	my ($self, $dbfile, $id) = @_;
	Genstat->connect($dbfile); #connect to specific user db
	
	# SELECT * FROM files WHERE password='$passwordhex'
	my $query = "SELECT * FROM files WHERE id=:1";
	
	my $sth = $dbh->prepare("$query");
	$sth->execute("$id");

	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	my $href = $sth->fetchrow_hashref;
	
	if(defined($href))
	{
		return $href->{filename}; #need to use deference operator '->' since we've a hash ref 
	}
	else
	{
		return undef; # there is no file with that path 
	}	
}


1;
