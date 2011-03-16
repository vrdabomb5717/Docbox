#!/usr/bin/perl

# Perl Script that Generates HTML specific to DocBox Site
# This is simply a testing script
# February 26, 2011
# Author: Jervis


use strict; 
use CGI qw/:standard/;
use HTML;
use HTML::Template;

my $q = new CGI();


use HTML::Template;

  # the fruit data - the keys are the fruit names and the values are
  # pairs of color and shape contained in anonymous arrays
  my %fruit_data = (
                    Apple => ['Red, Green or Yellow', 'Round'],
                    Orange => ['Orange', 'Round'],
                    Pear => ['Green or Red', 'Pear-Shaped'],
                    Banana => ['Yellow', 'Curved'],
                   );

  my $template = HTML::Template->new(filename => 'filelist.tmpl');

  my @loop;  # the loop data will be put in here

  # fill in the loop, sorted by fruit name
  foreach my $name (sort keys %fruit_data) {
    # get the color and shape from the data hash
    my ($color, $shape) = @{$fruit_data{$name}};
    
    # make a new row for this fruit - the keys are <TMPL_VAR> names
    # and the values are the values to fill in the template.
    my %row = ( 
               name => $name,
               color => $color,
               shape => $shape
              );

    # put this row into the loop by reference             
    push(@loop, \%row);
  }

  # call param to fill in the loop with the loop data by reference.
  #$template->param(fruit_loop => \@loop);

  # send the obligatory Content-Type
  print "Content-Type: text/html\n\n";

  # print the template
  #print $template->output;


sub printPass{
	
	my $cgi = new CGI();
	
	my $test = $cgi->param('user');
	print $test;
}