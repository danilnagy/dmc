---
layout: post
title:  Breaking up the code
date:   2015-10-14 00:15:00
tags:
- html
- js
- python
---

At this point we are ready to start developing some of the more advanced features of our Web Stack. However, our index.html file is already getting a bit crowded since it contains all of the client functionality, including the layout of HTML elements, our custom styling, and the dynamic JavaScript code. As we begin to add even more functionality, this file can quickly become very long and difficult to navigate. After a period of development, it is good practice to ['refactor'](https://en.wikipedia.org/wiki/Code_refactoring) or restructure existing code to make it more manager or easier to handle for further development. Refactoring does not change the behavior of the code, but simply gives it a better structure. 

Part of refactoring might be to redefine functions or object definition to make them perform more efficiently. Another common practice is to break code up into separate files which pertain to specific functionalities within the program. This helps further development since you can look at specific smaller files when you want to develop new features, instead of having to search through a single lengthy file which may have many sections for various features of the program. This is one of the fundamental aspects of ['modular programming'](https://en.wikipedia.org/wiki/Modular_programming), which is very popular today, and has to do with the breaking up of code into separate 'modules' which encapsulate specific functionalities and can be easily used and extended by both the original author as well as outside developers.

Let's do a bit of refactoring to our client side code in the `index.html` file by breaking out the custom CSS styling and the dynamic JavaScript code to separate files, leaving only the HTML code in the index.html file. To do this, you simply copy all of the code between the `<style> </style>` tags and paste it in a separate file called `style.css`. Once you do this you can delete this code, including the `<style> </style>` tags from the `index.html` file. Place the new file in the `/static` folder in the main repository folder, where we currently have the `/bin` folder with the JavaScript libraries. To create a new file you can right click within the destination folder and go to `New -> Text Document`. Then select the whole name, including the `.txt` extension and name it `style.css`. It will ask you if you are sure you want to change the extension, click yes. It is important that you use the proper extensions, otherwise the code may not be properly recognized by the web browser and the text editor. 

Now let's follow the same process to break out the JavaScript code to a separate file as well. Copy everything between the `<script type="text/javascript"> </script>` tags in the `index.html` file and paste it into a new file called `script.js`, also in the `/static` folder. What you name these files is up to you, but in this case I have given them very generic names, which you should keep to make sure that the rest of your code matches the examples.

Now that the CSS and JavaScript code is broken out into separate files, the last thing we need to do is reimport them into the base `index.html` file so they are loaded and run when the page loads. We have already done this to load in the external `d3.js` and `leaflet.js` libraries, and we can copy some of that code to load in our custom files as well. Fork and clone the ['week-5’](https://github.com/data-mining-the-city/week-5) repository from the DMC Github page and switch to the `01-breaking-up-the-code` branch. This branch already has the code broken up into separate files. You can find the `style.css` and `script.js` files in the `/static` folder. Now open up the 'index.html' file. Notice on line 9 the following code:

```html
<link rel="stylesheet" href="./static/style.css" />
```

Here, in the `<head>` section, we use the `<link>` tag to import the `style.css` into our file the same way we did for the leaflet custom styling contained in the `leaflet.css` file. We can use a similar strategy for importing the JavaScript code. However, we want to make sure this runs after all of our HTML structures have been created in the `<body>` section. Otherwise, the script will not be able to find and reference those elements in the code. At the very end of the `<body>` section on line 33 find the code:

```html
<script type="text/javascript" src="./static/script.js"></script>
```

This code will import the file in the 'src' parameter and execute its code at this point in the file. Notice that this is the same structure we used in the `<head>` section to import the d3.js and leaflet.js files. It is also the same tag we used to create JavaScript code directly in the `index.html` file. However, instead of typing the code directly between the `<script> </script>` tags, we are using the optional 'src' parameter to link to an external file.

Now when you run the `app.py` server in the Terminal or Command Prompt, or within the Canopy environment, you should get the same performance from the Web Stack. If you look at the messages from the Python interpreter, you should see two more requests being sent to the server for the `style.css` and `script.js` files.

![Break-up](/dmc/images/breakup01.png)

Although the functionality of our Web Stack has not changed, having the code in different files will make it easier for us to make changes and add further functionality in the next tutorials. It will also make it more clear for us which code is responsible for which parts of the program. For instance, when we add dynamic code, we will know to add it to the `script.js` file. If we need to do any styling we will know to add it to the `style.css` file. Although this is a specific example, there are no rules for how you refactor and break up your code. As you develop more and more functionality, you might want to break up the code even further, to have multiple scripts inside separate `.js` files and separate `.css` files for different sets of styling rules. Although the exact implementation depends on your project, you should get in the habit of performing this kind of 'refactoring' to make your code easier to understand and work with for yourself as well as for others.