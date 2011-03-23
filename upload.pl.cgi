#!/usr/bin/perl

# Upload.pl.cgi
# Uploads current file and saves it in the users' home directory.
# March 04, 2011
# Author: Jervis 

## Currently Expects User ID in through the query String in a GET Request. 

## Still to do:
# Handle cases when duplicate file are uploaded.
# Add user authentication verification and Save File to users' directory only. 

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use CGI qw/:standard/;
use HTML; 
use UserDB;

my $q = CGI->new(); # make CGI object
my $uid = $q->url_param('uid'); # because uid is passed over query string. 
UserDB->validateUser($uid); # Check if valid user logged in. 

my $user = UserDB->getUser($uid); # get userame
my $homepath = "Files/$user"; # Path to home root directory for the current user 
my $path =  $homepath; # path that file is to saved. Default is home directory. 
my $filename; 
savefile(); # Save Uploaded  file. 

HTML->start;
HTML->h1("Success Upload for $filename!");
printLinks();
HTML->end;

sub printLinks{
	
	print <<EOF;
<br>
<a href="upload_page.pl.cgi?uid=$uid"> Upload Another file </a>
<br>
<a href="home.pl.cgi?uid=$uid"> Go to Home Page </a>
EOF
}

sub savefile { # Process uploaded File
	my $lightweight_fh  = $q->upload('uploaded_file');
	$filename = scalar $lightweight_fh; # get file name.
	if (defined $lightweight_fh) { # check if file handle defined. 
	
	    my $io_handle = $lightweight_fh->handle; # Change the handle to one compatible with IO::Handle:
	    
	    open (OUTFILE,">$path/$filename") || die HTML->Error("open for writing","$path/$filename"); # Open File for Writing. If File Exists, It will be overwritten.
	
	    # switch file input/output to Binmode. This ensures that all data will be be preserved regardless of file format.
	    # This is especially important for windows machines where there is a distinction between text file and files like images
	    # that contain binary data. 
	    binmode OUTFILE;   
	    binmode $io_handle; 
	    
	    while (my $bytesread = $io_handle->read(my $buffer,1024)) { # Read Input      
	      print OUTFILE $buffer; # save to file
		}
		close OUTFILE;
	}
}

