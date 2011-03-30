#!/usr/bin/perl

# Log
# Logs events to a log file
# Authors: Jervis
# 26th March 2011

#Note: First argument in a static method call in perl is always the class name. This is what $self refers to. 

package Log;
use warnings; 
use Fcntl ':flock'; # handle file  i/o

sub log {
	my($self, $event) = @_; 
	
	open (FILE, ">>Logs/log.txt"); # Open file for appending. Note this will create the file if it does not exist already. 
	flock(FILE, LOCK_EX); # get file lock handle  
	{ 
		print (FILE "$event\n"); #Append to login file	
	}
	close FILE; # save changes
}

# log registrations
sub logReg{
	my($self, $event) = @_; 
	
	open (FILE, ">>Logs/registration.txt"); # Open file for appending. Note this will create the file if it does not exist already. 
	flock(FILE, LOCK_EX); # get file lock handle  
	{ 
		print (FILE "$event\n"); #Append to login file	
	}
	close FILE; # save changes
		
}

# log DB errors
sub Error{
	my($self, $event) = @_; 
	
	open (FILE, ">>Logs/errors.txt"); # Open file for appending. Note this will create the file if it does not exist already. 
	flock(FILE, LOCK_EX); # get file lock handle  
	{ 
		print (FILE "$event\n"); #Append to login file	
	}
	close FILE; # save changes
		
}



1;