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
    my @results = Filesearch->search($regex, $path);

    foreach my $lines(@results)
    {
	print "$lines\n";
    }
}
else
{
    die "You really ought to enter a regex and filepath there.\n";
}
