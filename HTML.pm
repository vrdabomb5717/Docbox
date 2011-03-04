#!/usr/bin/perl

# HTML
# Contains static method for generating commonly used HTML code specific to DocBox.
# February 26, 2011


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

sub end{
	my $s = "</body></html>";
	print $s; 
}


1;