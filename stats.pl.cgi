#!/usr/bin/perl

# Statistics
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
use Genstat; 

my $q = CGI->new();
my $uid = $q->param('uid'); # user id (token) of current user.

my $valid = UserDB->validateUser($uid); # validate user correctly logged in, redirect to homepage otherwise. 
if($valid == 0){
	exit; # stop running of user is not logged in. 
}

my $user = UserDB->getUser($uid); # store current user
my $template = HTML::Template->new(filename => 'templates/stats.tmpl');
my $public = $q->param('public'); # get public setting
my $filepath; # store full path to file
my $fid = $q->param('fid');

## Set filepath arguments appropriately for ListStat Function. 
if($public){
	HTML->Error("Parse", "$fid") if(!defined($fid)); # Make sure fid is defined
	$filepath = PublicDB->getFilePathByID($fid);
	
} else { ##use the file id to determine full file path 
	HTML->Error("Parse", "$fid") if(!defined($fid)); # Make sure fid is defined
	my $dbfile = "Files/$user/.user.db"; #get path to user's database
	$filepath = Genstat->getFilePathByID($dbfile,$fid);
} 


listStats($filepath,$user); # listStat takes argumetns: filepath, and username

# send the obligatory Content-Type
print "Content-Type: text/html\n\n";

# print the template
print $template->output();

sub listStats {
	my ($fp, $user) = @_; # fp is file path
	my $dbfile = "Files/$user/.user.db"; # path to user database file
	$user = 'user';
	my $count =0;	
	my $hash_ref_all = Genstat->top30($dbfile, $fp); # get (double) hash ref to top 30 words. Top30 takes arguments:  $dbfile, $filepath  
	
	my @list; # file list data will go here
	
	# Fill user's name and unique id in template:
	my $name = UserDB->getName($uid); 
	$template->param(user => $name);
	$template->param(userid => $uid);
	
	
	## Get and set File Count
	my $filecount = Genstat->num_files($dbfile); 
	$template->param(userfilecount => $filecount);
	
	## Get and set Average File Size
	my $avgfilesize = Genstat->num_files($dbfile);
	$avgfilesize = $avgfilesize/1024; # convert to Kilobytes 
	$avgfilesize = sprintf("%.2f", $avgfilesize); # round to 2 dps.
	$template->param(averagefilesize => $avgfilesize);
	
	## Get and set Total Number of Users
	my $usercount = UserDB->num_users();
	$template->param(totalusers => $usercount);
	
		

	## HTML Format the top 30 words in a table
	while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){
		# Row hash ref has following keys: id, word,count 
		 
		my $word = $row_hash_ref->{'word'};
		my $count = $row_hash_ref->{'count'}; 
				
		my %row = (
				word => $word,
				count => $count
				);
	
	 	push(@list, \%row);
	}	 
		 
 	# call param to fill in the loop with the loop data by reference.
	$template->param(list_loop => \@list);	
}