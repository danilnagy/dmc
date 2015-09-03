---
layout: post
title:  Accessing OrientDB through Python
date:   2015-09-16 03:00:00
tags:
- orientdb
- python
---

Accessing OrientDB through Python

OrientDB works fine as a standalone database, but it's real power (and usefulmess for our purpose) comes from integrating it within a larger data solution such as a server. For this, querying the database through the built in console or web interface is not super useful, since we want the queries to actually happen automatically on the backend of our Web Stack. For this, OrientDB provides many separate libraries to allow the database to work with other programming languages, including Python. Using this library, we can actually start the OrientDB server from within Python, make queries directly with Python code, and work with the returned objects. 

#For this tutorial we will be using the **soufun database**, so if you haven't loaded it yet, please follow the instructions in the previous post to load it before proceeding.

### Installing the pyorient library

This is the first time we have addressed using a separate library with Python, which is actually a very important part of working with Python that will come up again and again. On it's own, the basic Python installation has only the most basic functionality to make it work as a programming language. This is done intentionally to keep it relatively light compared to other software you might download. On the other hand, what has made Python so popular over the years is that it is very easy to create custom libraries that extend it's functionalities for particular purposes. To get this functionality, you just have to download and install the specific library you want to use. With the basic install of Python this can be tricky, since you usually have to go through the command line, make sure you have all the dependencies, and make sure you are installing into the proper folder (which is different depending on which version of Python you have and what operating system you are using). Luckily, Canopy makes installing these libraries (or 'packages' as they are sometimes called) much easier and relatively pain free.

Most popular packages can be installed directly through Canopy's package manager, which can be accessed through the button on the main Canopy splash screen, or by going to Tools -> Package Manager from the Editor window. Here you can search for your package using the search bar in the upper left corner, and if it is available you can install it directly from this window, no trips to the Command Promt necessary!

Unfortunately, the package we want to intall, called **pyorient** is not available through the Package Manager. In this case, you can try to search for it in the [Python Package Index](https://pypi.python.org/pypi) which is a much larger repository of Python packages online. If you search for 'pyorient' you will come to [this page](https://pypi.python.org/pypi/pyorient/) which has some information about the package with instructions on installing it and a link to download it's source files. If you can find the package on this site, you can usually install it through one command on the command line using the Python package management system called pip. The standard command for installing a package is

```
pip install <name of package>
```

However, even with this one step installation, it can still be tricky to get the package into the proper folder. To make this easier we will use the command line interface within Canopy itself. This will ensure that everything ends up in the right place. To do this you can consult the [official instructions](https://support.enthought.com/hc/en-us/articles/204469690-Installing-packages-into-Canopy-User-Python-from-the-OS-command-line) from the Canopy site. I will also go through the step by step process for installing the particular library we need.

First, open the Canopy Command Prompt by going to Tools -> Canopy Command Prompt from either the Editor or Package Manager window. Execute the following two commands

```
enpkg setuptools
enpkg pip
```

to update these two packages inside Canopy. If it tells you that the Enstaller is out of date, type 'y' to update it, and then run the above commands again. These packages will allow us to install the package we need through a simple one line process. Once both of these commands have finished running, type

```
pip install pyorient
```

This will install the actual pyorient library into your Python distribution. To check that it worked, go to your Canopy editor or a running version of the Python interpreter in a Command Prompt and try to import the pyorient library using

```python
import pyorient
```

If it does not give you an 'ImportError' saying 'No module named pyorient' the installation succeeded and you can continue with the rest of the tutorial.

### Working with OrientDB in Python

Now let's start to use the pyorient library to allow Python to communicate with OrientDB. At this point, the documentation of the library is somewhat limited, with most information found on the project's main [Github page](https://github.com/mogui/pyorient). However, the information there is sufficient for the purposes of the class, and since this is an open source project more advanced users can study the functionality by going directly into the source code.

Start a new file either in Canopy or another text editor, and name it 'pyorientTest.py'. On the first line, import the library by typing

```python
import pyorient
```

Next, we 