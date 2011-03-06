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
use File::Find;

my $user; # store current user

my $q = CGI->new();

if(validUser()){
	HTML->start("$user - DocBox");
	listFiles();
	print "<br> <a href=upload_page.pl.cgi> Upload a File </a>";
	HTML->end();
	
	#successLogin();
	
} else{
	
	HTML->redirectHome(); # redirect user to login page
}


sub listFiles{ # Producs HTML Output of a Listing of user's file in their root directory.  
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

## Read Files in User Directory and Print them in HTML


my @files = <Files/$user/*>; # get file and directory listing in user's home directory
my $count =0;
foreach my $filepath (@files){
	$count++;
	# leave only filename. A sample file path is 'Files/user/ColumbiaPic.jpg'. 
	my $filename = substr($filepath, length("Files/$user/"));
	print <<ENDROW
<tr>
<td> $filename </td> <!--File Name -->
<td>&nbsp; </td> <!-- Date Modified -->
<td>&nbsp; </td> <!-- File Size -->
</tr>
ENDROW
}

print "</table>"; # close table
HTML->h1("Count is $count");
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
	my $uid = $q->param('uid'); # gets the UID being passed along. UID is a SHA1 hash of the string "UseranmePasswordHEX"
	$user = UserDB->getUser($uid);
	return $user;
}


sub getFiles{ # should return list of Files belonging to user 
	
}
