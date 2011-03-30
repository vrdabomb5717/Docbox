#!/usr/bin/perl

# genstat.pm
# Contains methods for accessing user SQLite database
# Authors: Varun and Jervis
# 17th March 2011

#Note: First argument in a static method call in perl is always the class name. This is what $self refers to. 

## Still to DO:
# * Make sure RTF support works, and that renaming files works as planned.

package Genstat;

use strict;
use warnings;
use DBI;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1
use PublicDB;
use Text::Extract::Word;
use RTF::TEXT::Converter;

my $dbh; #declare db handle.  

#takes filepath, filename, whether the uploaded file is public, comments, and tags, and adds it to the database.
#if the file is already in the database, it attempts to update the record.
sub addFile
{
	my ($self, $dbfile, $filepath, $filename, $public, $comments, $tags) = @_;
	
	Genstat->connect($dbfile); #connect to specific user db
	
	#HTML->Error("READ Comment: ", $comments);
	  
	my $fph = getTableHash($filepath); # File path hash
	
	if(!defined($comments))
	{
		$comments = ""; 
	}
	
	if(!defined($tags))
	{
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
	my $length = int(@suffix);
	
	if(-T "$filepath") # if file is a text file
	{
		$kind = "txt";
	}
	else
	{
		#use extension to determine type
		$kind = $suffix[$length - 1];
		$kind = lc($kind);
	}
	
	# INSERT INTO userpass (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
	my $insert = "INSERT OR REPLACE INTO files (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)";
	my $sth = $dbh->prepare("$insert");
	$sth->execute("$filepath", "$filename", "$public", "$permissions", "$timemodified", "$timeadded", "$size", "$kind", "$comments", "$tags");

	
	## Insert into Public DB if file is Public
	my $public_file = Genstat->isPublic($filepath);
	if($public_file == 1)
	{
		# Argments are form: $filepath, $filename, $owner, $comments, $tags,  $timemodified, $timeadded, $size, $kind) = @_;
		my @l = split(/\//, $dbfile);
		my $username = $l[1]; # get username 
		PublicDB->addFile($filepath, $filename, $username, $comments, $tags, $timemodified, $timeadded, $size, $kind);
	}
	
	# if table already exists, DELETE it first
	my $drop = "DROP TABLE IF EXISTS $fph";
	$sth = $dbh->prepare("$drop");
	$sth->execute();
	
	my $create = "CREATE TABLE $fph (id INTEGER PRIMARY KEY, word TEXT NOT NULL COLLATE NOCASE, count INTEGER NOT NULL, UNIQUE(word))";
	my $cth = $dbh->prepare("$create");
	$cth->execute();


	$insert = "INSERT INTO $fph (word, count) VALUES (:2, :3)";
	$sth = $dbh->prepare("$insert");

	if(-T "$filepath" )  
	{
		 
		my @splitted = getWordCountText($filepath);
	    foreach my $line(@splitted)
	    {
			# List has format: aWord itsCount
			my @counts = split(' ', $line);
			$sth->execute($counts[0], $counts[1]);
	    }

	}
	elsif($kind eq "pdf")
	{
		my $text = `pdftotext -q "$filepath" -`;  
        my @splitted = getWordCount($text); 

        foreach my $line(@splitted)
        {
			my @counts = split(' ', $line);
            $sth->execute($counts[0], $counts[1]);
        }
	}
	elsif($kind eq "doc")
	{
		my $doc = Text::Extract::Word->new("$filepath");
		my $text = $doc->get_text();
		
		my @splitted = getWordCount($text); 

        foreach my $line(@splitted)
        {
			my @counts = split(' ', $line);
            $sth->execute($counts[0], $counts[1]);
        }
	}
	elsif($kind eq "rtf")
	{
		#open RTF file and read data into $text
		my $text = "";
		open(my $fh, "$filepath");
		my $object = RTF::TEXT::Converter->new(output => \$text);
		$object->parse_stream(\$fh);
		
		my @splitted = getWordCount($text); 

        foreach my $line(@splitted)
        {
			my @counts = split(' ', $line);
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
sub existsTable
{
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
sub connect
{
	my ($self, $dbfile) = @_; 

	$dbh = DBI->connect( "dbi:SQLite:$dbfile", "", "",
	{RaiseError => 1, AutoCommit => 1}) || die HTML->Error("connect to DB", "$dbfile - $DBI::errstr");
}


# Takes a string and Returns words in a sorted order list including word count like shown below. 
# List contains string of format: aWord itsCount
# Internal method - don't use publicly
sub getWordCount
{
	my $input = $_[0]; 
	
	my @output; 
	my %word_list; #hash table to store words
	$input = lc($input); #convert to lowercase
	my @words = split(/\W+/, $input); # get all words
	
	foreach my $word (@words)
	{
		$word_list{$word}++; # store word and increment count. 
	}
	
	my @sorted_list = sort{$word_list{$b} <=> $word_list{$a}} keys %word_list; #sort hash table on key value counts in descending order
	
	my $count;
	
	foreach my $word(@sorted_list)
	{
		$count = $word_list{$word}; # get word count 
		push(@output, "$word $count\n");
	}
	
	return @output;
}

# Takes a plain text file and returns words in a sorted order list including word count like shown below. 
# List contains string of format: aWord itsCount
# Internal method only
sub getWordCountText
{
	
	my $filepath = $_[0];
	my %word_list; #hash table to store words
	my @output;
	open(FILE, "$filepath") || die HTML->Error("opening", $filepath);	 
	
	while( my $line = <FILE>)
	{
		chomp($line);
		$line = lc($line); #convert to lowercase
		my @words = split(/\W+/, $line); # get all words in line
		foreach my $word (@words)
		{
			if($word eq '')
			{ # don't add empty strings 
				next; 
			}
			
			$word_list{$word}++; # store word and increment count. 
		}	
	}
	
	my @sorted_list = sort{$word_list{$b} <=> $word_list{$a}} keys %word_list; #sort hash table on key value counts in descending order
	
	my $count;
	
	foreach my $word(@sorted_list)
	{
		$count = $word_list{$word}; # get word count 
		push(@output, "$word $count\n");
	}
	
	return @output;
}

# Returns SHA1 hash of file path given.
# This is to be used in naming the tables to be created when a user adds a new file. 
#NOTE: In generating the tablenames, I take the filepath hash and a pre-append the letter "a"
#This is to please DBI becasue it can't process table names starting with numbers.
# Also, this is an internal method - dont use publicly. 
sub getTableHash
{ 
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
	if($public_file == 1)
	{ 
		PublicDB->removeFile($filepath, $filename); # Remove from Public DB if public file.  
	} 
	
	my $sth = $dbh->prepare("$delete");
	$sth->execute("$filepath", "$filename");
	
	my $drop = "DROP TABLE IF EXISTS $fph";
	$sth = $dbh->prepare("$drop");
	$sth->execute();
}

#updates a filename given a filepath, filename, a new filepath, and the new filename.
sub updateFile
{
	my ($self, $dbfile, $oldpath, $oldname, $newpath, $newname) = @_;
	
	Genstat->connect($dbfile); #connect to specific user db
	my $fph = getTableHash($oldpath); # File path hash
	my $nph = getTableHash($newpath); #new path hash
	 
	#because we cannot update a unique key directly, we must first do a select, capture the file's data, 
	#delete the old file, and insert the new one
	my $select = "SELECT * FROM files WHERE filepath = :1";
	my $sth = $dbh->prepare("$select");
	
	$sth->execute($oldpath);
		
	# Retrieve hash reference to result from running query.
	# This will be defined if the query returned more than 0 results.
	 
	my $href = $sth->fetchrow_hashref; 
	
	if(defined($href))
	{
		#need to use deference operator '->' since we've a hash ref
		my $public = $href->{public};
		my $permissions = $href->{permissions};
		my $timemodified = time();
		my $timeadded = $href->{timeadded};
		my $size = $href->{size};
		my $kind = $href->{kind};
		my $comments = $href->{comments};
		my $tags = $href->{tags};
		
		my $delete = "DELETE FROM files WHERE filepath = :1 AND filename = :2";
		$sth = $dbh->prepare("$delete");
		$sth->execute("$oldpath", "$oldname");


		# INSERT INTO userpass (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) 
		#VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
		my $insert = "INSERT OR REPLACE INTO files (filepath, filename, public, permissions, timemodified, timeadded, size, kind, comments, tags) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)";
		$sth = $dbh->prepare("$insert");
		$sth->execute("$newpath", "$newname", "$public", "$permissions", "$timemodified", "$timeadded", "$size", "$kind", "$comments", "$tags");

		#use the new filepath to check if the file is public because the update has already happened.
		my $public_file = Genstat->isPublic($newpath);
		if($public_file == 1)
		{ 
			# Update Public DB if public file is renamed.
			#PublicDB->updateFile($oldpath, $oldname, $newpath, $newname);
			
			my @l = split(/\//, $dbfile);
			my $owner = $l[1]; # get username
			
			PublicDB->removeFile($oldpath, $oldname);
			PublicDB->addFile($newpath, $newname, $owner, $comments, $tags,  $timemodified, $timeadded, $size, $kind);
		} 

		#print "fph is $fph\n";
		my $alter = "ALTER TABLE $fph RENAME TO $nph";
		$sth = $dbh->prepare("$alter");
		$sth->execute();
		
	}
	else
	{
		return -1;
	}
}



# Checks if a filename is public. Return 1 if public, and 0 if private.
# internal method only 
sub isPublic
{
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

# modifies a private file to make it public and adds it to the public db
sub makePublic
{
	my ($self, $dbfile, $filepath) = @_;
	my $public = isPublic($self, $filepath);
	
	
	#if file is private, add it to public db. Otherwise, do nothing.
	if($public == 0)
	{
		my $update = "UPDATE files SET public=1, timemodified = :1 WHERE filepath = :2";
		my $sth = $dbh->prepare("$update");
		my $timemodified = time();
		$sth->execute($timemodified, $filepath);
		
		#capture the file's data so we can add it to the public db
		my $select = "SELECT * FROM files WHERE filepath = :1";
		$sth = $dbh->prepare("$select");

		$sth->execute($filepath);

		# Retrieve hash reference to result from running query.
		# This will be defined if the query returned more than 0 results.

		my $href = $sth->fetchrow_hashref; 

		if(defined($href))
		{
			#need to use deference operator '->' since we've a hash ref
			my $filename = $href->{filename};
			my $timeadded = $href->{timeadded};
			my $size = $href->{size};
			my $kind = $href->{kind};
			my $comments = $href->{comments};
			my $tags = $href->{tags};
			
			my @l = split(/\//, $dbfile);
			my $owner = $l[1]; # get username
			
			PublicDB->addFile($filepath, $filename, $owner, $comments, $tags,  $timemodified, $timeadded, $size, $kind);
			
		}
		
	}
}

# modifies a public file to make it private and removes it from the public db
sub makePrivate
{
	my ($self, $dbfile, $filepath) = @_;
	my $public = isPublic($self, $filepath);
	
	#if file is public, remove it from public db. Otherwise, do nothing.
	if($public == 1)
	{
		my $update = "UPDATE files SET public=0, timemodified = :1 WHERE filepath = :2";
		my $sth = $dbh->prepare("$update");
		my $timemodified = time();
		$sth->execute($timemodified, $filepath);
		
		#get filename so we can remove file from public db
		my $select = "SELECT * FROM files WHERE filepath = :1";
		$sth = $dbh->prepare("$select");

		$sth->execute($filepath);

		# Retrieve hash reference to result from running query.
		# This will be defined if the query returned more than 0 results.

		my $href = $sth->fetchrow_hashref; 

		if(defined($href))
		{
			#need to use deference operator '->' since we've a hash ref
			my $filename = $href->{filename};
			PublicDB->removeFile($filepath, $filename);
		}
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

# Takes a Full File Path AND  
# Returns Hashref with full file recrod details
sub getFileRecord
{
	
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
		return $href; #return a hash reference to record details. 
	}
	else
	{
		return -1;
	}
}



# Returns ID number of file, given full path
sub getFileID
{
	
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

#### Implemented in Filesearch.pm. This is just dead code for initial plans to search database instead.
## Do a Document deep search of all Files in User's folder for given string...
## Should Return a Hashref to Filename. 
sub doc_search{
    my ($self, $dbfile, $query) = @_;
    Genstat->connect($dbfile); #connect to specific user db
	return;
}

#returns the average size of the user's files
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

#returns the number of files in the user's database
sub num_files
{
    my ($self, $dbfile) = @_;
    Genstat->connect($dbfile); #connect to specific user db
    
    #SELECT COUNT(filename) FROM files
    my $count= "SELECT COUNT(filename) FROM files";
    my $sth = $dbh->prepare("$count");

    $sth->execute(); # execute query, (this call is needed)

    my @row_array = $sth->fetchrow_array;
    return $row_array[0];
}

#use the user's database to search filenames for a specific query
sub search_filenames
{
    my ($self, $dbfile, $query) = @_;
    Genstat->connect($dbfile); #connect to specific user db
	
    #SELECT * FROM files WHERE filenames LIKE '$query'

    my $search = "SELECT * FROM files WHERE filename LIKE \'%$query%\' ORDER BY filename";
    my $sth = $dbh->prepare($search);
    $sth->execute();
    #return $sth->fetchall_hashref('id');
    return $sth->fetchall_arrayref([1,2,5,6,7,0]); # return filepath, filename, time modified, time added, size, file ID
}

#use the user's database to search file types for a specific query (e.g. search for all "pdf" files)
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

#use the user's database to search comments for a specific query
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

#use the user's database to search tags for a specific query
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

#use the user's database to return the top 30 most occurring words for a specific file
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
    return $sth->fetchall_arrayref([1,2]); # return word and count columns only
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
sub getFileNameByID
{
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
