#!/usr/bin/perl

# Reset Passord HTML Page
# Gives HTML page to perform password reset.  
# Authors: Jervis
# March 21, 2011

### Still To DO  ###
## * 

use strict;
use CGI qw/:standard/;
use HTML;
use HTML::Template; # for creating html from template files. 
use UserDB; 

my $q = CGI->new();
my $uid = $q->param('uid');
my $template = HTML::Template->new(filename => 'templates/reset.tmpl');
my $query_length = length();


if(defined($ENV{"QUERY_STRING"})){ # if query string empty, means that user just visited us to reset pass.  
	$template->param(resetpage => 1); # toggle reset password page on
	print $q->header(); # print http headers
	print $template->output();
}else{ # check if query string contains user id, validate it then show change pass page 
	
	if(defined($uid) && $uid ne ''){ # if user token id defined and non-empty
		##validate user id. If wrong, return to homepage
		UserDB->validateUser($uid);		
		
		$template->param(passwordchange => 1); # show password change page
		$template->param(userid => $uid); # store user id in hidden field
		print $q->header(); # print http headers
		print $template->output();
		
	}else{ #if  invalid query string
		HTML->redirectLogin(); # go to home page. 
	}
}

