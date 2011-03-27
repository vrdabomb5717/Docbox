#!/usr/bin/perl

#Filesearch.pm
#Contains method for searching text files, PDF files, and Word documents for a given regular expression
#Author: Varun Ravishankar
#26th March 2011

package Filesearch;

use strict;
use warnings;

#use CAM::PDF;
use Text::Extract::Word;

sub search
{
    my ($self, $regex, $homepath) = @_;

    #search text files, and return those results
    my $files = `grep -lrs "$regex" "$homepath" `;
    #$files =~ s/' '/\\' '/g;
    my @results = split(/'\n'/, $files);


    #search for all PDF files
    $files = `find "$homepath" -type f -name '*.pdf' -print`;
    my @filenames = split(/\n/, $files);

    foreach my $line (@filenames)
    {
	$line =~ s/\///;
	$line = "/" . "$line";

	#extract text of PDF, search for $regex, and if search returns true, push file into list
	my $exitcode = `pdftotext -q "$line" - | grep "$regex"`;
	$exitcode = $?;

	if($exitcode == 0)
	{
	    push (@results, $line);
	}
    }

    $files = `find "$homepath" -type f -name '*.doc' -print`;
    @filenames = split(/'\n'/, $files);

    #foreach my $line (@filenames)
    #{
	#extract text of Word document, search for $regex, and if search returns true, push file into list
	
	#push(@results, $line);
    #}

    return @results;    
}

1;
