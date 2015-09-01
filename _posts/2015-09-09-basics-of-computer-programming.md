---
layout: post
title:  The Basics of Computer Programming
date:   2015-09-09 03:00:00
tags:
- python
---

If you've never written code, or done any computer programming, the whole concept might seem daunting at first. In fact, while advanced software development is without a doubt incredibly complex, programming in general is based on only a few key concepts. If you compare a computer language to a human language, the particular syntax or terms of the language might be related to the proper spelling of words, while the larger concepts are related to the general grammar. By understanding these concepts from the beginning, you will be less intimidated by all of the particular syntax that you do not know. As long as you can express what you want the program to do in general terms, you can always search the internet for examples using the proper syntax. In fact this is how most people learn to code today. Furthermore, while each programming language (of which there are [many](https://en.wikipedia.org/wiki/Programming_language)) has it's own syntax, they almost all follow the same basic principles. Thus, learning these principles will be useful no matter what language you end up using, as we will see when we start to use some JavaScript later in the course.

In separating the basic principles and structure of code from the syntax of a particular language, one useful concept is [pseudocode](https://en.wikipedia.org/wiki/Pseudocode). Pseudocode is the description of a program's basic functionality through natural language, which is translated later to actual syntax. This is useful when you are learning a language to describe features of a program that you do not yet know how to execute. It is also used by experienced programmers to describe a program's rough template or outline, which is then fleshed out by one or more developers in actual code. Pseudocode is often even left in the final code as comments, to provide a quick reference to the code's structure as a reminder to the developer, or to someone who is not as familiar with the code.

Here we come to our first bit of Python syntax, the all important comment. You specify a comment by starting a line with '#', which tells Python to ignore everything on that line after the '#' symbol. Try typing the following lines code into a new file and executing it with Python:

```python
#this is a comment
print 'this is code' #this is also a comment
```

If you run this code through the interpreter, you can see that it prints out 'this is code' because it executes the line "print 'this is code'". Meanwhile it ignores both comments occuring after the '#' symbol. Although every language denotes them differently, comments are an important part of every programming language, as they allow the developer to add extra information and description to their code which is not strictly related to its execution.

Now that we know the basics, let's dive into the 5 fundamental elements of any computer program:

### 1. Variables

You can think of variables as containers that store some form of data. You can use variables in Python to store pieces of information, and then later recall them when you need them. Variables can be declared and assigned freely in Python, as opposed to other languages where you have to explicitly state the kind of data they will be storing. To assign a value to a variable, use the '=' operator:

```python
a = 2
```

Here, 'a' is the name of my variable, and the number '2' is the data I am assigning it. From here on out, 'a' will be associated with the number '2', until it is assigned another value, or the program ends. Try this code:

```python
a = 1
b = 2
print a + b
```

This should print out the number 3, since 'a' is storing the number '1', and 'b' is storing the number '2'. You can use many other common arithmetic operators in the same way. Some of the most common are:

- + 	addition
- - 	subtraction
- * 	multiplication
- / 	division
- ** 	raise to a power
- % 	modulo

In Python, you can name your variables anything, as long as it starts with a letter, does not contain spaces, and is not a reserved keyword (such as 'print'). In practice, to enhance readability most programmers follow some conventions for naming variables. One common approach is to use 'camel case' to make variables composed of multiple words readable without spaces.

withCamelCaseTheFirstWordIsLowerCaseWhileAllSubsequentWordsAreUpperCase

It is also common to substitute underscores ('_') for spaces in variable names. In general, variable names should not be too long, but should err on the side of decription rather than brevity to facilitate the code's readability. For instance, if you are keeping track of the number of blueberries, it is better to call the variable 'numBlueberries' than simply 'n' or 'b'. 



### 2. Conditionals



### 3. Loops



### 4. Functions



### 5. Objects