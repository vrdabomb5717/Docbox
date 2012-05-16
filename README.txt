COMS W3157 Homework 1
Operation: Project Docbox
Authors: Varun Ravishankar and Jervis Muindi
vr2263 and jjm2190

Repository: https://bitbucket.org/vrdabomb5717/docbox
CLIC: http://web3157.cs.columbia.edu/~jjm2190/public/project/
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



**Progress and Project Realization**
We made reasonable progress over the past month. About once a week, we would meet up to discuss potential issues and progress, and would make sure that we kept abreast of whatever the other was doing. However, midterms made sure that progress slowed in the middle and only sped up near launch day. We used Mercurial and Bitbucket as source control, which allowed us to keep our code in sync and have a high turnover for code reviews. Our biggest problem was that we did not test the backend code adequately enough, and so we both spent some time debugging the backend until it worked. This meant that, at the time of writing, the UI does not implement some of the features that were written on the backend, since once code is written to update part of the database, it is easy to write functions that will update the rest of the fields separately as well. For example, we do not have a profile page nor UI to update personal info, nor did we have a way to edit the tags and comments fields.

Overall, project development was not without hitches, but we worked well together and worked quickly and efficiently towards realizing our goal. One of us, however, would rather shoot himself in the foot than work with Perl for websites ever again.

**Security Issues**
Our main security issues are the easiness for spoofing users, since we are not using HTTPS and thus you can just listen in on the server's private communications and get a user's private information. Even worse, without HTTPS, we can just send the URL from one browser and spoof the user without even trying. The backend is not encrypted, which means that if the server is compromised, the attacker can get people's usernames and passwords if they know where to look. The other major issue is the possiblity of SQL injections. Since our backend is so heavily dependent on SQLite databases, SQL injection attacks that modify records or drop tables could have a devastating effect on the site.


**Bugs and Development Issues**
The biggest bug we had was RTF file searching. Normally, such files can be searched by grep on the backend, but for multiword searches, such tricks don't work. This is because RTF files are like HTML files in that they can have control words and escape sequences in them, and thus words that are individually marked can screw grep up. Instead, we used a module to get the RTF's text and then add it to our database, but the first module failed to work properly. We found another module that worked as planned, but CPAN and installing modules on the server caused us to remove this functionality from the site. We also had development issues with getting the server to cooperate when things went wrong, and log errors correctly rather than fail silently with the default error screen.

On the backend, we had problems with the speed of adding files and searching large quantities of them. Adding files is simple, but we keep track of the count of each word in a separate table per file, which must be generated whenever a file is added. Getting the strings for a file is easy, but this can generate hundreds of individual words. We must then do 100s of inserts into the database, slowing everything down. This is also done when a file is renamed, since we used filepath as a UNIQUE key and this cannot be changed after is is added to the db. This means that grouping, copying, and renaming is slow.

Searching is not as fast as we would like either. We call grep -r to search through all of the user's files, which can potentially be slow if there are many files. This could have been sped up by using a database meant for searching text, like Apache Lucene. This database would index file contents, and unless the file changed, optimize the contents for quick searches. However, we cannot count on the files being kept constant, especially in file storage situations, and we did not have time to learn how to make a search engine, so this development idea had to fall to the wayside.

We had problems separating Perl from HTML and CGI, where we had to find a way to write HTML files so that they could be changed easily, rather than having Perl do it. We also had trouble with the UI; anything more than a basic UI seems to require fudging around with either Perl CGI or using advanced CSS and Javascript, more skills than we possess. This means that the UI looks like it was designed by a 5 year old, and look ugly as sin; however, the UI is functional and works.

We had implemented a go up one level directory button but in testing this on CLIC we ran into issue with it displaying properly this specific feature is currently unusuable. However, users can use forward and back buttons of the browsers to get around this issue.

**License**
All source code is licensed under the Simplified BSD license (2-clause BSD). All documentation is licensed under the FreeBSD Documentation License.