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

## To be implemented
sub hiddenForm{ # Makes a hidden form. 

	print<<EOF;
<form>
</form>

EOF
	
}


sub Error{  
   print "Content-type: text/html\n\n";  
   print "The server can't $_[1] the $_[2]: $! <br>";
   my $prev = $ENV{'HTTP_REFERER'};
   print "<a href=\"$prev\">Click Here </a> to go back and try again. <br> ";  
   exit;  
 }

sub redirectLogin{
	print <<EOF;
Status: 302 Moved Temporarily
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