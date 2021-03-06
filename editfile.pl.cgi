#!/usr/bin/perl

# Edit File
# Manipulates A File for the user. 
# Can Copy, Delete, Rename and Download
# Authors: Jervis
# March 16, 2011

### Still To DO  ###
## * Add Safety checking to user input. e.g. user gives same filename for copy opertaion etc.
## * Collision check for rename operation. 
## * Add Full FIle PAths so that ops will work inside directories

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
use File::Copy; # provides functionality to copy and rename files
use Genstat;
use Log; 

my $user; # store current user
my $uid; # user id (token) of current user. 

my $q = CGI->new();
print $q->header(); # Print HTML Headers
my $template = HTML::Template->new(filename => 'templates/editfile.tmpl');
my $op_template = HTML::Template->new(filename => 'templates/fileop.tmpl'); # for making html for successful operation

$uid = $q->param('uid'); # because uid is passed over query string.
$uid = $q->url_param('uid') if(!defined($uid)); # for when uid is in post data and we're have mixed post/get.
UserDB->validateUser($uid); # Check if valid user logged in. Redirect to login page otherwise.

$user = UserDB->getUser($uid); # get username of current logged in user.

my $ip = $ENV{'REMOTE_ADDR'}; ## get ip address of user. 

## Define source file path for current user. 
# Will need to add directory path, after enabling grouping funtionality. 
my $sourcefilepath = "Files/$user/"; 
my $dir = $q->param('dir');
if(!defined($dir)){
	$dir = '';
}

if($dir ne ''){ ## Only IF directory path NOT empty, then append dir to the source filepath
	$sourcefilepath = "Files/$user/$dir/";	
}

my $filename = $q->param('filename');
$filename = $q->url_param('filename') if(!defined($filename));# for when filename is in post data and we're have mixed post/get.


## save extension of filename
my @s = split(/\./, $filename);
my $n = int(@s) - 1; # minus one to get correct index
my $extension =  $s[$n];

# Set user's name
my $name = UserDB->getName($uid);
$template->param(user => $name);

## Save Filename and user id in hidden form field to preserve user state
$template->param(userid => $uid); 
$template->param(filename => $filename);

## Get and Set the File ID
my $dbfile = "Files/$user/.user.db";
my $fp =  "$sourcefilepath" . "$filename"; 
my $fid = Genstat->getFileID($dbfile, $fp);
$template->param(fid => $fid);

## Set the dir string value
$template->param(dir => $dir);

my $renamedfilename = $q->param('renamedfile'); # comes thru post 
my $copyfilename = $q->param('copyfilename'); # comes thru post

my $prevlink; # stores link back to directory/file listing
my $prevlink_form = $q->param('prevlink'); #  

my $deleteoption = $q->param('delete'); # get user delete command
my $publicoption = $q->param('public'); # get user setting for privacy. 

if(!defined($prevlink_form)){
	$prevlink = $ENV{'HTTP_REFERER'}; # get previous page's link	
}else{
	$prevlink = $prevlink_form;
}
 
$template->param(prevlink => $prevlink); # write link to return to previous page.
$op_template->param(prevlink => $prevlink);
$op_template->param(filename => $filename); # show user filename of file being operated on. 

my $badinput; 
### Check for Bad User Input
if ( $renamedfilename eq '' && $copyfilename eq ''){ # if both fields empty
	$badinput = 1;
}
elsif($renamedfilename ne '' && $copyfilename ne ''){ # if both field defined
	$badinput = 1;
} elsif($copyfilename eq $filename || $renamedfilename eq $filename){ # copy/rename filename is same as actual copy of file. 
	$badinput = 1;
}



# special case for when, user first visits editfile page. In that case, 
# copyfilename & renamedfile nameare undefs.
if(!defined($copyfilename) || !defined($renamedfilename)){ 
	$badinput = 0; 
}

if($badinput){ ## Stop if bad input
	$template->param(badinput => 1);
	print $template->output();
	exit;
}



if($renamedfilename){ # if renmaedfilename field specified
		
	my $source = "$sourcefilepath" . "$filename"; 
	my $dest = "$sourcefilepath" . "$renamedfilename" . ".$extension";
	
	# move function overwrites filesystem with the destination filename. 
	# so if any file exits beforehand with same name as user supplied filename (to use for renaming)
	# then that file on the filesystem is overwritten.  
 
	my $success = move($source, $dest);
	if($success == 0){ ## check if rename failed
		HTML->Error("Rename", "the File from $source to $dest "); # Print Error
		my $time = localtime();
		Log->log("Rename Operation by $user at IP $ip Failed. Source:$source and Destination:$dest. Time: $time");
		exit;
	}
	## Update Database.
	my $dbfile = "Files/$user/.user.db";
	Genstat->updateFile($dbfile, $source, $filename, $dest, $renamedfilename); # takes arguments: $dbfile, $oldpath, $oldname, $newpath, $newname
	
	## Log Successful operation
	my $time = localtime();
	Log->log("Rename Operation by $user at IP $ip Succeeded. Source:$source and Destination:$dest. Time: $time");
	
	$op_template->param(operation => 'Rename');
	print $op_template->output();
	exit;
		
}

if($copyfilename){ # if copyfilename field specified
	
	my $source = "$sourcefilepath" . "$filename"; 
	my $dest = "$sourcefilepath" . "$copyfilename" . ".$extension";
	
	my $success = copy($source, $dest);
	if($success == 0){ ## check if copy failed
		HTML->Error("Copy", "the File from $source to $dest "); # Print Error
		my $time = localtime();
		Log->log("Copy Operation by $user at IP $ip Failed. Source:$source and Destination:$dest. Time:$time");
		exit;
	}
	
	## Update Database. 
	my $dbfile = "Files/$user/.user.db";
	my $hash_ref = Genstat->getFileRecord($dbfile, $source); # Supply sourcepath b'se DB not yet updated. 
	
	## Copy over Old File Record Details
	my $public = $hash_ref->{public};
	my $comments = $hash_ref->{comments};
	my $tags = $hash_ref->{tags};
	
	Genstat->addFile($dbfile, $dest, "$copyfilename.$extension", $public, $comments, $tags); # arguments: $filepath, $filename, $public, $comments, $tags
	
	
	## Log Successful operation
	my $time = localtime();
	Log->log("Copy Operation by $user at IP $ip Succeeded. Source:$source and Destination:$dest. Time:$time");
	
	
	$op_template->param(operation => 'Copy');
	print $op_template->output();
	exit;
}


if(defined($deleteoption)){
	if($deleteoption eq 'Yes'){
		
		my $file= "$sourcefilepath" . "$filename";
		my $success = unlink($file);
		
		if($success == 0){ ## Check if delete operation failed
			HTML->Error("Delete", "the File $file"); # Print Error
			my $time = localtime();
			Log->log("Delete Operation by $user at IP $ip Failed. Source:$file. Time:$time ");
			exit;
		}
		
		## Update Database:
		my $dbfile = "Files/$user/.user.db";
		Genstat->removeFile($dbfile, $file, $filename);  # argumetns are : $dbfile, $filepath, $filename
		
		my $time = localtime();
		Log->log("Delete Operation by $user at IP $ip Succeeded. Source:$file. Time:$time"); # Log Deletion. 
		
		$op_template->param(operation => 'Delete');
		print $op_template->output();
		exit;
	} 
}


if(defined($publicoption)){
	if($publicoption eq 'Yes'){
		my $file= "$sourcefilepath" . "$filename";
		
		## Update DB:
		my $dbfile = "Files/$user/.user.db";
		Genstat->makePublic($dbfile, $file);  # argumetns are : $dbfile, $filepath
		
		my $time = localtime();
		Log->log("Make File Public Operation by $user at IP $ip Succeeded. Source:$file. Time:$time"); # Log file privacy change 
		
		$op_template->param(operation => 'File Privacy');
		print $op_template->output();
		exit;
	} else{ # make private
		
		my $file= "$sourcefilepath" . "$filename";
		
		## Update DB:
		my $dbfile = "Files/$user/.user.db";
		Genstat->makePrivate($dbfile, $file);  # argumetns are : $dbfile, $filepath
		
		my $time = localtime();
		Log->log("Make File Private Operation by $user at IP $ip Succeeded. Source:$file. Time:$time"); # Log file privacy change 
		
		$op_template->param(operation => 'Privacy');
		print $op_template->output();
		exit;
		
	}
}

# print the template
print $template->output;