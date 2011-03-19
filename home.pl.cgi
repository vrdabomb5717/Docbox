#!/usr/bin/perl

# Home
# Home page for a user. 
# Lists all files currently owned by the user.
# Authors: Jervis and Varun
# February 26, 2011

### Currently Incomplete. Methods still need to be fully implemented. ###

# Still to Do:
# * Add a hidden form that will be used to maintain user state.  

use strict;
use Fcntl ':flock'; # handle file  i/o
use CGI qw/:standard/;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files. 
#use File::Find;

my $user; # store current user
my $uid; # user id (token) of current user. 

my $q = CGI->new();
my $template = HTML::Template->new(filename => 'templates/filelist.tmpl');


if(validUser()){
	#HTML->start("$user - DocBox");	
	listFiles();
	#print "<br> <a href=upload_page.pl.cgi?uid=$uid> Upload a File </a>"; # uid is defined in validUser routine. 
	#HTML->end();
	
	#successLogin();
	
} else{
	
	HTML->redirectLogin(); # redirect user to login page
}




sub listFiles{ # Producs HTML Output of a Listing of user's file in their root directory.  


## Read Files in User Directory and Print them in HTML


my @files = <Files/$user/*>; # get file and directory listing in user's home directory
my $count =0;


my @list; # file list data will go here
my @abbr = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ); # for date modified

# Fill user's name and unique id in template:
$template->param(user => $user);
$template->param(userid => $uid);

foreach my $filepath (@files){
	$count++;
	# leave only filename. A sample file path is 'Files/user/ColumbiaPic.jpg'. 
	my $filename = substr($filepath, length("Files/$user/"));
	
	open(my $fh, '<', "$filepath") or die "Couldn't open $filename"; # open file for reading only. 
	#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
    #   $atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
    
    my $mtimesecs;
    my $size;
    flock($fh, LOCK_EX); # get file lock handle
    {
    	$mtimesecs = (stat($fh))[9]; # modified time in secs since epoch
    	$size  = (stat($fh))[7]; # file size
	}
	close $fh;
	
    my ($sec,$min,$hour,$mday,$mon,$year) = localtime($mtimesecs); # get detailled time info 
    $year += 1900; #get proper year, since we start from 1900. 
    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
	
	#convert size to kilobytes to 2 decimal places:
	$size =  int($size/1024);
	$size = sprintf("%.2f", $size); # round to 2 dps. 
	
	# set query string for editfile script. 
	my $querystring = "editfile.pl.cgi\?uid=$uid\&filename=$filename";
	
	# set query string for download script
	my $directorypath = "";
	my $downloadquery = "download.pl.cgi\?uid=$uid\&filename=$filename" . "\&directorypath=$directorypath";
	my %row = (
			filename => $filename,
			date => $mtime,
			size => $size,
			querystring => $querystring,
			download_query => $downloadquery
			);

	# put this row into the loop by reference             
    push(@list, \%row);	
}

# call param to fill in the loop with the loop data by reference.
$template->param(list_loop => \@list);

# send the obligatory Content-Type
print "Content-Type: text/html\n\n";

# print the template
print $template->output;
}


sub temp {
# OLD CODE
## Print Headers for Table
	print<<ENDHEADER;
<h2> $user\'s DocBox </h2>
<table border="0">
  <tr>
    <th>File Name</th>
    <th>Date Modified</th>
    <th>File Size</th>
  </tr>
ENDHEADER

########################3

#print "</table>"; # close table
#HTML->h1("Count is $count");	

#############3	
	print <<ENDROW;
<tr>
<td> \$filename </td> <!--File Name -->
<td>&nbsp; </td> <!-- Date Modified -->
<td>&nbsp; </td> <!-- File Size -->
</tr>
ENDROW
	
}

sub successLogin{ # testing method
	print <<EOF;
<h2> Success Login !</h2>
EOF
}


sub validUser{
	getUser(); # get current user and store in $user
	
	if(defined($user)){ # if user found
		return 1;
	}
	else{
		return 0;
	}
}

sub getUser{ # should return user name of currently logged in user. 
	$uid = $q->param('uid'); # gets the UID being passed along. UID is a SHA1 hash of the string "UseranmePasswordHEX"
	$user = UserDB->getUser($uid);
	return $user;
}


sub getFiles{ # should return list of Files belonging to user 
	
}
