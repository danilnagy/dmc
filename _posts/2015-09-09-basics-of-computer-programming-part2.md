---
layout: post
title:  The Basics of Computer Programming Part 2: Conditionals and Loops
date:   2015-09-09 04:00:00
tags:
- python
---

Now that we understand variables, we can start to develop more complex code structures which can build more interesting functionality into our scripts. Up to this point, our scripts have been pretty basic, and limit to only executing in a top-down order, with one command or operation per line. The following two concepts, **conditionals** and **loops**, are the two basic 'flow control' structures which can actually alter the sequence in which our code is executed, thereby creating more complex behavior and more interesting functionality. 

## 2. Conditionals

Conditionals are structures within the code which can execute different lines of code based on certain 'conditions' being met. In Python, the most basic type of conditional will test a boolean to see if it is True, and then execute some code if it passes:

```python
b = True

if b:
	print 'b is True'
```

Here, since b is in fact True, it passes the test, causing the code that is inset after the 'if b:' line to execute. Try to run the code again, this time setting b to False to see that nothing happens. In this case, if b does not pass the test, the entire block on inset code after the first conditional line is skipped over and ignored. In Python, a line ending with a ':' followed by inset lines of code is a basic syntex for creating hierarchical structure, and is used with all higher codes structures including conditionals, loops, functions, and objects. The trick is that Python is very particular about how these insets are specified. You have the option of using TABS or a series of spaces, although you cannot mix and match, and you have have to be very explicit about the number of each that you use based on the level of the structure. For instance, this code:

```python
b = False

if b:
	print 'b is True'
	print 'b is False'
```

will skip both print lines if b is False. However, by deleting the indent on the last line, you take that line out of the nested structure, and it will now execute regardless of whether b is True or False:

```python
b = False

if b:
	print 'b is True'
print 'b is False'
```

On the other hand, if you inset the last line one level further:

```python
b = False

if b:
	print 'b is True'
		print 'b is False'
```

You will get an error saying

```
IndentationError: unexpected indent
```

which means that something is wrong with your indenting. In this case you have indented to a level that does not exist in the structure. Such errors are extremely common and can be quite annoying, since they may come either from improper indentation, mixing spaces with TABs or both. On the bright side, this focus on proper indenting enforces a clarity with Python scripts that is often missing in other languages.



## 3. Loops



## 4. Functions

We have already covered some function such as type(), str(), and .append()

## 5. Objects