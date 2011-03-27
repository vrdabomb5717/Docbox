#!/usr/bin/perl

# Search
# Performs a search to which files match given query  
# Authors: Jervis
# March 26, 2011

### Currently Incomplete. Methods still need to be fully implemented. ###

# Still to Do:
# * Add a hidden form that will be used to maintain user state.  

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 
use PublicDB;  # use public file database
use Genstat; 

my $q = CGI->new();
my $uid = $q->param('uid'); # user id (token) of current user.
$uid = $q->url_param('uid') if (!defined($uid)); # for when we have mixed post/get data

my $query = $q->param('query');  # get user query.
my $search_type = $q->param('searchtype'); # Can either be 'Filenames' OR 'Documents' 
my $search_scope = $q->param('scope'); # Can either be 'Personal' OR 'Public'

my $valid = UserDB->validateUser($uid); # validate user correctly logged in, redirect to homepage otherwise. 
if($valid == 0){
	exit; # stop running of user is not logged in. 
}

my $user = UserDB->getUser($uid); # store current user
my $template = HTML::Template->new(filename => 'templates/search.tmpl');


# Fill user's name and unique id in template:
my $name = UserDB->getName($uid); 
$template->param(user => $name);
$template->param(userid => $uid);

## Check if user visiting us for first time
if($ENV{'REQUEST_METHOD'} ne 'POST'){
	$template->param(results => 0); # Don't Show Search Results
	print $q->header(); 
	print $template->output();
	exit; # Exit script
}
else {
	$template->param(results => 1); # Show Search Results
	search(); #run search
	print $q->header(); 
	print $template->output();
	exit; # Exit script
}





sub search {
	my $fp; # file path
	my $fn;  # file name
	my $tm; # time modified
	my $size; # size in bytes
	my @list; # file lsit data will go here 
	my @abbr = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ); # for date modified
	
	if($search_type eq 'Filenames'){
		if($search_scope eq 'Personal'){ ## Search Personal Files
			my $dbfile = "Files/$user/.user.db"; # set path to user db file
			my $hash_ref_all = Genstat->search_filenames($dbfile, $query); # get (double) hash ref to query results. Arguments are:  $dbfile, $query		
			
			## HTML Format the search results in a table
			while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){ 
				 
				$fn = $row_hash_ref->{'filename'};
				$fp = $row_hash_ref->{'filepath'};
				$size = $row_hash_ref->{'size'};
				$tm = $row_hash_ref->{'timemodified'};
						
				 
				## Get FilePath ID
				my $fid = $row_hash_ref->{'id'};
				 
				## Get dir subdirectory
				my $offset = length("Files/$user/");
				my $dir = substr($fp,$offset );
				my @l = split(/\//, $dir); # check to see if there is at least one sub-directory 
				if(int(@l)<2){ # if no directories, reset dir (this is shown by fact the splited string had less than two elements)
					$dir = '';
				}
				
				 
				#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
		        #$atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
		    	
		    	my ($sec,$min,$hour,$mday,$mon,$year) = localtime($tm); # get detailled time info 
			    $year += 1900; #get proper year, since we start from 1900. 
			    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
				
				#convert size to kilobytes to 2 decimal places:
				$size =  $size/1024;
				$size = sprintf("%.2f", $size); # round to 2 dps. 
				
				# set query string for view statistics script. 
				my $querystring = "stats.pl.cgi\?uid=$uid\&fid=$fid";
				
				# set query string for download script
				my $downloadquery = "download.pl.cgi\?uid=$uid\&filename=$fn" . "\&directorypath=$dir";
				
				
				my %row = (
						filename => $fn,
						date => $mtime,
						size => $size,
						querystring => $querystring,
						download_query => $downloadquery
						);
			
			 	push(@list, \%row);
			}	 
				 
		 	# call param to fill in the loop with the loop data by reference.
			$template->param(list_loop => \@list);	
			
		}
		else { ## Search Filenames in Public Files
			
			my $dbfile = "Files/$user/.user.db"; # set path to user db file
			my $hash_ref_all = PublicDB->search_filenames($query); # get (double) hash ref to query results. Arguments are:  $query
				
			my $fp; # file path
			my $fn;  # file name
			my $tm; # time modified
			my $size; # size in bytes
			
			while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){
				
				#print $row_hash_ref;
				# Row hash ref has following keys: filepath, filename, owner, timemodified, size, kind, comments, tags
				 
				$fp = $row_hash_ref->{'filepath'};
				$fn = $row_hash_ref->{'filename'}; 
				$tm = $row_hash_ref->{'timemodified'};
				$size = $row_hash_ref->{'size'};
				 
				## Get FilePath ID
				my $fid = $row_hash_ref->{'id'};
		
				#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
		        #$atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
		    	
		    	my ($sec,$min,$hour,$mday,$mon,$year) = localtime($tm); # get detailled time info 
			    $year += 1900; #get proper year, since we start from 1900. 
			    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
				
				#convert size to kilobytes to 2 decimal places:
				$size =  $size/1024;
				$size = sprintf("%.2f", $size); # round to 2 dps. 
				
				# set query string for view statistics script.  
				my $querystring = "stats.pl.cgi\?uid=$uid\&fid=$fid\&public=1";
				
				# set query string for download script
				my $downloadquery = "download.pl.cgi\?uid=$uid\&public=1" . "\&fid=$fid"; # Don't specify a directory path
				
				my %row = (
						filename => $fn,
						date => $mtime,
						size => $size,
						querystring => $querystring,
						download_query => $downloadquery
						);
			
			 	push(@list, \%row);
			}	 
				 
		 	# call param to fill in the loop with the loop data by reference.
			$template->param(list_loop => \@list);
			
		}
		
	} else{ ## Do Deep Level Document Search ###### UNTESTED CODE ########
		
		HTML->Error("Complete Operation", " -- Code for Deep Level Search is Incomplete"); ## Don't Run the code below YET
		exit;
		
		if($search_scope eq 'Personal'){ ## Search in Personal Files
			my $dbfile = "Files/$user/.user.db"; # set path to user db file
			my $hash_ref_all = Genstat->doc_search($dbfile, $query); # get (double) hash ref to query results. Arguments are:  $dbfile, $query		
			
			## HTML Format the search results in a table
			while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){ 
				 
				$fn = $row_hash_ref->{'filename'};
				$fp = $row_hash_ref->{'filepath'};
				$size = $row_hash_ref->{'size'};
				$tm = $row_hash_ref->{'timemodified'};
						
				 
				## Get FilePath ID
				my $fid = $row_hash_ref->{'id'};
				 
				## Get dir subdirectory
				my $offset = length("Files/$user/");
				my $dir = substr($fp,$offset );
				my @l = split(/\//, $dir); # check to see if there is at least one sub-directory 
				if(int(@l)<2){ # if no directories, reset dir (this is shown by fact the splited string had less than two elements)
					$dir = '';
				}
				
				 
				#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
		        #$atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
		    	
		    	my ($sec,$min,$hour,$mday,$mon,$year) = localtime($tm); # get detailled time info 
			    $year += 1900; #get proper year, since we start from 1900. 
			    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
				
				#convert size to kilobytes to 2 decimal places:
				$size =  $size/1024;
				$size = sprintf("%.2f", $size); # round to 2 dps. 
				
				# set query string for view statistics script. 
				my $querystring = "stats.pl.cgi\?uid=$uid\&fid=$fid";
				
				# set query string for download script
				my $downloadquery = "download.pl.cgi\?uid=$uid\&filename=$fn" . "\&directorypath=$dir";
				
				
				my %row = (
						filename => $fn,
						date => $mtime,
						size => $size,
						querystring => $querystring,
						download_query => $downloadquery
						);
			
			 	push(@list, \%row);
			}	 
				 
		 	# call param to fill in the loop with the loop data by reference.
			$template->param(list_loop => \@list);	
			
		}
		else { ## Search  in Public Files
			
			my $dbfile = "Files/$user/.user.db"; # set path to user db file
			my $hash_ref_all = PublicDB->doc_search($query); # get (double) hash ref to query results. Arguments are:  $query
				
			my $fp; # file path
			my $fn;  # file name
			my $tm; # time modified
			my $size; # size in bytes
			
			while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){
				
				#print $row_hash_ref;
				# Row hash ref has following keys: filepath, filename, owner, timemodified, size, kind, comments, tags
				 
				$fp = $row_hash_ref->{'filepath'};
				$fn = $row_hash_ref->{'filename'}; 
				$tm = $row_hash_ref->{'timemodified'};
				$size = $row_hash_ref->{'size'};
				 
				## Get FilePath ID
				my $fid = $row_hash_ref->{'id'};
		
				#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
		        #$atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
		    	
		    	my ($sec,$min,$hour,$mday,$mon,$year) = localtime($tm); # get detailled time info 
			    $year += 1900; #get proper year, since we start from 1900. 
			    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
				
				#convert size to kilobytes to 2 decimal places:
				$size =  $size/1024;
				$size = sprintf("%.2f", $size); # round to 2 dps. 
				
				# set query string for view statistics script.  
				my $querystring = "stats.pl.cgi\?uid=$uid\&fid=$fid\&public=1";
				
				# set query string for download script
				my $downloadquery = "download.pl.cgi\?uid=$uid\&public=1" . "\&fid=$fid"; # Don't specify a directory path
				
				my %row = (
						filename => $fn,
						date => $mtime,
						size => $size,
						querystring => $querystring,
						download_query => $downloadquery
						);
			
			 	push(@list, \%row);
			}	 
				 
		 	# call param to fill in the loop with the loop data by reference.
			$template->param(list_loop => \@list);
		}		
			
	}
}