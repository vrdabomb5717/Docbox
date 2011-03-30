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
#use HTML::Template;
use Digest::SHA qw(sha1 sha1_hex sha1_base64); # import SHA1 
use Genstat;
use PublicDB;


my $db = "Files/user/.user.db";
my $filepath = "Files/user/220.jpg";
my $oldpath = "Files/user/110.jpg";
my $averagesize = Genstat->average_size($db);
my $numfiles = Genstat->num_files($db);
#print "The number of files in .user.db before removal is $numfiles.\n";
print "The average size of files .user.db before removal is $averagesize.\n";


removeFile();
removePDF();
removeDoc();
removeRTF();

my $newfiles = Genstat->num_files($db);
print "numfiles is $numfiles and newfiles is $newfiles.\n";

my $removesize = Genstat->average_size($db);
print "The average size of files in .user.db after removal is $removesize.\n";

addfile();

my $addsize = Genstat->average_size($db);

if($addsize != $averagesize)
{
	print "removeFile or addFile is broken.\n";
	print "Alternatively, average_size is broken.\n";
	#exit;
}

my $addnumfiles = Genstat->num_files($db);

if ($addnumfiles != $newfiles + 1 && $addnumfiles != $numfiles)
{
	print "addFile is broken.\n";
	print "Alternatively, num_files is broken.\n";
	#exit;
}


updateFile();

my $fileid = Genstat->getFileID($db, $filepath);
print "The fileid of $filepath is $fileid.\n";
my $testpath = Genstat->getFilePathByID($db, $fileid);
my $testname = Genstat->getFileNameByID($db, $fileid);
print "The filename of $filepath is $testname.\n";

if($filepath ne $testpath)
{
	print "The filepath and testpath are not the same. getFilePathByID is broken.\n";
	#exit;
}

my $public = Genstat->isPublic("$filepath");

if($public != 0)
{
	print "$filepath is public.\n";
	
	#my $publicnum = PublicDB->
	
}
else
{
	print "$filepath is not public.\n";
}

addPDF();
addDoc();
addRTF();

changePublic();

exit; 

#sql2();
exit;

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

my $db = "Files/user/.user.db";
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


sub sql2{
	my $db = "Files/TestUser/.user.db";
$fp= "HTML.pm";
#my $hash_ref_all = Genstat->get_public($db);
my $ary_ref_all = Genstat->top30($db,$fp );

foreach my $arr_ref (@$ary_ref_all){
	my @array = @$arr_ref; # deference
	my $word = $array[0];
	my $count = $array[1];
	print "$word - $count \n";
}
exit;
#foreach $row (keys %$hash_ref_all){
#	 my $row_hash_ref = $hash_ref_all->{$row}; # deref hash reference
#	 
#	 foreach $col (keys %$row_hash_ref){
#	 	print "$col => $row_hash_ref->{$col}\n";	
#	 }
#	 print "===================================\n"; 
#}

 
}


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

sub removeFile
{
	#my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/220.jpg";
	#$filepath = "passwords.txt"; 
	#$filepath = "HTML.pm";
	my $fn = "220.jpg";
	my $comments = " I have no commnets at this time";
	my $tags = " THis is to be tage dlater on"; 
	
	print "Running remove file command ... \n"; 
	Genstat->removeFile($db, $filepath, $fn);
}

sub removePDF
{
	#my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/About Stacks.pdf";
	my $fn = "About Stacks.pdf";
	
	print "Running remove PDF command ... \n"; 
	Genstat->removeFile($db, $filepath, $fn);
}

sub removeDoc
{
	#my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/Halo 2.doc";
	my $fn = "Halo 2.doc";
	my $comments = "Halo 2 random document";
	my $tags = "Halo fun gaming"; 
	
	print "Running remove Doc command ... \n"; 
	Genstat->removeFile($db, $filepath, $fn);
}

sub removeRTF
{
	#my ($self, $filepath, $filename, $public, $comments, $tags) = @_;
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/Source Code License.rtf";
	my $fn = "Source Code License.rtf";
	my $comments = "random file lying around on my hard drive";
	my $tags = "cs code license"; 
	
	print "Running remove RTF command ... \n"; 
	Genstat->removeFile($db, $filepath, $fn);
}

sub changePublic
{
	#doc is initially private, pdf and rtf are initially public
	my $db = "Files/user/.user.db";
	my $pdf = "Files/user/About Stacks.pdf";
	my $doc = "Files/user/Halo 2.doc";
	my $rtf = "Files/user/Source Code License.rtf";
	
	my $numfiles = PublicDB->num_files();
	print "The number of public files before changePublic is $numfiles.\n";	
	
	Genstat->makePrivate($dbfile, $pdf);
	Genstat->makePublic($dbfile, $doc);
	Genstat->makePrivate($dbfile, $rtf);
	
	$numfiles = PublicDB->num_files();
	
	print "The number of public files is now $numfiles.\n";	
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
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/110.jpg";
	#$filepath = "passwords.txt"; 
	#$filepath = "HTML.pm";
	my $fn = "110.jpg";
	my $comments = " I have no commnets at this time";
	my $tags = " THis is to be tage dlater on"; 
	
	print "Running addfile command ... \n"; 
	Genstat->addFile($db, $filepath, $fn, "1", $comments, $tags);
	
}

sub addPDF
{
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/About Stacks.pdf";
	my $fn = "About Stacks.pdf";
	my $comments = "Default PDF that came with Mac OSX";
	my $tags = "cs apple tired";
	
	print "Running add PDF command ... \n"; 
	Genstat->addFile($db, $filepath, $fn, "1", $comments, $tags);	
}

sub addDoc
{
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/Halo 2.doc";
	my $fn = "Halo 2.doc";
	my $comments = "Halo 2 random document";
	my $tags = "Halo fun gaming";
	
	print "Running add Doc command ... \n"; 
	Genstat->addFile($db, $filepath, $fn, "0", $comments, $tags);
	
}

sub addRTF
{
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/Source Code License.rtf";
	my $fn = "Source Code License.rtf";
	my $comments = "random file lying around on my hard drive";
	my $tags = "apple code license";
	
	print "Running add RTF command ... \n"; 
	Genstat->addFile($db, $filepath, $fn, "1", $comments, $tags);
	
}

sub updateFile
{
	my $db = "Files/user/.user.db";
	my $filepath = "Files/user/110.jpg";
	my $fn = "110.jpg";
	my $newpath = "Files/user/220.jpg";
	my $newname = "220.jpg";
	
	print "Running updateFile command ... \n"; 
	Genstat->updateFile($db, $filepath, $fn, $newpath, $newname);	
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
