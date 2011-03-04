#!/usr/bin/perl  

# TestDB
# Test Code to test UserDB module works correctly 
# Tests registeration and user authentication query
# Authors: Jervis
# March 02, 2011
 
use DBI;
use UserDB;

#print "Hello";

#open(FILE, "userpass.sql") || die "\ncant open";

my $u = "TestUser";
my $p = "Test_User_Hashed_Password";
my $em = "testuser\@testdomain.com";
my $fn = "John";
my $mn = "Alex";
my $ln = "Smith";


#my $db = Userpass->new();

#$username, $password, $email, $firstname, $middlename, $lastname


print "Test for Userpass Module\n";

#Test Adding User
print "Adding user...";
UserDB->register($u,$p,$em,$fn,$mn,$ln);
print "\nUser $u added successfuly";

# Test Authentication
print "\nauthenticating user...";

my $valid = UserDB->authenticate($u,"hkjhjk");

print "\nSuccessful Authentication" if($valid);
print "\nAuthentication failure" if(!$valid);