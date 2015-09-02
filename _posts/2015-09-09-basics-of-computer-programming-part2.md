---
layout: post
title:  The Basics of Computer Programming Part 2 - Conditionals and Loops
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

Here, since b is in fact True, it passes the test, causing the code that is inset after the 'if b:' line to execute. Try to run the code again, this time setting b to False to see that nothing happens. In this case, if b does not pass the test, the entire block of inset code after the first conditional line is skipped over and ignored. In this case, 'if b:' is shorthand for 'if b is True:'. If you want to test for Falseness, you would have to write the full 'if b is False:'.

In Python, a line ending with a ':' followed by inset lines of code is a basic syntex for creating hierarchical structure, and is used with all higher codes structures including conditionals, loops, functions, and objects. The trick is that Python is very particular about how these insets are specified. You have the option of using TABS or a series of spaces, although you cannot mix and match, and you have have to be very explicit about the number of each that you use based on the level of the structure. For instance, this code:

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

which means that something is wrong with your indenting. In this case you have indented to a level that does not exist in the code structure. Such errors are extremely common and can be quite annoying, since they may come either from improper indentation, mixing spaces with TABs or both. On the bright side, this focus on proper indenting enforces a visual clarity with Python scripts that is often missing in other languages.

Moving on, if a conditional test does not pass and the first block of code is passed over, it can be caught by an 'else' statment:

```python
b = True

if b:
	print 'b is True'
else:
	print 'b is False'
```

In this case, when b is True the first statement will execute, and when b is False the second statement will execute. Try this code both ways to see.

In addition to using booleans, you can also create conditionals using various comparison operators. For example, a conditional can test the size of a number:

```python
num = 7

if num > 5:
	print 'num is greater than 5'
```

Or the contents of a string:

```python
t = 'this is text'

if t == 'this is text':
	print 'the text matches'
```

In this example I use the double equals '==' operator to check if one thing equals another. This is the standard way to check equality, since the single equals '=' is reserved for assigning values to variables. The most common comparison operators are:

- == (equal)
- != (not equal)
- > (greater than)
- >= (greater than or equal)
- < (less than)
- <= (less than or equal)

You can use the 'elif:' (a concatenation of else and if) statement to chain together conditions to create more complex logics:

```python
num1 = 3
num2 = 7

if num1 > 5:
	print 'num1 is greater than 5'
elif num2 > 5:
	print 'num2 is greater than 5'
else:
	print "they're both too small!"
```

This creates a chain of tests that happen in order. If the first test passes, that block of code is executed, and the rest of the conditional is skipped. If it fails, however, the second test (after the 'elif:') is analyzed, and so on. If none of the tests pass, the code following the else: statement is executed).

Finally, you can also combine multiple tests within a single line by using the 'and' and 'or' keywords:

```python
num1 = 3
num2 = 7

if num1 < 5 and num2 < 5:
	print "they're both too small!"

if num1 < 5 or num2 < 5:
	print "at least one of them is too small!"
```

## 3. Loops

Loops are the second primary type of 'flow control' structure, and they can be used to make code repeat multiply times under specific conditions. The most basic type of loop is one that iterates over each value within a list:

```python
fruits = ['apples', 'oranges', 'bananas']

for fruit in fruits:
	print fruit
```

The 'for *item* in *list*: structure is the basic way to construct loops in Python. It basically runs the inset code within the structure once for each item in the list, each time setting the current item to the variable specified before the 'in'. In this case, it will run the 'print' code three times, once for each fruit in the list. Every time the code is run, the variable 'fruit' is set to a different fruit in the list in order. This is often used to apply a certain kind of analysis or processing to every element within a list.

You can do the same basic kind of iteration on a dictionary using the .keys() function, which will return a list of all the keys in the dictionary, and allow you to iterate over each entry:

```python
dict = {'a': 1, 'b': 2, 'c': 3}

for key in dict.keys():
	print dict[key]
```

If you run this code, you will see that the entries are not returned in the same order that they are typed. This is because dictionaries, unlike lists, do not enforce a specific order. However, iterating through the keys using the .key() function will ensure that you go through each item in the dictionary.

In addition to iterating through every item in a list or dictionary, loops are often used to simply repeat a particular piece of code a specific amount of times. For this, Python's range() function is very useful, which takes in an integer value and returns a list of integers starting at 0, up to but not including that value:

```python
print range(5)
```

Using the range() function, we can set up a basic loop like:

```python
for i in range(5):
	print 'Hello'
```

This will simply run the code inside the loop five times, since in effect we are creating a list of five sequential number, and then iterating over every item in that list. In addition, we are also storing each successive number in the variable 'i', which we can also use within the loop. A common example is to combine both strategies by tying the range() function to the length of a list (using the len() function), and then using the iterating number to get items from that list:

```python
fruits = ['apples', 'oranges', 'bananas']

for i in range(len(fruits)):
	print fruits[i]
```

Although this might seem redundant given the first example, there are times when you want to build a loop that has access to both an item within a list, as well as an iterator which specifies its index. In such cases, you can use a special function called enumerate() which takes in a list and returns both the item and its index:

```python
fruits = ['apples', 'oranges', 'bananas']

for i, fruit in enumerate(fruits):
	print 'the ' + fruit + ' are in position ' + str(i)
```

While the 'for' loop will serve most purposes, there is another kind of loop which will iterate over a piece of code until a certain condition is met:

```python
i = 0

while i < 5:
	print i
	i += 1
```

In this case, the loop will keep going while it's condition is satisfied, and only stop once the variable 'i' obtains a value greater or equal to 5. This type of loop can be useful if you do not know know how long the loop should be run for, or if you want to make the termination criteria somehow dynamic relative to other activities within the script. It requires a bit more setup, however, as the value tested must first be initialized (i = 0), and there has to be code within the loop which changes that value in such a way that it eventually meets the exit criteria. This type of loop is also more dangerous, because it can easily create a situation where the loop can never exit. In theory, such a loop will run indefinitely, although in practice it will most certainly cause Python to crash. The most dangerous kind of loop is also the simplest:

```python
while True:
	print 'infinity'
```

because by definition it has no way to ever terminate. Surprisingly, such a loop does have a common use (which we will encounter later in these tutorials), but you should never write such code unless you absolutely know what you are doing (maybe try it just the once so you can get a sense of its effects). By the way, if you every run into trouble with infinite loops, you can use the shortcut Ctrl+C to force Python to terminate, or go to Run->Restart Kernel... in the Canopy interface to force restart the Python interpreter.

This concludes our basic coverage of the two main types of 'flow control' structures, *conditionals* and *loops*. With these structures you can start to write much more complex scripts, which are not restricted to executing one command per line, and can exhibit different behavior based on changing conditions in the script. In the final tutorial, we will introduce even more flexibility by packaging pieces of code into custom functions and objects so they can be reused throughout the script.