#!/usr/bin/perl

# Email.pl.cgi
# Emails user a password reset link.  
# Authors: Jervis
# March 21, 2011

BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
}
use strict;
use CGI qw/:standard/; 
use HTML;
use UserDB; # use for validating user.
use HTML::Template; # for creating html from template files.

my $q = CGI->new();
print $q->header(); # Print HTTP Header
 
my $email; # user supplied email address
my $fname; #user supplied first name
my $lname; #user supplied last name
my $msg_body;
my $resetlink;
my $validemail; 
my $uid; #user id token. 


  
$email = $q->param('email');
$fname= $q->param('firstname');
$lname = $q->param('lastname');
#$validemail = UserDB->validEmailAndName($email);  # checks if email along with supplied names exists in database. Names are case-sensitive
$validemail = UserDB->validEmail($email);  # checks only if email exists in database.
my $template; # html template object 

if(malformed_email($email)){
	$template = HTML::Template->new(filename => 'templates/reset.tmpl'); # warn user about malformed email and ask to retry
	$template->param(badinput => 1); # flag bad input. 
	print $template->output();
	exit; 
} elsif($validemail) {
	$uid = UserDB->getUserID($email);
	write_msg();
	send_mail(); 
	$template = HTML::Template->new(filename => 'templates/success.tmpl'); # successful email sent. 
	$template->param(passwordchange => 1); # toggles html logic to show successful email  sent page
	print $template->output();
	exit;
} else{ # Email supplied does not exist. 
	
	$template = HTML::Template->new(filename => 'templates/success.tmpl'); # successful email sent. 
	$template->param(passwordchange => 1); # toggles html logic to show successful email  sent page
	print $template->output();	
}



sub write_msg{ # write msg to $msg_body
	my $server = $ENV{'HTTP_HOST'}; # e.g. web3157.cs.columbia.edu
	my $file = $ENV{'SCRIPT_FILENAME'}; # e.g. /home.pl.cgi
	my $script_name = "email.pl.cgi";
	my $strlen = -1 * length($script_name); #negative to so that we start counting at end of string. 
	my $dirpath = substr($file,0,$strlen); # strlen is NEGATIVE
	
	$dirpath = "/~jjm2190/public/project/"; # hard-set for project submission. 
	
	my $base = "http://" . "$server" . "$dirpath" . "reset_page.pl.cgi";
	my $query="\?uid=$uid"; # set query string. 
	$resetlink = "$base" . "$query"; 
	$msg_body = 
"Dear $fname, 
Thank you for using DocBox. At your request, we are sending you a link to reset your password. Please follow the link below in your web browser to perform the password reset.

$resetlink 

If you did not initiate the password reset, please disregard this email.

The DocBox Team" 
;
}


sub send_mail{ # send email
		 
	open (MAILH, "|mail -s \"Password Reset Link\" $email") # the '|' lets us print out input to the piped command. Note you should NOT use'-f arugment in sample code, otherwise mail won't be sent!' 
	|| die "cant open mail handle, quitting";
	print MAILH "$msg_body"; # write msg body
	close(MAILH);# send mail.
	 
	
	### Alternate way to send email
	#my $cmd = "echo \" $msg \" | mail -s \"Password Reset\" $email";
	#`$cmd`; # send mail
	#`echo \"$msg\" | mail -s \"Password Reset\" $email`;
}


sub malformed_email{ ## Check if user supplied email is actually a valid email address. 
	
	my $mail = $_[0]; # get email id
	
	if($mail!~/@/){ # check if @ simple missing
		return 1 ; 
	}
	
	my @list = split(/@/, $mail); # split around @ symbol.
	if(int(@list) > 2){ # if email contains more than two @ symbols.
		return 1;
	}
	my $user = $list[0];
	my $domain = $list[1];
	
	if($user !~ /[(\w)\.]*/ ) {# if it does not match word character followed by dot any no. of times, email invalid
		return 1; 	
	}elsif($user =~ /[\`\!\#\@\$\%\^\&\*\(\)\=\+\[\{\]\}\|\:\;\'\"\,\<\>\?\/ ]/){ # if it contains illegal chars
		return 1;
	}
	
	if($domain !~ /[(\w)\.]*/ ) {# if it does not match word character followed by dot any no. of times, email invalid
		return 1; 	
	} elsif($domain =~ /[\`\!\#\@\$\%\^\&\*\(\)\=\+\[\{\]\}\\|\:\;\'\"\,\<\>\?\/ ]/){ # if it contains illegals chars
		return 1;
	}
}

