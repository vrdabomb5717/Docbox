#!/usr/bin/perl

# HTML
# Contains static method for generating commonly used HTML code specific to DocBox.
# March 04, 2011
# Author: Jervis

## Still to do 
# * Write HTML Code for passing hidden form containing user id. 

package HTML;

sub start{
	my $title = $_[1];
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

sub redirectHome{
	print <<EOF;
Status: 302 Relocate status
Location: index.html
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Registration Complete</TITLE>
</HEAD>
<BODY>
<H1>Registeration Complete !</h1>
<p> You will automatically be redirected soon to the login page. <a href=index.html>Click here</a> to manually return to the home page</p>
</BODY>
</HTML>

EOF
}


1;