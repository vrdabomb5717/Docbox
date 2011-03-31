Battleship v1.0 readme.txt
Written on February 17, 2010 by Jervis Muindi.

Send all feedback/comments/problems to jjm2190@columbia.edu
 
WHAT IS BARCODECONVERTER ?
==========================

Battleship is a simple java program that lets you play the popular battleship game against a computer opponent.
	

HOW DO I USE BARCODECONVERTER?
===============================
To run BarcodeConverter, compile Battleship.java and  run this command from the terminal: 'java Battleship' without the quotes. 

Upon first run, the program will ask you to enter the coordinates of your ship. You should use the following format: (x,y,z) where x and y are x and y coordinates respectively and z is a standin for the letter v or h with v representing vertical and h horizontal. For example, to add a ship at (0,0) vertical, you would enter (0,0,v). If you wanted it horizontally the command would be (0,0,h)

The synmbols used in the grid display as follows:
 - X which represents a hit
 - O which represents a miss.

The other part of the program are self-explanatory and on screen directions should be followed.


WHAT DOES THE PROGRAM CONSIST OF?
=================================

The program consists of 6 classes: 
1. Battleboard - 

2. Computer - This class represents a computer player of the game Battleship.

3. Human - This class represents a human player of the game Battleship.

4. Game Engine - This class represents the game engine of the Battleship game.

5. Vessel - This class represents a naval vessel such as a submarine or aircraft carrier.

6. Battleship - This class contain the main methods that runs the battleship game.


CHECKING USER INPUT:
================================
I have added code to check that for errors in user input and so the program will prompt you to try again you enter an incorrect or invalid input. This code is robust enough that wrong or erronoues input won't cause the program to crash.



OTHER FILES SUBMITTED
=============================
Computer Science Assignment 1 - FINAL. This contains the written portion of the assignment except for Part 3 which is submitted on paper. This documents exists in both pdf and docx formats.

