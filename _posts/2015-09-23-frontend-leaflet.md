---
layout: post
title:  Setting up maps with Leaflet.js
date:   2015-09-23 03:00:00
tags:
- html
- js
---

Now that we have the communication down, it is time to start building out the actual functionality of our Web Stack. After all, we are not trying to create a website that tells time, right?

The first step will be to use the [Leaflet.js](http://leafletjs.com/) library to create an interactive map underlay for our front end website. Leaflet.js is a very lightweight and popular library for creating interactive web maps based on tiling technology. [Tiling](https://en.wikipedia.org/wiki/Tiled_web_map) is a way of creating interactive, continuous, multi-scalar maps in a web browser by seamlessly joining individual image files that are requested on demand from a server as the user navigates the map. This is the technology that powers almost all modern web maps, including Google Maps, Bing Maps, as well as open source versions such as [Open Street Map](https://www.openstreetmap.org/#map=5/51.500/-0.100) as well as more in depth web mapping services such as [Mapbox](https://www.mapbox.com/) and [CartoDB](https://cartodb.com/). The basic concept is that a collection of tile images at various scales are stored on a server, and a website uses dynamic code to request them as needed and present them in the correct location on the site. The Leaflet library makes this job easier by automating the process of requesting and placing the tiles, and allowing us to use any set of tiles available online.

The Leaflet.js site has a [great set of very clear tutorials](http://leafletjs.com/examples.html) that you can consult to get started with it's basic features. Since we want to build a full-window map application (similar to Google Maps), I will base our code on the ['Leaflet on Mobile'](http://leafletjs.com/examples/mobile.html) tutorial to create a simple interactive full-page map.

Switch to the `03-leaflet` branch in the ['week-3'](https://github.com/data-mining-the-city/week-3) repository. Open the `index.html` file in the templates folder. This file contains a basic html web site, with d3 imported, and a `<script>` section in the `<body>` for writing code. Start by importing the Leaflet library, by adding

```html
<script type="text/javascript" src="./static/lib/leaflet.js"></script>
```

under the d3 import statement. In addition to the .js file, Leaflet also requires us to import a custom .css file that defines how certain features of the map is layed out. [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) is a styling language that provides a quick way for specifying the 'look and feel' of HTML components. This way, you do not have to specify parameters such as color, size, or font for each element in a website. Instead, you just specify those parameters globally in a CSS 'stylesheet', and they will apply to each element contained within a specific tag. Import the Leaflet stylesheet by typing

```html
<link rel="stylesheet" href="./static/lib/leaflet.css"/>
```

on the next line. Next, we will define a couple of our own styles to control how the page and the map is layed out. Like JavaScript, CSS can be either written in a separate .css file and imported, or written directly in the html file, as long as it is enclosed within specific tags. Unlike JavaScript, however, we include the style information within the `<head>` of the page. On the next few lines, type the following code:

```html
<style>
	body {
	    padding: 0;
	    margin: 0;
	}
	html, body, #map {
	    height: 100%;
	}
</style>
```

The basic syntax of CSS stylesheets is pretty simple. You define the html tags you want to add style information to, and enclose the style information within curly braces '{}'. Then you list the styles as key/value pairs, with the property name followed by a ':', followed by the value of that property. As with JavaScript, CSS does not care about spaces or line breaks, so make sure that you end each property wtih a ';' symbol. In this code, we define some basic properties for the `<body>` of the page, telling it that the page should have no padding or marging. This will basically ensure that the page is full screen (you can see a good description of the different properties that control element layout, also known as the 'box model', [here](http://www.w3schools.com/css/css_boxmodel.asp)). We also specify that everything, including the whole document, the `<body>`, as well as any tag labeled with the 'map' id (remember that the '#' refers to the 'id' property of a tag) should have a height of 100%, again ensuring that everything appears full screen.

We are almost done with the `<head>` code. The last thing we need to do is add some code to tell the browser to disable unwanted scaling of the page and set it to its actual size by adding the following line to the end of `<head>` section:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
```

Now in the `<body>` section of the document let's create an empty `<div>` container to store our map.

```html
<div id="map"></div>
```

We give the container the unique id 'map' so that we can apply styling to it and refer to it later in the JavaScript code. Now, within the `<script>` tags let's use the Leaflet library to set up our basic map. The first thing we do is create a variable called 'map' that will store a reference to our new map.

```javascript
var map = L.map('map').setView([22.399961, 114.117523], 11);
```

We use the .map() function of the base Leaflet class (called 'L') and pass it the id of the container where the map should go. In the same line, we run the .setView() function on this map to set where the latitude and longitude where the map should be centered, as well as the zoom level. Executing a sequence of functions one after the other like this is known as 'method chaining', and is another aspect of JavaScript that may be confusing at first, but becomes very handy with practice. This is possible in JavaScript because most class functions return the modified version of 