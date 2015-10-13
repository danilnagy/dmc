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

In the next set of tutorials, we will start to implement some features to process our data and use it to create new data. This process of creating new data from existing data is called 'modeling'. A model uses a finite set of known data to develop a representation of how the underlying system that created the data works. Once this model is developed, it can then be used to predict new data points which are not yet known. A simple example of a model is the formula 'F = ma', Newton's second law of motion which describes the relationship between an object's mass and acceleration, and the force that was applied to it. Before this formula was known, values for each of these three variables might have been gathered by experimenting with different objects. Once enough data was gathered, you (if you were as smart as Isaac Newton) might have seen a relationship between the three values that was perfectly described by the equation 'F = ma', which is the model that describes how the underlying system of motion functions. Once you have this model, you can use it to describe the behavior of objects that you have not yet tested. For example, you might take an object of a known weight, and predict how fast it will accelerate when a given force is applied to it.

The class of models we will explore in this class fall under the category of ['Machine Learning'](https://en.wikipedia.org/wiki/Machine_learning). These are highly complex models often used to describe systems that cannot be easily represented by an equation. Instead, they are described by an abstract computational structure, and utilize a system of 'training' to model a given set of data. Once the model is trained with a sufficient amount of known data, it can be used to predict information about unknown data. One very common example of these models are [recommender systems](https://en.wikipedia.org/wiki/Recommender_system), which are used by sites like Netflix and Amazon to predict what the customer will want based on past purchases and the purchases of other similar customers. Another common use in geo-spatial analysis is [spatial interpolation](https://en.wikipedia.org/wiki/Spatial_analysis#Spatial_interpolation), which tries to estimate the properties of unsampled sites within an area covered by existing observations. For example, if we have a collection of data about housing prices in various points within a city, we can use Machine Learning to predict what the price will be at other points of the city where we don't have actual samples. 

Since many applications in [geospatial analysis](https://en.wikipedia.org/wiki/Geospatial_analysis) deal with predicting the values of certain properties over space, it is helpful to have a standard geometry that we can use to visualize these values. For this purpose it is common to use a regular square grid, which creates an 'overlay' over the map to visualize the data at a given resolution. To create this overlay, we first train the model using a finite set of data points within our study area. Then, the coordinates of each cell in the regular grid overlay are fed into the model, and the value is predicted for each grid location. Then, the color of each cell can be used to represent the value, creating a visualization of the value across the space.

[diagram showing interpolation]

In this tutorial we will build a graphic overlay within our client side code and connect it to our back end server so it can send information about the data to be visualized. We will then use this overlay to visualize the results of data processing and Machine Learning applications in later tutorials. Switch to the `02-analysis-overlay` branch in the ['week-5’](https://github.com/data-mining-the-city/week-5) repository. This branch contains our current implementation of the Web Stack, including the refactoring work done in the previous tutorial. 

Let's start by creating the graphic portion of the overlay. Open the `script.js` file within the `/static` folder in a text editor. The first step will be to create a new 'svg' container and 'g' group to hold our rectangle geometry. These new elements will be very similar to the ones created to hold the circle geometry, and can be added to the code directly above them. Find the line that reads:

```javascript
var svg = d3.select(map.getPanes().overlayPane).append("svg");
```

This is the line that creates the svg for the circles. Directly above it, type the lines:

```javascript
var svg_overlay = d3.select(map.getPanes().overlayPane).append("svg");
var g_overlay = svg_overlay.append("g").attr("class", "leaflet-zoom-hide");
```

You can see that these lines are very similar to the two below. They specify a new 'svg' element called 'svg_overlay' which will contain the graphic elements of the overlay, and a new 'g' group called 'g_overlay' which will group the actual rectangle geometries. 

Now that we have the basic containers for visualizing our overlay geometry, we need to connect it to the back end server which will specify the size and location of the overlay grid, and attach to each cell the data to be visualized. To create the overlay grid, the server will need to know the width and height of our browser window, as well as the resolution of grid we want. In this case we will specify the size we want for each square in pixels, and let the server figure out the total resolution of the grid. To pass this information to the server, we will modify the request string that is sent to the server within the `updateData()` function. In the `script.js` file, find the line that reads:

```javascript
request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2
```

This is the current request being sent to the server every time the `updateData()` function runs. At this point it is only sending the latitutde and longitude ranges of the area to use for querying the data points. In place of this line, let's create a few new variables to store the dimensions of our browser window as well as our desired grid cell size, and modify the request to send this information to the server:

```javascript
var res = 25;
var w = window.innerWidth;
var h = window.innerHeight;

request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2 + "&w=" + w + "&h=" + h + "&res=" + res
```

The first line specifies that we want each square in the grid to be 25 pixels in size. The next two lines use the handy `window.innerWidth` and `window.innerHeight` functions to get the current width and height of the browser window and store them in two new variables. We will use these variables to tell the server how big to make our grid. We will also use them later to resize the `svg_overlay` element so that it always matches the dimensions of our screen. Finally, we append these three variables to the query string of our request to send this information to server.

