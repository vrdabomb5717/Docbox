#!/usr/bin/perl

# Perl Script that Generates HTML specific to DocBox Site
# This is simply a testing script
# February 26, 2011
# Author: Jervis


use strict; 
use CGI qw/:standard/;



sub printPass{
	
	my $cgi = new CGI();
	
	my $test = $cgi->param('user');
	print $test;
}