#!/usr/bin/perl

# Public
# Shows all available public files.  
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




my $q = CGI->new();
my $uid = $q->param('uid'); # user id (token) of current user.

my $valid = UserDB->validateUser($uid); # validate user correctly logged in, redirect to homepage otherwise. 
if($valid == 0){
	exit; # stop running of user is not logged in. 
}

my $user = UserDB->getUser($uid); # store current user
my $template = HTML::Template->new(filename => 'templates/public.tmpl');

listFiles();

# send the obligatory Content-Type
print "Content-Type: text/html\n\n";
	
# print the template
print $template->output;


sub listFiles{ # Producs HTML Output of a Listing of user's file in their root directory.  
	#$user = 'user'; ### DELTE FROM PRODCTION VERSION
	my $count =0;	
	my $hash_ref_all = PublicDB->getFiles($user); # get (double) hash ref to all public files 
	
	my @list; # file list data will go here
	my @abbr = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ); # for date modified
	
	# Fill user's name and unique id in template:
	my $name = UserDB->getName($uid); 
	$template->param(user => $name);
	$template->param(userid => $uid);
	
	
	my $fp; # file path
	my $fn;  # file name
	my $tm; # time modified
	my $size; # size in bytes

	while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){
		#my $row_hash_ref = $hash_ref_all->{$row}; # deref hash reference
		
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
		#my $downloadquery = "download.pl.cgi\?uid=$uid\&filename=$file" . "\&directorypath=$dir";
		my $downloadquery = "download.pl.cgi\?uid=$uid\&public=1" . "\&fid=$fid";
		
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
	
	


