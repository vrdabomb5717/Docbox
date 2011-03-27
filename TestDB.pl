#!/usr/bin/perl  

# TestDB
# Test Code to test UserDB module works correctly 
# Tests registeration and user authentication query
# Authors: Jervis
# March 02, 2011
 
BEGIN{
	unshift(@INC, "/home/jjm2190/perl5/lib/perl5"); #Load Locally installed modules. Needed for site to function in CLIC. Don't use lib - it doesn't work. 
} 
 
use DBI;
use UserDB;
use HTML::Template;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use Genstat; 

#print "Hello";

#open(FILE, "userpass.sql") || die "\ncant open";

my $u = "TestUser";
my $p = "Test_User_Hashed_Password";
my $em = "testuser\@testdomain.com";
my $fn = "John";
my $mn = "Alex";
my $ln = "Smith";

my $t = Genstat->num_files("Files/TestUser/.user.db");
print "USER TABLE HAS $t FILES";
exit; 

#my $db = Userpass->new();

#$username, $password, $email, $firstname, $middlename, $lastname

print "Test for Userpass Module\n";
#word();
#makedb();

#my @splitted = split(' ', $y);
#print @splitted;
#print"\n length is" . int(@splitted);

#print w($y);

my $db = "Files/TestUser/.user.db";
$fp= "HTML.pm";
#my $hash_ref_all = Genstat->get_public($db);
#my $hash_ref_all = Genstat->top30($db,$fp );



#my $result = Genstat->isPublic("HTML.pm");
#if($result){
#	print "FILE PUBLIC ";
	#exit;
#}else{
#	print "FILE PRIVATE";
	#exit;
#}

#print "avg size is \n";
#print Genstat->average_size($db); 


my @l = split(/\//, "Files/username/.user.db");
print @l;  

#makedb();
exit;
#addfile();
#removeFile();

sub sql{
	my $db = "Files/TestUser/.user.db";
$fp= "HTML.pm";
#my $hash_ref_all = Genstat->get_public($db);
#my $hash_ref_all = Genstat->top30($db,$fp );

#foreach $row (keys %$hash_ref_all){
#	 my $row_hash_ref = $hash_ref_all->{$row}; # deref hash reference
#	 
#	 foreach $col (keys %$row_hash_ref){
#	 	print "$col => $row_hash_ref->{$col}\n";	
#	 }
#	 print "===================================\n"; 
#}

while( my ($id, $row_hash_ref) =  each(%$hash_ref_all)){
	 #my $row_hash_ref = $hash_ref_all->{$row}; # deref hash reference
	 
	 #print $row_hash_ref; 
	 foreach $col (keys %$row_hash_ref){
	 	print "$col => $row_hash_ref->{$col}\n";	
	 }
	 print "===================================\n"; 
}
	
}

sub removeFile{
	#my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	my $db = "Files/TestUser/.user.db";
	my $filepath = "Files/user/110.jpg";
	$filepath = "passwords.txt"; 
	$filepath = "HTML.pm";
	my $fn = "110.jpg";
	my $comments = " I have no commnets at this time";
	my $tags = " THis is to be tage dlater on"; 
	
	print "Running REMOVE file command ... \n"; 
	Genstat->removeFile($db, $filepath, $fn);
	
}

sub w{
	my $input = $_[0]; 
	
	my @output; 
	my %word_list; #hash table to store words
	$input = lc($input); #convert to lowercase
	my @words = split(/\W+/, $input); # get all words
	foreach my $word (@words){
		$word_list{$word}++; # store word and increment count. 
	}
	
	my @sorted_list = sort{$word_list{$b} <=> $word_list{$a}} keys %word_list; #sort hash table on key value counts in descending order
	
	my $count; 
	foreach my $word(@sorted_list){
		$count = $word_list{$word}; # get word count 
		push(@output, "$word $count\n");
	}
	return @output;
	
}

sub word{
	$filepath = "Project Desc";
	my $words = `"cat $filepath | perl -ne 'print join("\n", split(/\\W+/, $_))' | sort | uniq -c | sort -nr"`;
	    my @splitted = split(/'\n'/, $words);

	    foreach my $line(@splitted)
	    {
	    my @counts = split($line);	
		print "line is $line : counts are ";
		print "$counts[1] and $counts[0] \n";
		
		
		#$sth->execute($counts[1], $counts[0]);
	    }
}

sub read{
	#my @files = <Files/user/*>;
	#print @files;
	
	my $dir = "./Files/user";
	opendir(my $dh, $dir); 
	
	
	#my @dir =  readdir($dh); 
	#my $d =  readdir($dh);
	#print $d; 
	while(defined(my $aFile = readdir $dh)){
		if(-f "$dir/$aFile"){
			print scalar($aFile);
			#print $aFile;
			print "\n";
		} 
	}
	#print @dir;
}

 

sub addfile{
	#my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	my $db = "Files/TestUser/.user.db";
	my $filepath = "Files/user/110.jpg";
	$filepath = "passwords.txt"; 
	$filepath = "HTML.pm";
	my $fn = "110.jpg";
	my $comments = " I have no commnets at this time";
	my $tags = " THis is to be tage dlater on"; 
	
	print "Running addfile command ... "; 
	Genstat->addFile($db, $filepath, $fn, "1", $comments, $tags);
	
}

sub makedb{
	print "making db ...\n";
	#mkdir "./files/$u";
	
	
	`sqlite3 public.db "CREATE TABLE files ( id INTEGER PRIMARY KEY,
                        filepath TEXT NOT NULL COLLATE NOCASE,
                        filename TEXT NOT NULL,
                        owner TEXT NOT NULL COLLATE NOCASE,
                        timemodified TEXT NOT NULL,
                        timeadded TEXT NOT NULL,
                        size REAL NOT NULL,
                        kind TEXT NOT NULL COLLATE NOCASE,
                        comments TEXT COLLATE NOCASE,
                        tags TEXT COLLATE NOCASE,
                        UNIQUE (filepath) );"`;
	exit;                        
	`sqlite3 ./files/$u/user.db "CREATE TABLE files ( id INTEGER PRIMARY KEY,
                        filepath TEXT NOT NULL COLLATE NOCASE,
                        filename TEXT NOT NULL,
                        public INTEGER NOT NULL,
                        permissions INTEGER NOT NULL,
                        timemodified TEXT NOT NULL,
                        timeadded TEXT NOT NULL,
                        size REAL NOT NULL,
                        kind TEXT NOT NULL COLLATE NOCASE,
                        comments TEXT COLLATE NOCASE,
                        tags TEXT COLLATE NOCASE,
                        UNIQUE (filepath) );"`;
}



#Test Adding User
sub adduser{
print "Adding user...";
UserDB->register($u,$p,$em,$fn,$mn,$ln);
print "\nUser $u added successfuly";
}

# Test Authentication
sub authenticate{
print "\nauthenticating user...";
my $valid = UserDB->authenticate($u,"hkjhjk");
print "\nSuccessful Authentication" if($valid);
print "\nAuthentication failure" if(!$valid);
}

# Test Email checking
sub checkemail{
print "checking user email id...";
my $email = "jjm2190\@columbia.edu";
my $valid2 = UserDB->validEmailAndName($email,"Jervis","Muindi");

print "\nSuccessful Valid email and name\n" if($valid2);
print "\nEmail / name not Valid\n" if(!$valid2);
}

# Test User ID retrieval
sub getuser{
my $passhex = sha1_hex("user"."user");
my $result = UserDB->getUser($passhex);
print "Output of Username for given ID is below\n".$result;
}