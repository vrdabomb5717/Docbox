Physics Simulator v1.0 readme.txt
Written on April 18, 2010 by Jervis Jerome Muindi.

Send all feedback/comments/problems to jjm2190@columbia.edu
 
WHAT IS Physics Simulator ?
==========================

Phyiscs Simulator is a simple graphical physics simulation program built off Hortstmann's Graph Editor framework. This program lets you see what happens when you connect you connect nodes (you can think of them as balls) to a stretched rubber band.


HOW DO I USE Physics Simulator?
===============================
To run Physics Simulator, compile PhysicsSimulator.java and run this command from the terminal: 'java PhysicsSimulator' without the quotes. If you are running the terminal session remotely via an SSH session, you will need to make sure that the terminal session is X11 Window enabled as this program utilises a Graphical User Interface and does not accept any keyboard input.

Once the Program launches and is running an empty Graphical Display appears with a toolbar at the top. Click on the appropriate Nodes to add them and you can connect the nodes with the line tool. When you are done setting up your node connections, click on the start animation button to see how the nodes will move. 


WHAT ARE THE DIFFERENT NODES SUPPORTED?
========================================

This program has builtin support for the following Nodes:

- A small and light node: this is colored blue and has a fairly small size. 
- A medium size node: this is colored red and has a medium size.
- A large and heavy node : this is colored green and has a large size.
- A rigid node : this is colored black and has a large size just like the heavy node. 

The specialty of the rigid node is that it has infinite mass and so it does not move when the animation is running. 


WHAT DOES THE PROGRAM CONSIST OF?
=================================

The program consists of 17 classes: 

1.  AbstractEdge - A class that supplies convenience implementations for a number of methods in the Edge interface type. It's Part of the Framework. 

2.  AnimateActionListener -  This class represents an an Animation Action Listener. It contains animation logic to simulate how the nodes should move when connected to a stretched rubber band.

3.  Circle Node - A circular node that is filled with a color, has a certain size and mass and it can either be rigid (fixed) or movable.

4.  Edge -  An edge in a graph. It's part of the framework

5.  EnumEditor - A property editor for enumerated types. It's part of the framework

6.  FormLayout - A layout manager that lays out components along a central axis. It's part of the framework

7.  Graph -  A graph consisting of selectable nodes and edges. It's part of the framework

8.  GraphFrame -  This frame shows the toolbar and the graph. It's part of the framework

9.  GraphPanel -  A panel to draw a graph. It's part of the framework

10. LineStyle - This class defines line styles of various shapes. It's part of the framework

11. Node - A node in a graph. It's part of the framework

12. PhysicsSimulator -  A simple physics simulator that simulates the motion of nodes that are connected to stretched rubber bands.

13. PointNode - An inivisible node that is used in the toolbar to draw an edge. It's part of the framework

14. PropertySheet - A component filled with editors for all editable properties of an object. It's part of the framework

15. RubberEdge -  A rubber edge that is shaped like a straight line.

16. SimpleGraph -  A simple graph with round nodes and straight edges. It's part of the framework

17. ToolBar -  A tool bar that contains node and edge prototype icons. It's part of the framework



DESIGN of PhysicsSimualtor :
====================================

For this assignment, I simply built off the framework provided by Hortsmann. The way I did that is creating my own edge called RubberEdge and also making my own nodes by editing the provide CircleNode class. Then, all that was left to do, was to create a AnimationActionListener which performs the correct calculations in terms of how to move the nodes to give a realistic looking physics simulation. 


DOES THIS PROGRAM SUPPORT SAVING / LOADING?
================================================

No and this is intentional: because Hortsmann framework does not fully support saving and loading, I have decided to go ahead disable those features completely. I did this by commenting out section of his code in the GraphFrame class instead of straighout deletion. I chose to do this, so that in the future, when you fix the save/loading feature it will be easy to add this option back - all you have to do is uncomment the code. 


Change the Masses of the Nodes be Changed?
==========================================


Yes, you can manually change the masses of the node to see how that affects the simulation. To change a mass of a node, perform the following steps

	1. Select the Node.
	2. Click on Edit -> Properties
	3. Enter the new desired mass of the node
	4. Click on Okay 


TEST RUNS
=============

I tried out the 3 suggested test cases in the assignment and all of them worked well in my program. 


HANDLING ERRORS:
================================
This program is a GUI program that accepts no user keyboard input besides from Mouse Input. As such, there is little if any possiblity at all that the user can crash the program and there should be no errors encountered when running the program. 


FILES SUBMITTED
=============================

1.  AbstractEdge - A class that supplies convenience implementations for a number of methods in the Edge interface type. It's Part of the Framework. 

2.  AnimateActionListener -  This class represents an an Animation Action Listener. It contains animation logic to simulate how the nodes should move when connected to a stretched rubber band.

3.  Circle Node - A circular node that is filled with a color, has a certain size and mass and it can either be rigid (fixed) or movable.

4.  Edge -  An edge in a graph. It's part of the framework

5.  EnumEditor - A property editor for enumerated types. It's part of the framework

6.  FormLayout - A layout manager that lays out components along a central axis. It's part of the framework

7.  Graph -  A graph consisting of selectable nodes and edges. It's part of the framework

8.  GraphFrame -  This frame shows the toolbar and the graph. It's part of the framework

9.  GraphPanel -  A panel to draw a graph. It's part of the framework

10. LineStyle - This class defines line styles of various shapes. It's part of the framework

11. Node - A node in a graph. It's part of the framework

12. PhysicsSimulator -  A simple physics simulator that simulates the motion of nodes that are connected to stretched rubber bands.

13. PointNode - An inivisible node that is used in the toolbar to draw an edge. It's part of the framework

14. PropertySheet - A component filled with editors for all editable properties of an object. It's part of the framework

15. RubberEdge -  A rubber edge that is shaped like a straight line.

16. SimpleGraph -  A simple graph with round nodes and straight edges. It's part of the framework

17. ToolBar -  A tool bar that contains node and edge prototype icons. It's part of the framework

18.  Object Oriented Programming and Design in Java Assignment 4 - This documents exists in pdf format and contains answers to the written questions of this assignment (Assignment 4).