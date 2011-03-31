COMS W3157 Homework 1
Operation: Project Docbox
Authors: Varun Ravishankar and Jervis Muindi
vr2263 and jjm2190


**Files included:**

*.project*
Nonessential, contains listing of files for editing.

*Files/*
Directory contains files uploaded by users.

*Filesearch.pm*
Perl module

*Genstat.pm*
A module that contains methods to add files, remove files, update files, and generate statistics based upon the user's database, such as the number of files, the average file size, the top 30 words, change the public status of a file, search the tags/comments/filetype/filename/size, generate the word counts of words in a file, and find out if a file is public.

*HTML.pm*
Contains static methods for generating commonly used HTML code specific to DocBox.

*Log.pm*
Logs messages to the server, like logins, failed logins, errors, and all other important events on the server.

*Logs/*
Folder that contains the log files.

*Project Desc*
Division of responsibilities in project.

*PublicDB.pm*
Contains static methods for accessing Public file SQLite database; similar in function to Genstat, but specific to the public database.

*TestDB.pl*
Test Code to test UserDB module works correctly, by removing, adding, and updating text files, Word docs, PDFs, and RTFs.

*Test_HTML.pl.cgi*
Testing script for HTML::Template.

*ToDoList.txt*
List of things still to do. Has not been updated in a while, so it should not be believed.

*UserDB.pm*
List of methods for accessing and modifying the user registration database, including registering a user, changing password, and changing personal info.

*clip_image002.png*
Random image that is apparently our site's logo.

*css/*
Directory that contains the CSS files for the website.

*database schema*
Basic schema for the SQL databases we created.

*download.pl.cgi*
Downloads the given file to the user's browser. 

*editfile.pl.cgi*
Edit file, allowing user to copy, delete, rename, and download.

*email.pl.cgi*
Emails user a password reset link.  

*filelist.html*
HTML page that is displayed to test the file listing.

*group.pl.cgi*
Groups the user selected file into its own directory.

*home.pl.cgi*
Lists all files currently owned by the user.

*images/*
Contains images used on the website for all operations.

*index.html*
Main landing page for website.

*login.pl.cgi*
Page that is displayed for user to log in on.

*login_failed.html*
Page that is displayed when a user fails to authenticate against userpass.db

*passwords.txt*
Test file for storing a user and their password, used on an older revision of the site.

*public.db*
Contains a listing of all public files on the server.

*public.pl.cgi*
Shows all available public files.

*register.pl.cgi*
Registers new user and adds to the database.

*reset.pl.cgi*
Resets the password of a user.

*reset_page.pl.cgi*
Gives HTML page to perform password reset.

*search.pl.cgi*
Performs a search to which files match given query.

*searchtest.pl*


*stats.pl.cgi*
Shows statistics about the users' files and about the website in general, like number of files, users, and average file size.

*temp.tar*
Temporary file created to enable directory downloading.

*templates/*
Contains HTMl template files used on the website.

*upload.pl.cgi*
Uploads current file and saves it in the users' home directory.

*upload_page.pl.cgi*
Generates HTML to let user upload file to the server.

*user.db*
Test db that contains a listing of users' files, and the files' properties, as well as word counts for each file.

*user.sql*
Contains the SQL schema for the .user.db file that is created for each user.

*userpass.db*
Database that contains a list of users, their passwords, and users' personal information.

*userpass.sql*
Database SQL schema file for the userpass.db, which is used to create a new database if we migrate the site.


**./Files:**

*test/*
*user/*

These two directories are separate users, to help test our code.


**./Files/test:**

*.user.db*
*about_Arithmetic_Operators.help.txt*
*pub/*
*t1/*

This user has their user database, a text file, and two subdirectories.


**./Files/test/pub:**

*pub3.txt*
*public-copy.txt*
*public.txt*

Three text files in this subdirectory.


**./Files/test/t1:**

*hosts*

Another text file, without an extension.



**./Files/user:**

*.user.db*
*110.jpg*
*About Stacks.pdf*
*Columbia Internet Download Speed FATEST.png*
*Halo 2.doc*
*Source Code License.rtf*
*Untitled.rtf*
*sample midterm.pdf*
*test/*
*testfile.txt*
*works.txt*

The second user has their database, a jpeg file, 2 PDFs, a PNG, a Word document, 2 RTF files, 2 text files, and a subdirectory called test.


**./Files/user/test:**

*111.jpg*
*testfile.txt*
*works.txt*

A jpeg and two text files are in this subdirectory.


**./Logs:**

*errors.txt*
*log.txt*
*logins.txt*

Log files for the server. log.txt is a log of all events on the server, errors.txt is a log of all errors that occur on the server, and logins.txt is a log of all successful and attempted logins on the server.


**./css:**

*main.css*

CSS file for the website.


**./images:**

*copy.png*
*delete.png*
*dir.png*
*download.png*
*email.png*
*file.png*
*public.png*
*rename.png*
*stat.png*
*up.png*

Images that appear during any operation on the website.


**./templates:**

*editfile.tmpl*
*filelist.tmpl*
*fileop.tmpl*
*group.tmpl*
*group_op.tmpl*
*public.tmpl*
*reset.tmpl*
*search.tmpl*
*stats.tmpl*
*success.tmpl*
*upload.tmpl*

Template HTMl pages for all the pages that appear on the website.




