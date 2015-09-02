---
layout: post
title:  Setting up OrientDB
date:   2015-09-16 01:00:00
tags:
- orientdb
---

To start working with OrientDB, go to [http://orientdb.com/](http://orientdb.com/) and click on the 'Download' button on the top right of the screen. Download the latest version of the database for your platform. When the file is finished downloading, unzip it and put the resulting folder somewhere in your file system (such as /My Documents/). Since the whole database runs completely in Java, there is no installation procedure, and the database can be used directly from the unzipped folder.

All of the commands that control the running of the database can be found in the /bin folder within the main OrientDB folder. To start the server, open a command prompt or terminal within this folder (remember Shift+right-click on windows to start a terminal in a folder, or navigate there manually). If you are using Windows, type in

```
server.bat
```

and hit Return. If you are using OSX or Linus type

```
server.sh
```

This will start the server, and will give you feedback on what the server is doing in the terminal window. **Do not close* this window while the server is running. This will cause the server to stop, and can lead to loss of data from not properly shutting down the server. To shut down the server, open another terminal window in the /bin directory, run the `shutdown.bat` or `shutdown.sh` command, and verify that the first window says that shutdown was completed.

A full coverage of OrientDB is beyond the scope of this class, since we will mostly be importing and querying existing databases. For more thorough tutorials and descriptions of features you can consult the [OrientDB documentation](http://orientdb.com/docs/last/). You can also do the free [Getting Started Course](http://orientdb.com/getting-started/) on [Udemy](https://www.udemy.com/orientdb-getting-started/), which will teach you all the basics of working with the OrientDB.

## Working with OrientDB

The easiest way of working with OrientDB is through its graphical web-based interace (called OrientDB studio). Once the server is running, open a web browser and go to http://localhost:2480/ to access the studio. It might prompt you for a global user name and password, which you should have set up when you first started the server. You can also find the user name and password in the 'orientdb-server-config.xml' file in the /config folder in your OrientDB installation. It is in the `<users>` section around line 100.

Once you are logged into studio, you can select a database from the drop down menu. OrientDB comes preloaded with the 'GratefulDeadConcert' database which will allow you to explore some of it's features. Using 'admin' for the User and Password, log into the 'GratefulDeadConcert' database.

You are first presented with the 'Browse' interface, which allows you to query the database using specific commands. Although OrientDB is a NoSQL database, to make transitioning easier for people who have used other databases OrientDB implements a query language built on top of SQL which shares many of it's basic features. Thus if you are already familiar with SQL you will find that most of the same commands work with OrientDB.

Before we get into query commands, let's see how this database is structured. Click on the 'Schema' tab in the top menu. This will show you all of the classes that are in the database. In OrientDB, classes operate similarly as in Python, and define how specific types of data in the database function. Because OrientDB is a graph database, it is initialized with two basic types of classes: 'V' which represents the verteces or objects in the graph, and 'E' which represents the edges or connections. For specific implementations, you can 'extend' one of these two basic classes to include all of their functionality while adding specific properties that is contained in your data.

[graph example]

In the 'GratefulDeadConcert' database, all of the songs, people, and places are stored within the basic 'V' class. This is a great example of a schema-less database, since each 'V' object can have different properties depending on what kind of thing it is, while still existing in the same database. For the connections, the database defines three types of Edge objects, which each extend the base 'E' object ('E' in this case is each of their 'SuperClass'). There is a separate connection type which represents which song was written and sung by which person, and which songs followed which during concerts. Splitting up the connections into different types makes it easier to search through the graph and find the information we are looking for.

Let's explore the data set by making some queries. Go back to the 'Browse' tab on the main menu. In the text box type in

```sql
SELECT * FROM V WHERE type = 'song'
```

This is a basic query that will *SELECT* all data entries *FROM* the class 'V' that match the requirement included after the *WHERE* keyword. In this case we want to select all objects where the 'type' property is 'song'. The (*) is a wildcard, which specified that we want to select all properties from the returned objects. Studio will limit your queries to the first 20 results by default. You don't need to worry about this since it will not be an issue when we start querying with Python, but if you want to change it you can use in the 'LIMIT' keyword to the end of your query, which will explicity set the maximum number of records to return.

```sql
SELECT * FROM V WHERE type = 'song' LIMIT 1000
```

![OrientDB](/dmc/images/orientdb01.png)

For each query OrientDB will give a graphic table which will give the pieces of data along the rows, with the various properties in the columns. You can also view this in the raw JSON format by clicking on the Raw tab at the bottom of the query display. 

The first few columns are devoted to Metadata such as the object's unique ID number (rid or 'record id'), the class it belongs to, and the version of that object (this is incremented automatically if you update an object). The rid is a unique number reserved for each object in the database. It is made up of the 'cluster' to which the object belongs to (there is initially one cluster for each class, but you can make more) and it's index within that cluster. Clicking on the rid will take you to the entry of that object, showing all of it's properties. You can also directly bring up a record by querying its rid. For example

```sql
SELECT * FROM #9:1
```

will directly select this song from the database.

The next section are the actual properties of the object, which can very depending on the definition of the class and the object itself. In this case, since we are only looking at songs, the properties include information such as the type of song, it's name, and the number of times it was performed. The last two sections deal with the graph data, which show the edge objects that connect to each object, and whether they point into or out of the object.

We can also combine conditional and use comparison to find the data for need. For instance, to select all songs that have been performed more than 10 times, we can use the query

```sql
SELECT * FROM V WHERE type = 'song' and performances > 10
```

We can also count the number of entries a query returns simply by wrapping the wildcard with a COUNT() request like this

```sql
SELECT COUNT(*) FROM V WHERE type = 'song' and performances > 10
```

So far all of these examples have used the basic SQL language, and you can find many more useful queries and keywords by searching online. OrientDB also builds additional functionality on top of SQL to allow queries based on the graph structure of the database. For instance, if we want to find all songs sung by the artist whose rid is #9:8 we can use the query

```sql
TRAVERSE in(sung_by) FROM (SELECT * FROM #9:8)
```

*TRAVERSE* is a new keyword provided by OrientDB to deal specifically with navigating graph structures. You can find more information on using traverse in the [OrientDB documentation](http://orientdb.com/docs/2.0/orientdb.wiki/SQL-Traverse.html). This query will return all edges of type 'sung_by' which go *into* the object selected in the query within the second set of parenthesis. Notice, however, that this will also return the artist himself. To fix this you can wrap the whole query with another *SELECT* which will only return objects with type 'song'

```sql
SELECT * FROM (TRAVERSE in(sung_by) FROM (SELECT * FROM #9:8)) WHERE type = 'song'
```

This type of nested request, combined with and interlinked graph structure, can be used to build up complex queries which will locate the exact set of object you are looking for.

For a great basic tutorial of starting out with OrientDB you can consult a [great blog entry](http://pettergraff.blogspot.com/2014/01/getting-started-with-orientdb.html) from Petter Graff.