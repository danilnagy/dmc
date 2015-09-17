---
layout: post
title:  The Basics of Computer Programming Part 3 - Functions and Objects
date:   2015-09-09 05:00:00
tags:
- python
---

So far, we have seen how we can use *variables* in Python to store different kinds of data, and how we can use 'flow control' structures such as *conditionals* and *loops* to change the order or the way in which lines of code get executed. With only these tools we can already start to express some pretty complex logics. However, with only our current tools, any sufficiently complex script would start to get very long, since every time we wanted to do a certain process we would have to rewrite all of its code. This is where *functions* and *classes* come in. Functions allow us to encapsulate lines of code to create custom processes that can be reused anywhere throughout the script. Objects take this encapsulation one step further and wrap up not only a single process, but several related processes, as well as local variables that can keep track of that object's status.

## 4. Functions

We have already seen and used some functions such as type(), str(), .append(), .keys(), and range(). But what are functions really?

As in math, a function is a basic structure that can accept inputs, perform some processing on those inputs, and give back a result. Let's create a basic function that will add two to a given number and give us back the result:

```python
def addFunction(inputNumber):
	result = inputNumber + 2
	return result
```

On its own, this code will only define what the function does, but will not actually run any code. To execute the code inside the function you have to *call* it somewhere within the script and pass it the proper inputs:

```python
print addFunction(2)
```

A function's definition begins with the keyword 'def'. After this is the function's name, which follows the same naming conventions as variables. Inside the parenthesis after the function name you can place any number of input variables, which will be passed to the function when it is called, and are available within the body of the function. When you call a function, you can either directly pass values or pass variables that have values stored inside of them. For example, this code will call the function in the same way:

```python
var = 2
print addFunction(var)
```

Here the value of the 'var' variable, which in this case is 2, is being passed to the 'addFunction' function, and is then available within that function through the 'inputNumber' variable. Notice that the names of the two variables 'var' and inputNumber' don't have to match. When a value gets passed to a function it forms a direct connection between the two sets of parenthesis which carries the data. In this case 'var' is a *global variable* that stores the value '2' in the main script, while 'inputNumber' is a *local variable* which stores that value only for the duration of that function. In this way functions 'wrap up' specific tasks and all the data that is necessary to execute that task to limit the number of global variables necessary in the main function.

The first line declaring the function and its inputs ends with a colon, which should be familiar by now, with the rest of the function body inset from the first line. Optionally, if you want to return a value from the function back to the main script, you can end the function with the keyword 'return', followed by the value or variable you want to return. Once the function hits on a return statement, it will skip over the rest of the body and return the associated value. This can be used to create more complex behavior within the function:

```python
def addFunction(inputNumber):
	if inputNumber < 0:
		return 'Number must be positive!'
	result = inputNumber + 2
	return result

print addFunction(-2)
print addFunction(2)
```

You can see that in this case, if the input is less than zero the conditional will be met, which causes the first return statement to run, skipping the rest of the code in the function.

You can pass any number of inputs into a function, but the number of inputs must always match between what is defined in the function, and what is passed into it when the function is called. For example, we can expand our simple addition function to accept two numbers to be added:

```python
def addTwoNumbers(inputNumber1, inputNumber2):
	result = inputNumber1 + inputNumber2
	return result

print addTwoNumbers(2, 3)
```

You can also return multiple values by building them into a list, and then extracting them from the returned list. Let's expand our function to return both the addition and multiplication of two numbers

```python
def twoNumbers(inputNumber1, inputNumber2):
	addition = inputNumber1 + inputNumber2
	multiplication = inputNumber1 * inputNumber2
	return [addition, multiplication]

result = twoNumbers(2, 3)
print 'addition: ' + str(result[0])
print 'multiplication: ' + str(result[1])
```

These kinds of functions are extremely useful for creating efficient and readable code. By wrapping up certain functionalities into custom modules, they allow you (and possibly others) to reuse code in a very efficient way, and also force you to be explicit about the various sets of operations happening in your code. You can see that the basic definition of functions is quite simple, however you can quickly start to define more advanced logics, where functions call each other and pass around inputs and returns in highly complex ways (you can even pass a function as an input into another function, which we will see later in these tutorials). This kind of programming, which uses functions to encapsulate discrete logics in a program is called **functional programming**.



## 5. Classes

A step beyond functional programming is [object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming) or OOP. In OOP, programs are defined not as a list of procedures to be executed one at a time, but as a collection of interacting objects. In the traditional procedural approach, a program is executed and finishes once all the procedures are run. With OOP, the program is running continuously, with objects interacting and triggering different behaviors based on events occurring in real time.

Although we will not get too deep into OOP within the confines of this course, many of the technologies we build on will be inherently based on OOP. So it is important to at least get familiar with what objects are, and how we can use them in a very basic sense. An object in Python is called a **class**, but the two words are often used interchangeably. You can think of a class as a structure that encapsulates a set of related functions (functions belonging to specific objects are often called that object's 'methods') with a set of local variables that keep track of that class' state. Together, these variables and methods define the 'behavior' of the object, and dictate how it interacts with other objects in the programming 'environment'.

Let's think about this in everyday terms. For an animal, an example of a method might be 'running'. Lots of things can run, so the definition of running as a function would be general, and would not necessarily relate to who is doing the running. On the other hand, an example of a class might be 'dog', which would have an instance of the 'running' method, as well as other methods related to being a dog such as 'eating' and 'barking'. It would also have a set of variable for storing information about a given dog, such as its age, breed or weight. Another class might be 'human', which would store different variables, and would have it's own particular version of methods such as 'running' and 'eating' (but hopefully not 'barking').

Let's define a very basic class to see how it works. We will use an example of a counter, which will store a value, and increment that value based on user requests:

```python
class CounterClass:
	
	count = 0

	def addToCounter(self, inputValue):
		self.count += inputValue

	def getCount(self):
		return self.count
```

Notice we are again using the '+=' shorthand to increment the value of the object's count variable by the input value. To use this class, we first need to create an instance of it, which we will store in a variable just like any other piece of data:

```python
myCounter = CounterClass()
```

Once we create an instance of a class (called 'instantiation'), we can run that instance's methods, and query it's variables. Note that the general class definition is only a construct. All variables within the class only apply to a particular instance, and the methods can only be run as they relate to that instance. For example:

```python
myCounter.addToCounter(2)
print myCounter.getCount()
```

Right away, you will notice a few differences between how we define functions and classes. First of all, no variables are passed on the first line of the definition since the 'class' keyword only defines the overall structure of the class. After the first line you will find a list of variables that are the local variables of that class, and keep track of data for individual instances. After this you will have a collection of local methods (remember 'methods' are simply functions that belong to a particular class) that define the class functionality. These methods are defined the same way as before, except you see that the first input is always the keyword 'self'. This represents the object instance, and is always passed as the first input into each method in a class. This allows you to query the local variables of the instance, as you can see us doing with the 'count' variable.

To call a method within a class, you use the name of the variable that is storing the instance, and use the dot '.' notation to call the method. The dot is basically your way into the instance and all of it's data and functionality. We have seen the dot before, for example when we called the .append() function on a list. This is because a list is actually a class itself! When you define a list you are actually creating an instance of the list class, which inherits all of the functionalities of that class (crazy right?). Actually there is only a small collection of primitive data types in Python (ints, floats, booleans, and a few others), with everything else defined as classes in the OOP framework. Even strings are special classes which store a collection of characters.

By the way, it is also possible to use the '.' syntax to query the local variables of the class instance. For example, if we want to find the value of myCounter's count variable, we can just ask it by typing:

```python
myCounter.count
```

However, this is discouraged because it reveals the true name of the local variables to the end user. In a production environment this would pose severe security risks, but it is considered bad practice even in private uses. Instead, you are encouraged to create special 'accessor' methods to pull variable values from the instance, as we have done with the 'getCount()' method in our example. Another advantage of this practice (which is called [encapsulation](http://beginnersbook.com/2013/05/encapsulation-in-java/)) is that the code is easier to maintain. You are free to make any changes within the class definition, including changing the names of the local variables and what they do. As long as you maintain the accessor functions and they return the expected result, you do not have to update anything in the main code.

As far as naming classes goes, you can follow the same rule as naming variables or functions, however the standard practice is to capitalize every word, including the first one.

Finally, in the example above every instance we make of the CounterClass will start the counter at 0. However, what if we want to specify what this count should be when we make an instance of the class? For this we can implement the `__init__()` method (those are two underscores on each side of 'init'):

```python
class CounterClass:
	
	count = 0

	def __init__(self, inputValue):
		self.count = inputValue

	def addToCounter(self, inputValue):
		self.count += inputValue

	def getCount(self):
		return self.count
```

Now we can create a new instance of the counter, but this time pass in a starting value for the count. 

```python
myNewCounter = CounterClass(10)
myNewCounter.addToCounter(2)

#this should now return 12
print myNewCounter.getCount()
```

When the class instance is initialized, it will automatically run the `__init__()` method, which will utilize any variable passed into it during initialization. Notice how we still have to initialize the local variable with a value in the class definition, which is then replaced during the `__init__()` method. `__init__()` is one of a series of special methods that classes can implement to achieve different functionality. The rest of these are beyond the scope of this class, but you can find a more thorough description of these, as well as other aspects of classes, in the [Python documentation](https://docs.python.org/2/tutorial/classes.html).

This concludes our very basic overview of Python and the fundamental elements of computer programming. To test your knowledge, please clone the [week-1 repository from Github]() and complete the programming assignment by working directly in the 'week-1.py' file. This assignment will test your knowledge of some of the basic ideas covered in this week's tutorials. Make sure to submit a pull request on your completed assignment before the deadline.