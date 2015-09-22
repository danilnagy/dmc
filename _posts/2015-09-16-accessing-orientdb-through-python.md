---
layout: post
title:  Accessing OrientDB through Python
date:   2015-09-16 03:00:00
tags:
- orientdb
- python
---

OrientDB works fine as a standalone database, but its real power (and usefulness for our purposes) comes from integrating it within a larger data solution such as a server. In this case, querying the database through the built-in console or web interface is not super useful, since we want the queries to actually happen automatically on the backend of our Web Stack. For this, OrientDB provides many separate libraries to allow the database to work with other programming languages, including Python. Using this library, we can start the OrientDB server from within Python, make queries directly with Python code, and work with the returned objects using some of the Python functionality we've already discussed. 

### For this tutorial we will be using the **soufun database**, so if you haven't loaded it yet, please follow the instructions in the previous post to load it before proceeding.

## Installing the pyorient library

This is the first time we have addressed using a separate library with Python, which is actually a very important part of working with Python that will come up again and again. On its own, the Python installation includes only the most basic functionality to make it work as a programming language. This is done intentionally to keep it relatively light compared to other software you might download. On the other hand, what has made Python so popular over the years is that it is very easy to create custom libraries that extend its functionalities for particular purposes. To get this functionality, you just have to download and install the specific library you want to use. With the standard install of Python this can be tricky, since you usually have to go through the command line, make sure you have all the dependencies, and make sure you are installing into the proper folder (which is different depending on which version of Python you have and what operating system you are using). Luckily, Canopy makes installing these libraries (or 'packages' as they are also called) much easier and relatively pain free.

Most popular packages can be installed directly through Canopy's package manager, which can be accessed through the button on the main Canopy splash screen, or by going to Tools -> Package Manager from the Editor window. Here you can search for packages using the search bar in the upper left corner, and if it is available you can install it directly from this window, no trips to the Command Prompt necessary!

Unfortunately, the package we want to install, called **pyorient** is not available through the Package Manager. In this case, you can try to search for it in the [Python Package Index](https://pypi.python.org/pypi) which is a much larger repository of Python packages online. If you search for 'pyorient' you will come to [this page](https://pypi.python.org/pypi/pyorient/) which has some information about the package with instructions on installing it and a link to download it's source files. If you can find the package on this site, you can usually install it through one command on the command line using the Python package management system called pip. The standard command for installing a package is

```
pip install <name of package>
```

However, even with this one step installation, it can still be tricky to get the package into the proper folder. To make this easier we will use the command line interface within Canopy itself. This will ensure that everything ends up in the right place. To do this you can consult the [official instructions](https://support.enthought.com/hc/en-us/articles/204469690-Installing-packages-into-Canopy-User-Python-from-the-OS-command-line) from the Canopy site. Let's follow these instructions to install the pyorient library.

First, open the Canopy Command Prompt by going to Tools -> Canopy Command Prompt from either the Editor or Package Manager window. Execute the following two commands:

```
enpkg setuptools
enpkg pip
```

to update these two packages inside Canopy. If it tells you that the 'Enstaller' is out of date, type 'y' to update it, and then run the above commands again. These packages will allow us to install the package we need through a simple one line process. Once both of these commands have finished running, type

```
pip install pyorient
```

This will install the actual pyorient library into your Python distribution. To check that it worked, go to your Canopy editor or a running version of the Python interpreter in a Command Prompt and try to import the pyorient library using

```python
import pyorient
```

If it does not give you an 'ImportError' saying 'No module named pyorient', the installation succeeded and you can continue with the rest of the tutorial.

## Working with OrientDB in Python

Now let's use the pyorient library to allow Python to communicate with OrientDB. At this point, the documentation of the library is somewhat limited, with most information found on the project's main [Github page](https://github.com/mogui/pyorient). However, the information there is sufficient for the purposes of the class, and since this is an open source project more advanced users can study the functionality by going directly into the source code.

Start a new file either in Canopy or another text editor, and name it 'pyorientTest.py'. Start by importing the two external libraries we will need in this demo

```python
import pyorient
import sys
```

The first is the pyorient library which we will use to work with our database. The second, 'sys', is a system library with some useful functions for working with the operating system. Next, we will create some variables to store information about our OrientDB database. Type the following lines after the import statement:

```python
client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("login", "password")
db_name = "soufun"
db_username = "admin"
db_password = "admin"
```

The first line creates a variable to store our session with the OrientDB server. Notice that the 'OrientDB' function which connects to the server is accessed (through the '.' syntax) directly from the pyorient library. If we had not imported the library this function would not work. Into this function we pass the local address that the database server is running on, which should be the same for everyone. 

The second line connects to the database server using your global username and password. Notice that the 'connect' function is actually a function of the 'client' object and returns a variable that stores information about this particular connection. If you don't remember your username and password you can find it in the 'orientdb-server-config.xml' file in the /config folder in your OrientDB installation. It is in the `<users>` section around line 100. 

The third line stores the name of the database you want to access. For this example we will use the 'soufun' database, so unless you changed its name during loading stage leave this as it is. The last two lines store the username and password for the soufun database, which should be admin/admin unless they were changed during loading.

The next thing we need to do is to open the particular database we will be working with. However, we also want to build in a simple error check to alert the user incase the database they are trying to access does not exist. This is called *error handling* and involves catching certain expected errors and reporting them back to the user in a meaningful way so they know what the problem is. Without proper error handling, every error that the program encounters would cause the program to crash, and the user would not know if it was due to their mistake or a bug in the program.

To create our error check we will build a conditional around a function from pyorient that will check whether a database exists. If the database exists we will open it and proceed with the rest of the script. If it does not exist, we will alert the user and exit the program gracefully (that's where sys comes in).

```python
if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
	client.db_open( db_name, db_username, db_password )
	print db_name + " opened successfully"
else:
	print "database [" + db_name + "] does not exist! session ending..."
	sys.exit()
```

The first line uses the .db_exists() function of the 'client' object to test whether the database name stored in the 'db_name' variable exists on the local server. If the test passes, the database is opened using the .db_open() function, and the success is reported to the user. If it fails, the user is notified that the database was not found, and we use the .exit() function within the sys library to gracefully close the program ('gracefully' implies that we closed the program intentionally, instead of just letting it crash). We will encounter other examples of error handling soon enough, but for a more thorough overview you can consult the [Python documentation](https://docs.python.org/2/tutorial/errors.html).

At this point it is a good idea to save your file and run it through the Python interpreter. Try to use the real database name and make sure that you are getting the success message. Then, try a different name to make sure that the error handling is working as you expect. In general, it is a good idea to test your program constantly, especially after you implement a key feature such as this. Because of the strict syntax involved, fixing bugs is an inherent part of life for even the most seasoned programmer. In general, the more lines of code you've written since the last check, the harder it will be to troubleshoot any bugs.

### If you are getting the error "Protocol version 32 is not supported yet by this client" it is because the latest version of OrientDB is not currently supported by the pyorient library (since pyorient is developed by an outside party it can take some time to update it after a new version of OrientDB is released). If you are having this issue, go to [http://orientdb.com/download-previous/](http://orientdb.com/download-previous/) and download version 2.1.0 which is the one that was used while making these tutorials and has been tested to work with both Windows and OSX. 

Now that we've opened up the database we are ready to start making queries. At this point we are ready to start building our fist spatial query, which we will expand on in the following tutorials. This query will select all of the housing listings within a specified range of latitude and longitude. We will use this later to display listings dynamically based on the boundaries of a map. Before we write the query, we want to create four variables that will store the minimum and maximum latitude and longitude which will define the area we want to look at. An easy way to get latitude and longitudes is to go to Google Maps and use their 'What's here' feature. Go to [https://goo.gl/maps/xAdAx](https://goo.gl/maps/xAdAx). Right click somewhere in the lower left portion of the map, and select 'What's here' from the context menu. 

![OrientDB](/dmc/images/orientdb04.png)

This will create a popup at the bottom of the screen that will tell you the latitude and longitude of that point. Do the same for the upper right corner of the map to get the second set of coordinates. 

![OrientDB](/dmc/images/orientdb05.png)

Now create four variables in your python script to store these values. These are the ones I used:

```python
lat1 = 22.532498
lat2 = 22.552317

lng1 = 114.044329
lng2 = 114.076644
```

You can try to use your own coordinates, but make sure that the area is not too large or the query will take a long time and could return so many results that they fill up the RAM on your computer, causing an 'Out of Memory' error. Also make sure that lat1/lng1 are smaller than lat2/lng2 to make sure the query runs correctly. Note that while the soufun dataset covers all of China, it only represents the urban areas, so you can experiment with other cities but might not get many results in the less populated regions.

Now we are ready to make the query. We will start by creating a string variable that will store the basic template of the query:

```python
query = 'SELECT FROM Listing WHERE latitude BETWEEN {} AND {} AND longitude BETWEEN {} AND {}'
```

This query uses the 'BETWEEN' keyword to find all objects in the 'Listing' class whose latitude and longitude are within certain bounds. It also combines two range queries with the 'AND' keyword. The '{}' marks are variables in the string which we can replace through the string's .format() function. This will save us from having to do a lot of messy concatenation for each lat/lng variable. On the next line, we will actually execute the query on the database using the .command() function of our OrientDB client object. This function will actually send a command (in the SQL format we explored in the last tutorial) to the server. Although pyorient has some of it's own functions for querying databases, .command() is the easiest to use since you can run the same exact queries you would use in the OrientDB Studio. This means you can test the queries first in studio to make sure they work, and then paste them directly into your Python code when you are satisfied. On the next line, type:

```python
records = client.command(query.format(lat1, lat2, lng1, lng2))
```

This line does two things. First, the part within the inner parenthesis takes the basic template string stored in the 'query' variable and formats it (replaces the {} placeholders) with our geographic variables. Then it takes the resulting string and feeds it into the 'client' object's .command() function to execute the query. The results of the query are then stored in a new variable called 'records'. If you are curious you can print the results of the .format() function on its own to make sure that the variables are placed into the correct place. The results will come back as a list, so we can use the len() function to count the number of returned results and print it out:

```python
numListings = len(records)
print 'received ' + str(numListings) + ' records'
```

Let's run the whole script to make sure our query is working. This script should take a few seconds as it is executing the query, and then return the number of results. If you are using the bounds included above, the number should be around 4,000. If the query takes a long time or creates an error, make sure your bounds are not too large. Also, make sure that you have rebuilt your indexes and they are up to date. In this case, as we are searching through millions of data points, having the latitude and longitude fields indexed is crucial to making sure that the query executes in a reasonable amount of time.

Once we are finished with the query, it is important to close the database. Keeping the database open could start to eat up RAM on your computer, and create errors or inconsistencies in your database. At the very end of the script write the line:

```python
client.db_close()
```

to close the database. Next, let's explore what the 'records' variable actually looks like, and how we can work with the actual results. As mentioned above, the results are returned as a list, but a list of what? To find out, let's add some code to print out some information about the results. After the query write

```python
record = records[0]
print type(record)
print record
```

This will get the first record in the records list, and then print the type as well as the contents of the record.

![OrientDB](/dmc/images/orientdb06.png)

As you can see, the records come back as a list of 'OrientRecord' objects, which are similar to dictionaries, except the properties of the listings can be accessed through the '.' syntax, instead of the typical '[]'. For example, to print out the price of the first listing we can add the line

```python
print record.price
```

Similarly, we can access any properties of the returned object that we see in the printed out result. Don't worry about all the text starting with '\x'. This is because the Command Prompt cannot property represent Chinese characters. The results will look much better if you run it in Canopy and once we integrate it with our web-based client side interface.

Now we know the basic way of accessing our OrientDB databases through Python. With this basic setup, you should be able to run any query and analyze the results within Python. For your homework, you will build on this example to return some useful information about the queried results. Please fork the ['week-2' repository](https://github.com/data-mining-the-city/week-2) from the Github page and complete the instructions in the pyorientAssignment.py file. Remember to submit a pull request with your changes before the next deadline.