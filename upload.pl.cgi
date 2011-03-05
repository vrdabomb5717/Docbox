#!/usr/bin/perl

# Upload.pl.cgi
# Uploads current file and saves it in the users' home directory.
# March 04, 2011
# Author: Jervis 

## Still to do:
# Handle cases when duplicate file are uploaded.
# Add user authentication verification and Save File to users' directory only. 


use strict;
use CGI qw/:standard/;
use HTML; 

my $q = CGI->new(); # make CGI object
my $homepath = "files"; # Path to home root directory for the current user 
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
<a href="upload_page.pl.cgi"> Upload Another file </a>
<br>
<a href="home.pl.cgi"> Go to Home Page </a>
EOF
}

sub savefile { # Process uploaded File
	my $lightweight_fh  = $q->upload('uploaded_file');
	$filename = scalar $lightweight_fh; # get file name.
	if (defined $lightweight_fh) { # check if file handle defined. 
	
	    my $io_handle = $lightweight_fh->handle; # Change the handle to one compatible with IO::Handle:
	    
	    open (OUTFILE,">$path/$filename") || die "Can't Open File for Writing"; # Open File for Writing. If File Exists, It will be overwritten.
	
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
