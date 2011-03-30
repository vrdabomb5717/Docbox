#!/usr/bin/perl

#Filesearch.pm
#Contains method for searching text files, PDF files, and Word documents for a given regular expression
#Author: Varun Ravishankar
#26th March 2011

package Filesearch;

use strict;
use warnings;
use Text::Extract::Word;
#use RTF::TEXT::Converter;

#search for a query given the path to search at. Searches text files, PDFs, Word documents, RTF files, and anything else grep might inadverdently recognize.

#returns array where each element is a filepath with a result
sub search
{
    my ($self, $query, $homepath) = @_;

    #get the last character of $homepath so we can later append a / for `find`
    my @home = split('', $homepath);
    my $lastchar = $home[-1];
    pop(@home) if $lastchar eq '/';
    $homepath = join('', @home);

    #search text files and RTF files, and return those results
	#silenced all error messages so they don't interfere with results.
    my $files = `grep -ilrs "$query" "$homepath" `;
    #$files =~ s/' '/\\' '/g;
    my @results = split(/\n/, $files);
    
    pop(@results) if scalar(@results) > 0 && "$results[-1]" eq '\t';
    #print scalar(@results) . "\n";

    #search for all PDF files and returns the paths of those files
    $files = `find "$homepath" -type f -name '*.pdf' -print`;
    my @filenames = split(/\n/, $files);

    foreach my $line (@filenames)
    {
		#removes the extra slash that find places in the path.
		#I think these lines just undo each other's changes, but keeping them for now.
		#$line =~ s/\///;
		#$line = "/" . "$line";

		#extract text of PDF, search for $query, and if search returns true, push file into list
		my $exitcode = `pdftotext -q "$line" - | grep -ils "$query"`;
		$exitcode = $?;

		if($exitcode == 0)
		{
	    	push (@results, $line);
		}
    }

    #search for all Word documents
    $files = `find "$homepath" -type f -name '*.doc' -print`;
    @filenames = split(/\n/, $files);

    foreach my $line (@filenames)
    {
		#removes the extra slash that find places in the path.
		#I think these lines just undo each other's changes, but keeping them for now.
		#$line =~ s/\///;
		#$line = "/" . "$line";

		
		#extract text of Word document, search for $query
		#if search returns true, push file into @results
		
		my $doc = Text::Extract::Word->new("$line");
		my $text = $doc->get_text();
		
		if($text =~ /$query/ix)
		{
	    	push(@results, $line);
		}
    }

    
    #search for all RTF files
    #$files = `find "$homepath" -type f -name '*.rtf' -print`;
    #@filenames = split(/\n/, $files);
    
    #foreach my $line (@filenames)
    #{
		#$line =~ s/\///;
		#$line = "/" . "$line";

		#extract text of RTF file, search for $query, and if search returns true, push file into @results
		#my $text;
		#my $object = RTF::TEXT::Converter->new(output => \$text);
		#$object->parse_string($line);

		#if($text =~ /"$query"/i)
		#{
	    #	push(@results, $line);
		#}
    #}

	my %seen = ();
	my @unique = grep { ! $seen{ $_ }++ } @results;

    return @unique;    
}

#search for the query in the given filepath. Returns 0 if not in file, and 1 if query is present.
#Query is case-insensitive.
sub searchFile
{
	my ($self, $query, $filepath) = @_;
	
	#extracts filetype from the filename	
	my @suffix = split('\.', $filepath);
	my $length = int(@suffix);
	
	#use extension to determine type
	my $kind = $suffix[$length - 1];
	$kind = lc($kind);
	#print "kind is $kind.\n";
	
	if($kind eq "pdf")
	{
		#extract text of PDF, search for $query, and if search returns true, return
		my $exitcode = `pdftotext -q "$filepath" - | grep -ils "$query"`;
		$exitcode = $?;

		if($exitcode == 0)
		{
	    	return 1;
		}
	}
	elsif($kind eq "doc")
	{
		my $doc = Text::Extract::Word->new("$filepath");
		my $text = $doc->get_text();
		#print "$text\n";
		
		if($text =~ /$query/ix)
		{
	    	return 1;
		}
	}
	else
	{
		my $files = `grep -ils "$query" "$filepath" `;
		my $exitcode = $?;

		if($exitcode == 0)
		{
	    	return 1;
		}
	}
	
	return 0;
}

1;
