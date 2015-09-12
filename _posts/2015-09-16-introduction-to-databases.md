---
layout: post
title:  Introduction to Databases
date:   2015-09-16 00:30:00
---

Now that we know that basics of writing code in Python, we can start the actual work of developing our Web Stack. One of the fundamental components of the Stack is a database, which will store all of our data and allow us to access it in an efficient way. 

Databases can come in a variety of structures. One of the most basic is a table, such as the ones used within Excel. Typically, each row in a table represents a piece of data, and each column represents a specific property of that data. Because the columns are hard wired into the tables, each piece of data needs to share the same property, and it is very difficult to add or delete properties once a table has been started. 

![table database](/dmc/images/db01.png)
*A traditional table-based database where connections between items can be made by linking keys*

Despite these limitations, traditional tables are still widely used in data management applications today. Traditionally, these databases are termed '[relational](https://en.wikipedia.org/wiki/Relational_database)'. For large data applications, a special language was developed called 'Structured Query Language' or [SQL](https://en.wikipedia.org/wiki/SQL), which has commands for searching and retrieving (querying) data from the database.

To address some of the limitations of relational databases, and to accommodate the specific needs of Big Data and Cloud-based applications, several new types of databases have been developed in the last decade, loosly organized under the term NoSQL. The term [NoSQL](https://en.wikipedia.org/wiki/NoSQL) stands for 'Not Only Structural Query Language', implying that such systems support all the functionality of traditional SQL databases, but also add other functionality.

A very popular type of NoSQL database is known as a ['document-oriented database'](https://en.wikipedia.org/wiki/Document-oriented_database), which organizes the database as a loose collection of 'documents', with each piece of data represented by a single document. These documents do not necessarily have to have the structure, allowing different pieces of data to have different properties. Because this type of database does not have to start with a predefined '[schema](https://en.wikipedia.org/wiki/Database_schema)' of property, it is often called a schema-free database. One very popular document-based database is [MongoDB](https://www.mongodb.org/) which is widely used in many web applications today.

![document database](/dmc/images/db02.png)
*A document-based database where each item is stored as a separate document and can have it's own unique properties*

Another exciting kind of NoSQL database is a ['graph database'](https://en.wikipedia.org/wiki/Graph_database), which can store not only individual data points, but information about how those data relate to each other and how they interconnect. One early graph database which has become quite popular is [Neo4J](http://neo4j.com/). 

![graph database](/dmc/images/db03.png)
*A graph-based database where relationships between different items can be represented as connections or 'edges' in a graph. These connections are stored as objects themselves, with data about which objects they are connecting.*

Although GIS applications have traditionally used relational, table-style databases, there are many potential advantages to using a NoSQL database. Although tables are great at storing well curated, government-provided geographic data, as urban analysts embrace more 'messy' data such as that found on the internet they will need tools that can handle a large steady stream of data that does not necessarily conform to a predefined schema. 

One of the data sets we will use in this class contains apartment listings for all of China, with data about when those apartments were seen online. Because each listing was accesed at different times, this kind of data could not be accommodated by a traditional table. Likewise, graph databases also have some interesting applications for urban analysis, as they are able to capture not only the static 'stuff' of cities, but also the dynamics behind how all that stuff interacts. Another data set we will see in the class contains data about locations within the Pearl River Delta, users of the social network Weibo, and information about which users visited which places when. Although this data could be stored in several different tables, a graph database allows us to search through the connections between places very quickly using some fundamental ideas from [graph theory](https://en.wikipedia.org/wiki/Graph_theory).

For developing our Web Stack, we will utilize one of the youngest NoSQL databases, [OreintDB](http://orientdb.com/), which combines features of both document-oriented databases suchs as MongoDB, and graph databases such as Neo4J. Although OrientDB is relatively new and still has some bugs, it's potential as an integrated and extremely modern database system is quite exciting, and will be great to explore through the class.