---
layout: post
title:  The Basics of Computer Programming Part 1 - Variables
date:   2015-09-09 03:00:00
tags:
- python
---

If you've never written code, or done any computer programming, the whole concept might seem daunting at first. In fact, while advanced software development is without a doubt incredibly complex, programming in general is based on only a few key concepts. If you compare a computer language to a human language, the particular syntax or terms of the language might be related to the proper spelling of words, while the larger concepts are related to the general grammar. By understanding these concepts from the beginning, you will be less intimidated by all of the particular syntax that you do not know. As long as you can express what you want the program to do in general terms, you can always search the internet for examples using the proper syntax. In fact this is how most people learn to code today. Furthermore, while each programming language (of which there are [many](https://en.wikipedia.org/wiki/Programming_language)) has it's own syntax, they almost all follow the same basic principles. Thus, learning these principles will be useful no matter what language you end up using, as we will see when we start to use some JavaScript later in the course.

In separating the basic principles and structure of code from the syntax of a particular language, one useful concept is [pseudocode](https://en.wikipedia.org/wiki/Pseudocode). Pseudocode is the description of a program's basic functionality through natural language, which is translated later to actual syntax. This is useful when you are learning a language to describe features of a program that you do not yet know how to execute. It is also used by experienced programmers to describe a program's rough template or outline, which is then fleshed out by one or more developers in actual code. Pseudocode is often even left in the final code as comments, to provide a quick reference to the code's structure as a reminder to the developer, or to someone who is not as familiar with the code.

Here we come to our first bit of Python syntax, the all-important comment. You specify a comment by starting a line with '#', which tells Python to ignore everything on that line after the '#' symbol. Try typing the following lines code into a new file and executing it with Python:

```python
#this is a comment
print 'this is code' #this is also a comment
```

If you run this code through the interpreter, you can see that it prints out 'this is code' because it executes the line "print 'this is code'". Meanwhile it ignores both comments occurring after the '#' symbol. Although every language denotes them differently, comments are an important part of every programming language, as they allow the developer to add extra information and description to their code which is not strictly related to its execution.

Now that we know the basics, let's dive into the 5 fundamental elements of any computer program:

## 1. Variables

You can think of variables as containers that store some form of data. You can use variables in Python to store pieces of information, and then later recall them when you need them. Variables can be declared and assigned freely in Python, as opposed to other languages where you have to explicitly state the kind of data they will be storing. To assign a value to a variable, use the '=' operator:

```python
a = 2
```

Here, 'a' is the name of my variable, and the number '2' is the data I am assigning it. From here on out, 'a' will be associated with the number '2', until it is assigned another value, or the program ends. Try this code:

```python
a = 2
b = 3
print a + b
```

This should print out the number 5, since 'a' is storing the number '2', and 'b' is storing the number '3'. You can use many other common arithmetic operators in the same way. Some of the most common are:

- + (addition)
- - (subtraction)
- * (multiplication)
- / (division)
- ** (raise to a power)
- % (modulo)

In Python, you can name your variables anything, as long as it starts with a letter, does not contain spaces, and is not a reserved keyword (such as 'print'). In practice, to enhance readability most programmers follow some conventions for naming variables. One common approach is to use 'camel case' to make variables composed of multiple words readable without spaces.

withCamelCaseTheFirstWordIsLowerCaseWhileAllSubsequentWordsAreUpperCase

It is also common to substitute underscores ('_') for spaces in variable names. In general, variable names should not be too long, but should err on the side of description rather than brevity to facilitate the code's readability. For instance, if you are keeping track of the number of blueberries, it is better to call the variable 'numBlueberries' than simply 'n' or 'b'. 

Variables can hold data of different types. Although Python does not make you explicitly declare the type of data you will be using, it is important to know the types because they will each behave differently in your code. Although there are many different types of data supported by Python, the most common are:

- int (means integer, or a whole number)
- float (means floating point, or decimal number)
- bool (means boolean, or a True/False)
- str (means string, or 'a piece of text')

In Python you can use the type() function to get the type for any piece of data. Try to run the following code:

```python
print type(12)
print type(12.1)
print type(True)
print type('blueberries')
```

you can see that it prints the four types described above. Notice also the particular way in which the data must be written so that Python does not confuse it with the name of a variable. Number can be written directly because you cannot name variables with only a number. Booleans must be written capitalized (True or False) as these are reserved key words in Python (notice the syntax coloring). Strings are always contained within quotes. You can use single (') or double (") quotes, but they must match on either side of the string. If you try to write

```python
print type(blueberries)
```

without the quotes, you will get the following error:

```
NameError: name 'blueberries' is not defined 
```

telling you that the name 'blueberries' is not defined as a variable. However, if you write

```python
blueberries = 5
print type(blueberries)
```

it will tell you it's an int because 'blueberries' is now a variable with an int stored inside of it.

In Python, many operators are 'over-loaded', which means that they function differently depending on the data structure that they are used on. For instance, if we type

```python
print 2 + 2
```

we get '4'. When given two numbers, the '+' operator performs arithmetic addition. However, if we type

```python
print 'First ' + 'Last'
```

we get 'First Last'. When given two strings, the '+' operator 'concatenates' or merges them together into one string. Over-loading is useful because it produces clean and readable code without having a special function for each type of variable. You have to be careful, however, because mismatching different types of variable can lead to errors. For instance, this line

```python
numBerries = 5
print 'Number of Blueberries: ' + numBerries
```

will produce an error because it is trying to perform a concatenation of a string and an integer. Instead, you can use the int() function to convert the 5 to a string before using it with the '+' operator.

```python
numBerries = 5
print 'Number of Blueberries: ' + str(numBerries)
```

### Multi-part variables

In addition to storing single pieces of data, you can also use variables to store many pieces of data, and then access them in a structured way. There are two basic types of multi-part variables:

- lists (also called arrays) and
- dictionaries (also called key-value pairs)

A list can be created by using square brackets, and separating individual elements by commas like so:

```python
numbers = [1, 2, 3, 4, 5]
fruits = ['apples', 'oranges', 'bananas']
```

To retrieve an object from such a list, you once again use square brackets, but this time appended to the end of the variable name. Inside the brackets you place the index or place of the piece of data you want. For instance:

```python
numbers = [1, 2, 3, 4, 5]
print numbers[0]

fruits = ['apples', 'oranges', 'bananas']
print fruits[1]
```

Notice that like in all languages, counting begins with '0', so if you want the first item in a list you use [0], the second item [1], and so on. Unlike many other languages, Python will allow you to mix different types of data within a single list, so something like this is perfectly legal:

```python
fruitsAndNumbers = ['apples', 2, 'bananas']
print type(fruitsAndNumbers)
print type(fruitsAndNumbers[0])
print type(fruitsAndNumbers[1])
```

You can also use a ':' within the square brackets to obtain a range of values from a list, which will form a new list:

```python
numbers = [1, 2, 3, 4, 5]
newNumbers = numbers[0:3] # [index of first item:index after last item]
print newNumbers
```

You can even index backwards using negative indices. For instance, this will print out the last item in the list:

```python
numbers = [1, 2, 3, 4, 5]
print numbers[-1]
```

Various functions exist to help you work with lists. The most common is .append(), which adds a value to the end of a list:

```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
print numbers
```

You can even start with an empty list, and fill it gradually with appends:

```python
numbers = []
numbers.append(1)
numbers.append(2)
print numbers
```

For other list functions you can refer to the [Python documentation](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists).

Lists are extremely useful for storing multiple pieces of data within a specifc sequence. However, sometimes you want to be able to recall a piece of data without knowing its exact position in a list. For this you can use dictionaries. Dictionaries store multiple pieces of data by tying them to unique keys. You can then use the keys to recall the data. For this reason, dictionaries are often called *key-value pairs*.

To create a dictionary, you use curly braces, separating keys and values with ':', and multiple entries with ',':

```python
dict = {'a': 1, 'b': 2, 'c': 3}
```

In this dictionary, the integers 1, 2, and 3 are tied to their unique keys, 'a', 'b', and 'c'. Note that keys must be strings, while values can be any data type. To retrieve a piece of data from this dictionary, I can again use the square bracket notation, this time passing in a key instead of an index:

```python
dict = {'a': 1, 'b': 2, 'c': 3}
print dict['a']
```

To add entries to a dictionary, you just have to specify the data that relates to a particular key using the same square bracket syntax:

```python
dict = {'a': 1, 'b': 2, 'c': 3}
dict['d'] = 4
print dict['d']
```

As with lists, you can start with an empty dictionary and build it up over time:

```python
dict = {}
dict['a'] = 1
dict['b'] = 2
print dict
```

There are also many useful functions for working with dictionaries, including the .keys() function which returns a list of all of the dictionary's keys:

```python
dict = {'a': 1, 'b': 2, 'c': 3}
print dict.keys()
```

For other useful functions you can refer to the proper place in [the documentation](https://docs.python.org/2/tutorial/datastructures.html#dictionaries).

Finally, values within lists and dictionaries are not restricted to being single pieces of data either, and can be lists and dictionaries as well. This allows you to build highly sophisticated data structures that match the needs of any project. You can access items within such a hierarchical structure by chaining together requests with square brackets. Here is an example:

```python
dict = {}

dict['numbers'] = [1, 2, 3, 4, 5]
dict['fruits'] = ['apples', 'oranges', 'bananas']

dict['numbers'].append(6)
dict['fruits'].append({'berries':['strawberries', 'blueberries']})

#compound request, should print 'blueberries'
print dict['fruits'][-1]['berries'][1]
```

JSON, one of the most wide spread and easiest to work with data formats is actually based on this concept of nested lists and dictionaries, and has great support within almost every programming language, including Python and JavaScript. We will start to implement it later in the course, but for now you can check out its documentation here: [http://json.org/](http://json.org/).