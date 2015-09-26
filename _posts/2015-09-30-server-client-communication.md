---
layout: post
title:  Server/Client communication (passing arguments)
date:   2015-09-30 03:00:00
tags:
- html
- js
- python
---

Now that we have several ways to capture user intraction and have users drive the functionality of our Web Stack, we need a better way to handle communication between the client and the server. Currently, our communication is limited to only executing functions written on the server. However, we have no way of sending any other information to the server to control how this function is executed. For example, we are able to call a function to get data from the database, but we can't tell the server exactly what data we want. In our immediate case, it would be great if we can get the range of latitude and longitude coordinates currently presented on the screen, and send those to the server when we execute the function so it can return all of the data points within that range.

If we were just working in Python, we would be able to pass this information as inputs into the function. Since we are now dealing with a distributed framework between the JavaScript client and the Python server, however, passing such information is a bit more complicated. To handle this kind of communication, HTTP allows you to attach a list of extra parameters, known as a [query string](https://en.wikipedia.org/wiki/Query_string), to the end of a request. You may have already seen such parameters in the address bar of your web browser. For instance, if you use Google to search for the term 'javascript', the address bar might change to something like this:

```
https://www.google.com/?q=javascript
```

Here Google is using a query string to communicate what you are searching for back to it's main page. Because Google's pages are always dynamic, there is obviously no special page for any single query. Instead, the base page gets the information from the query string and process the query dynamically as the page is loadeding. The query string is attached to the main request using a '?' mark. Each parameter or 'argument' in the query string is a key/value pair separated by a '=' mark. Multiple arguments can be sent by separating them with a '&' mark. For instance, if Google supported another argument which specified the maximum results to return, you might have a request such as this:

```
https://www.google.com/?q=javascript&maxresults=100
```

This query string has two arguments: 'q' which stores the search term, and 'maxresults' which stores the maximum number of results to return. 

To improve the capabilities of our Web Stack, we will use a query string attached to our `/getData` request to pass information about the exact range of latitude and longitude we want to retreive from the database based on the current limits of the map. Before we can do this, however, we must first find this range by getting the bounds of our map from Leaflet. Switch to the `02-creating-ui-elements` branch in the ['week-4’](https://github.com/data-mining-the-city/week-4) repository and open the `index.html` file inside the '/template' folder. Within the `updateData()` function, before the line that runs the `d3.json` method, let's create a new variable to store the current map bounds:

```javascript
var mapBounds = map.getBounds();
```

To get the map bounds we are using the `.getBounds()` method of the Leaflet map object stored in the 'map' variable. The map bounds come back as a dictionary with the latitude and longitude of the 'northeast' and 'southwest' corner of the currently visible map. Let's create four more variables to store the min/max values of latitude and longitude that we will pass to the server:

```javascript
var lat1 = mapBounds["_southWest"]["lat"];
var lat2 = mapBounds["_northEast"]["lat"];
var lng1 = mapBounds["_southWest"]["lng"];
var lng2 = mapBounds["_northEast"]["lng"];
```

We take the smaller latitude and smaller longitude from the southwest corner, and the maximum latitude and longitude from the northeast corner of the map. Now let's build up a new request, this time using a query string to pass these four geography variables. Previously, our request was just the `/getData` route that we specified on our server. We can add a query string to this route the same way we would for a web address, but just appending it to the request with a '?'. Let's write out the request string on a new line after our new lat/lng variables:

```javascript
request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2
```

Here we're using '+' to concatenate strings that describe the data being sent (the 'keys') with the data we want to send (stored in the lat1, lat2, lng1, and lng2 variables). To make sure the request is right, you can log it to the JavaScript console. The final request should look something like this:

```
/getData?lat1=22.532695150697624&lat2=22.545379121718994&lng1=114.04907226562499&lng2=114.07510042190552
```

Finally, let's change the parameter that we are passing into the `d3.json()` function from the static "/getData" to our new dynamic request string:

```javascript
d3.json(request, function(data) {
```

Now that the client is sending our geographic parameters as arguments to the server, we need to handle them on the server side so they can be used to make the proper database query. Open the `app.py` file in the main folder of the repository. At the top of the file, let's import another module of the flask library by adding this line below the other two flask import statements:

```python
from flask import request
```

This imports an object called 'request' that processes the requests coming into the server, and gives us access to the arguments sent through the query string. Next, delete these four lines within the `getData()` function, which we were using to staticly specify the lat/lng ranges of our query:

```python
lat1 = 22.532498
lat2 = 22.552317

lng1 = 114.044329
lng2 = 114.076644
```

Instead, at the top of the `getData()` function, let's create four new variables to store the arguments coming in from the request:

```python
lat1 = str(request.args.get('lat1'))
lng1 = str(request.args.get('lng1'))
lat2 = str(request.args.get('lat2'))
lng2 = str(request.args.get('lng2'))
```

You can see that the arguments are stored in the 'args' property of the request object, and we can use its '.get()' method to retreive the arguments we want. Notice that the keys we pass into the '.get()' method correspond directly to the keys we specified in the query string of the request. We also wrap the arguments within a `str()` function to make sure that the arguments come in as text strings. We can check that we are getting the proper coordinates by printing out the values of these variables on the next line:

```python
print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"
```

Since our new lat/lng variables share the same names as the old ones, our query should still work. Now, however, the geographic parameters are being determined dynamically according to the bounds of the map, and being passed as arguments from directly from the client. Restart the server and reload the page to make sure everything is working properly. Now when you pan the map and click the 'Update Data' buttom, it should reload new data filling the extents of the map. You can even try zooming out and running the function again to get a wider set of data. Be careful though. The wider your search query, the more data the database will return, and the longer the query will take on the server side.

For more details about Flask's use of the [request object](http://flask.pocoo.org/docs/0.10/quickstart/#the-request-object) as well as other ways of [accessing request data](http://flask.pocoo.org/docs/0.10/quickstart/#the-request-object) you can consult the [Flask quickstart](http://flask.pocoo.org/docs/0.10/quickstart/) documentation.

Congratulations! We can now pass all kinds of information from the client to the server, and create more nuanced commands that react to the current conditions of the client interface. In the next tutorial we will explore another kind of communication, which will allow the client and server to communicate back and forth in real time. This will allow us to get immediate feedback about what is happening on the server, and let us track it's progress during longer periods of processing.