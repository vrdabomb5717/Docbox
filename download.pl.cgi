#!/usr/bin/perl

# Download.pl.cgi
# Downloads the given file to the user's browser. 
# Authors: Jervis
# March 19, 2011


## Still to DO:
# * add checking of file name supplied. (taint mode ??)
# * 


BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use CGI qw/:standard/; 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 
use PublicDB; 


my $user; # store current user
my $uid; # user id (token) of current user. 


my $q = CGI->new();
#print $q->header(); # Print HTML Headers
#my $template = HTML::Template->new(filename => 'templates/editfile.tmpl');
#my $op_template = HTML::Template->new(filename => 'templates/fileop.tmpl'); # for making html for successful operation

$uid = $q->param('uid'); # because uid is passed over query string.
$uid = $q->url_param('uid') if(!defined($uid)); # for when uid is in post data and we're have mixed post/get.
UserDB->validateUser($uid); # Check if valid user logged in. Redirect to login page otherwise.

my $public = $q->param('public');
my $fid = $q->param('fid');

if($public){
	my $fp = PublicDB->getFilePathByID($fid); # filepath
	my $fn = PublicDB->getFileNameByID($fid); #filename
	download($fp, $fn); # download takes arguments 'filepath, filename'
	exit;
}
else {
	$user = UserDB->getUser($uid); # get username of current logged in user.
	
	#get currently working directory path for the file. 
	my $dirpath = $q->param('directorypath');  # dirpath shouldn't NOT containing trailling '/'
	
	if(!defined($dirpath)){
		$dirpath = '';
	}
	
	## Define source file path for current user. 
	# Will need to add directory path, after enabling grouping funtionality. 
	my $sourcefilepath = "Files/$user/$dirpath" ; 
	
	if($dirpath eq ''){ ## if not Directory Path Specified, Assume user root directory. 
		$sourcefilepath = "Files/$user" ;
	}
	
	my $filename = $q->param('filename');
	my $fp = "$sourcefilepath/$filename"; # filepath
	
	download($fp, $filename);
	exit;
}

sub download{
	my $filepath = $_[0]; # get given file path
	my $filename = $_[1]; # get filename
	
	if(-d $filepath){ # if directory
		`tar -cvf temp.tar $filepath`; # zip directory into tar
		my $dfile = "temp.tar";
		open(FH, $dfile) || die Error('open',$dfile); # opens file for reading.
		$filename = "$filename.tar"; # append .tar extension to filename so that this is the name of file being downloaded.	
	  
	} else{
		open(FH, $filepath) || die Error('open',$filepath); # opens file for reading.
	 	
	}
	
	 
	 
	#switch both input and output handles to binary mode to ensure proper file transfer.
	binmode STDOUT; 
	binmode FH; 
	
	## Download the file.
	# The Headers below will force browse to show save as dialog rather than 
	# showing/vieweing the file.  
	
	print $q->header(-type            => 'application/x-download',
	                 -attachment      => $filename,
	                 'Content-length' => -s $filepath
	   				);
	
	print while(<FH>); # reading file one line at a time. 
	close FH;
}

sub Error{  
   print "Content-type: text/html\n\n";  
   print "The server can't $_[0] the $_[1]: $! \n";  
   exit;  
 }
