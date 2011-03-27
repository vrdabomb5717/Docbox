#!/usr/bin/perl

# Home
# Home page for a user. 
# Lists all files currently owned by the user.
# Authors: Jervis and Varun
# February 26, 2011

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
#use File::Find;


 

my $q = CGI->new();
my $uid = $q->param('uid'); # user id (token) of current user.
my $dir = $q->param('dir'); # get current directory relative to the User's Home Directory.  

$dir = '' if !(defined($dir)); # if dir is not given in query string, set it to empty. 

my $valid = UserDB->validateUser($uid); # validate user correctly logged in, redirect to homepage otherwise. 
if($valid == 0){
	exit; # stop running of user is not logged in. 
}

my $user = UserDB->getUser($uid); # store current user
my $template = HTML::Template->new(filename => 'templates/filelist.tmpl');

listDirs();
listFiles();

# send the obligatory Content-Type
print "Content-Type: text/html\n\n";
	
# print the template
print $template->output;

sub listDirs{ # Producs HTML Output of a Listing of user's file in their root directory.  
	
	my $count =0;	
	
	my @list; # file list data will go here
	my @abbr = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ); # for date modified
	
	# Fill user's name and unique id in template:
	$template->param(user => $user);
	$template->param(userid => $uid);
	
	
	my $subdir = "Files/$user/$dir"; # set subdirectory if any specified; otherwise, working at root of user's directory.
	opendir(my $dh, $subdir); 
	
	while(defined(my $file = readdir $dh)){
		if(-d "$subdir/$file"){ # -f specifies if file handle is a directory
			if($file eq '.' || $file eq '..'){
				next; # skip the . and .. directories. 
			}
			$count++;
			my $filepath = "$subdir/$file";
			
			#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
	        #$atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
	    	
			my $mtimesecs = (stat($filepath))[9]; # modified time in secs since epoch
	    	my $size  = (stat($filepath))[7]; # file size
	    	
	    	my ($sec,$min,$hour,$mday,$mon,$year) = localtime($mtimesecs); # get detailled time info 
		    $year += 1900; #get proper year, since we start from 1900. 
		    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
			
			#convert size to kilobytes to 2 decimal places:
			$size =  int($size/1024);
			$size = sprintf("%.2f", $size); # round to 2 dps. 
			
			# set query string for opening directory. 
			my $querystring = "home.pl.cgi\?uid=$uid\&filename=$file\&dir=$file";
			
			# set query string for download script
			my $downloadquery = "download.pl.cgi\?uid=$uid\&filename=$file" . "\&directorypath=$dir";
			my %row = (
					dirname => $file,
					date => $mtime,
					size => $size,
					querystring => $querystring,
					download_query => $downloadquery
					);
		
			# put this row into the loop by reference             
		    push(@list, \%row);	
		}
	}
		
	# call param to fill in the loop with the loop data by reference.
	$template->param(dir_loop => \@list);
	
	
}





sub listFiles{ # Producs HTML Output of a Listing of user's file in their root directory.  
	
	my $count =0;	
	
	my @list; # file list data will go here
	my @abbr = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ); # for date modified
	
	# Fill user's name and unique id in template:
	$template->param(user => $user);
	$template->param(userid => $uid);
	
	
	my $subdir = "Files/$user/$dir"; # set subdirectory if any specified; otherwise, working at root of user's directory.
	opendir(my $dh, $subdir); 
	
	while(defined(my $file = readdir $dh)){
		if(-f "$subdir/$file"){ # -f specifies if file handle is a file
			$count++;
			my $filepath = "$subdir/$file";
			
			if($dir eq '' && $file eq '.user.db'){ ## Don't Print User Datababse File. 
				next;
			}
			
			#my ($dev,$ino,$mode,$nlink,$uniqueid,$gid,$rdev,$size,
	        #$atime,$mtime,$ctime,$blksize,$blocks) = stat $fh;
	    	
			my $mtimesecs = (stat($filepath))[9]; # modified time in secs since epoch
	    	my $size  = (stat($filepath))[7]; # file size
	    	
	    	my ($sec,$min,$hour,$mday,$mon,$year) = localtime($mtimesecs); # get detailled time info 
		    $year += 1900; #get proper year, since we start from 1900. 
		    my $mtime = "$hour:$min:$sec $abbr[$mon] $mday $year"; #E.g.  07:12:43 Oct 12 2011. 
			
			#convert size to kilobytes to 2 decimal places:
			$size =  int($size/1024);
			$size = sprintf("%.2f", $size); # round to 2 dps. 
			
			# set query string for editfile script. 
			my $querystring = "editfile.pl.cgi\?uid=$uid\&filename=$file\&dir=$dir";
			
			# set query string for download script
			my $downloadquery = "download.pl.cgi\?uid=$uid\&filename=$file" . "\&directorypath=$dir";
			my %row = (
					filename => $file,
					date => $mtime,
					size => $size,
					querystring => $querystring,
					download_query => $downloadquery
					);
		
			# put this row into the loop by reference             
		    push(@list, \%row);	
		}
	}
		
	# call param to fill in the loop with the loop data by reference.
	$template->param(list_loop => \@list);
}

## backup version, incase need to revert. 
sub listFiles_OLD{ # Producs HTML Output of a Listing of user's file in their root directory.  


## Read Files in User Directory and Print them in HTML

my @files;
if(length($dir) == 0){ # no subdirectory specified. 
	@files = <Files/$user/*>; # get file and directory listing in user's home directory	
} else {
	@files = <Files/$user/$dir/*>; # get file and directory listing in user's home directory
}

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




sub getFiles{ # should return list of Files belonging to user 
	
}
