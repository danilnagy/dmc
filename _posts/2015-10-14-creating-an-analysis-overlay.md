---
layout: post
title:  Creating an analysis overlay
date:   2015-10-14 00:30:00
tags:
- html
- js
- python
---

At this point, we have developed most of our basic Web Stack functionality. Our system contains a database, a server side which can query the database for data, and a client side which can understand user input, make requests to the server, and visualize the information it gets back to the user interface. Pretty cool!

In the next set of tutorials, we will start to implement some features to process our data and use it to create new data. This process of creating new data from existing data is called 'modeling'. A model uses a finite set of known data to develop a representation of how the underlying system that created the data works. Once this model is developed, it can then be used to predict new data points which are not yet known. A simple example of a model is the formula 'F = ma', Newton's second law of motion which describes the relationship between an object's mass and acceleration, and the Force that was applied to it. Before this formula was known, values for each of these three variable might have been gathered by experimenting on different objects. Once enough data was gathered, you (if you were as smart as Isaac Newton) might have seen a relationship between the three values that was perfectly described by the equation 'F = ma', which is the model that describes how the underlying system of motion functions. Once you have this model, you can use it to describe the behavior of objects that you have not tested and thus for which you have no data. For example, you might take an object of a known weight, and predict how fast it will accelerate when a given force is applied to it.

The class of models we will utilize in this class fall under the category of 'Machine Learning'. These are highly complex models that typically cannot be described by an equation. Instead, they are described by an abstract computational structure, and utilize a system of 'training' to model a given set of data. Once the model is trained with a sufficient amount of data, it can be used to predict data for which we do not know a certain kind of information. One very common example of these models are [recommender systems](https://en.wikipedia.org/wiki/Recommender_system), which are used by sites like Netflix and Amazon to predict what the customer will want based on past purchases. Another common use in geo-spatial analysis is [spatial interpolation](https://en.wikipedia.org/wiki/Spatial_analysis#Spatial_interpolation), which tries to estimate the value of properties at unsampled sites within an area covered by existing observations. For example, if we have a collection of data about housing prices in various points within a city, we can use Machine Learning to predict what the price will be at other points of the city where we don't have samples. 

Since many applications in [geospatial analysis](https://en.wikipedia.org/wiki/Geospatial_analysis) deal with predicting the values of certian properties over space, it is helpful to have a standard geometry that we can use to visualize these values. It is common to use a regular square grid for this purpose. In this way, the model is trained using a finite set of data points with geographic coordinates. Then, the coordinates of each cell in the regular grid are fed into the model, and the value is predicted for each location. Then, the color of each cell can be used to represent the value, creating a visualization of the value across the space.

[diagram showing interpolation]

