#!/usr/bin/perl

# Group
# Groups the user selected file into its own directory.  
# Authors: Jervis 
# March 29, 2011

### Currently Incomplete. Methods still need to be fully implemented. ###

# Still to Do:
# * Add a hidden form that will be used to maintain user state.  

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files.
use Genstat; 
use File::Copy; # provides functionality to copy and rename files
use Log;


my $q = CGI->new();
my $uid = $q->param('uid'); # user id (token) of current user.
$uid = $q->url_param('uid') if (!defined($uid)); # for when we have mixed post/get data. 


my $ip = $ENV{'REMOTE_ADDR'};
my @fids = $q->param('selectedfiles'); # get list of fids on which to act on.  

my $valid = UserDB->validateUser($uid); # validate user correctly logged in, redirect to homepage otherwise. 
if($valid == 0){
	exit; # stop running of user is not logged in. 
}





my $user = UserDB->getUser($uid); # store current user
my $template = HTML::Template->new(filename => 'templates/group.tmpl');
my $op_template = HTML::Template->new(filename => 'templates/group_op.tmpl'); # for making html for successful operation / any errors


# Fill user's name and unique id in template:
my $name = UserDB->getName($uid); 
$template->param(user => $name);
$template->param(userid => $uid);

## Put username in OP template
$op_template->param(user => $name);
$op_template->param(userid => $uid);

## Check if user visiting us for first time
my $first = $q->param('firstvisit'); # comes in thru a hidden form field and always true on true first visit. 
$first = 0 if(!defined($first));  # set firstvisit to false. 
if($first == 1){
	
	if (int(@fids) == 0){
		## Print Error
		$template->param(nofiles_selected => 1); # Show MSG telling user to select files
		print $q->header(); 
		print $template->output();
		exit; 
	 	
	}	
	
	$template->param(group => 1); # Show confirmation to do file grouping. 
	
	my @list; # list that will be used to print filenames to be grouped.  
	my $filename;
	my $dbfile = "Files/$user/.user.db"; # user db file
	foreach my $fid (@fids){
		
		$filename =Genstat->getFileNameByID($dbfile, $fid);  
		my %row = (	filename => $filename,
					fid => $fid); # save fid to preserve state. 
		
		# put this row into the loop by reference             
		push(@list, \%row);    	
	}
	
	$template->param(list_loop => \@list);
	
	print $q->header(); 
	print $template->output();
	exit;
	
}

else{ ## Try to do File Grouping. 
	
	my $dir = $q->param('dirname');
	my $dbfile = "Files/$user/.user.db"; # user db file
	
	if(!defined($dir) || $dir eq ''){ # if user didn't specify directory name, print error and exit. 
		print $q->header();
		$op_template->param(error => 1);
		print $op_template->output();
		exit; 
	} 
	my $result = mkdir "Files/$user/$dir"; # attempt to make directory. 
	my $filepath; # filepath to the current file being processed.
	my $filename;
	my $dest;  
	foreach my $fid (@fids){
		
		$dest = "Files/$user/$dir/";
		$filepath = Genstat->getFilePathByID($dbfile, $fid);
		$filename = Genstat->getFileNameByID($dbfile, $fid); # get filename
		move($filepath, $dest); # when source is a file, and dest a directory, then move moves sourcefile into destination directory
		
		## Update User DB with new paths.
		my $oldpath = $filepath;  
		my $newpath = "$dest" . "$filename";
		Genstat->updateFile($dbfile, $oldpath, $filename, $newpath, $filename); # arguments are: $dbfile, $oldpath, $oldname, $newpath, $newname
		
		## Log Group OP. 
		my $time = localtime();
		Log->log("$user successfully moved $oldpath to $newpath at $time. IP = $ip");     	
	}
	
	$op_template->param(success => 1); # Print Success message
	print $q->header();
	print $op_template->output();
	exit;
}
