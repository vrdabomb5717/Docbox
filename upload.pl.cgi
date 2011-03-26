#!/usr/bin/perl

# Upload.pl.cgi
# Uploads current file and saves it in the users' home directory.
# March 04, 2011
# Author: Jervis 

## Currently Expects User ID in through the query String in a GET Request. 

## Still to do:
# Handle cases when duplicate files are uploaded.
# Impose A File Size Limit : Enforce on client side with JS ??  

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser); # debugging only. remove for production use. 
use HTML; 
use UserDB;
use GenStat;

# Need to handle case when file size too big
# Code below causes CLIC webserver to show 500 Internal error, when size over limit. 
#$CGI::POST_MAX = (1024*1024) * 25;  # maximum upload filesize is 25 Megabytes

my $q = CGI->new(); # make CGI object
my $uid = $q->url_param('uid'); # because uid is passed over query string.
my $public =  $q->url_param('public');
my $comments = $q->url_param('comments');
my $tags = $q->url_param('tags');

UserDB->validateUser($uid); # Check if valid user logged in. 

my $user = UserDB->getUser($uid); # get userame
my $homepath = "Files/$user"; # Path to home root directory for the current user 
my $path =  $homepath; # path that file is to saved. Default is home directory. 
my $filename; 

#checkLimit(); # not tested yet. 
savefile(); # Save Uploaded  file. 

HTML->start;
HTML->h1("Success Upload for $filename!");
printLinks();
HTML->end;

sub checkLimit{ # ensures file size limit. 
	 if ($q->cgi_error()) {
        print $q->cgi_error();
        print <<'EOF';
    <p>
    The file you are attempting to upload exceeds the maximum allowable file size of 25Megabytes.
    <p>
    Please Select a file that is less than 25MB and try again. 
EOF
        print $q->hr, $q->end_html;
        exit 0;
    }
}

sub printLinks{
	
	print <<EOF;
<br>
<a href="upload_page.pl.cgi?uid=$uid"> Upload Another file </a>
<br>
<a href="home.pl.cgi?uid=$uid"> Go to Home Page </a>
EOF
}


sub savefile { # Process uploaded File
	my $fh  = $q->upload('uploaded_file'); # get file handle
	$filename = scalar $fh; # get file name.
	if (defined $fh) { # check if file handle defined. 
	
	    #my $io_handle = $lightweight_fh->handle; # Change the handle to one compatible with IO::Handle:
	    
	    open (OUTFILE,">$path/$filename") || die HTML->Error("open for writing","$path/$filename"); # Open File for Writing. If File Exists, It will be overwritten.
	
	    # switch file output only to Binmode. This ensures that all data will be be preserved regardless of file format.
	    # Note that switching to binmode on file handles causes a server error on CLIC webserver, so don't do that. 
	    binmode OUTFILE;   
	     	    
	    while(<$fh>){ # read file a line at time
	    	print OUTFILE $_; # save output to file. 
	    }
	    
		close OUTFILE; # close file. 
		
		## Add file to database.
		my $dbfile = "$path/.user.db"; # user db file
		my $fp = "$path/$filename";  # full file path
		#addfile takes arguments in form: $dbfile, $filepath, $filename, $public, $comments, $tags	
		Genstat->addFile($dbfile, $fp, $filename, );
		
		return; # exit function
	}
	
	HTML->Error("open file handle","$fh");
}

## Old Code
## Doesn't work on CLIC
sub savefile_OLD { # Process uploaded File
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