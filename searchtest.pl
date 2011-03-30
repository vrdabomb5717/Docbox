#!/usr/bin/perl

# searchtest.pl
# Tests Filesearch.pm to search text files and PDFs for a given query
# Author: Varun Ravishankar
# 27th March 2011

use strict;
use warnings;
use Filesearch;

my ($regex, $path) = @ARGV;


#simple error check to make sure a regular and filepath were actually provided
if (defined($regex) && defined($path))
{
	search($regex, $path);
	
	#searchFile($regex, $path);
	
}
else
{
    die "You really ought to enter a regex and filepath there.\n";
}

sub search
{
	my($regex, $path) = @_;
	
	my @results = Filesearch->search($regex, $path);

    foreach my $lines(@results)
    {
		print "$lines\n";
    }
}

sub searchFile
{
	my($regex, $path) = @_;
	
	my $result = Filesearch->searchFile($regex, $path);

    if($result == 1)
	{
		print "The query was found. Yay!\n";
		return;
	}
	
	print "The query was not found.\n";
}
