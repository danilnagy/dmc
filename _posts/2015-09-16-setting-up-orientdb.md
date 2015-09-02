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



To start, we can type