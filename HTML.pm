#!/usr/bin/perl

# HTML
# Contains static method for generating commonly used HTML code specific to DocBox.
# March 04, 2011
# Author: Jervis

## Still to do 
# * Write HTML Code for passing hidden form containing user id. 

package HTML;

sub start{
	my $title = $_[0];
	print "Content-type: text/html\n\n"; # declaration for cgi script
	print <<EOF;
	<html>
	<head>
	<title> $title </title>
	</head>
	<body bgcolor="orange"> 
EOF
}

sub h1{
	print "<h1> $_[1] </h1>";
}

sub end{
	my $s = "</body></html>";
	print $s; 
}


1;