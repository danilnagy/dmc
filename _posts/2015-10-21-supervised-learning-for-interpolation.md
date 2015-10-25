---
layout: post
title:  Supervised learning for interpolation
date:   2015-10-21 02:00:00
tags:
- python
- orientdb
---

### Setting up the model

To start developing the Machine Learning model, fork and clone the ['week-6'](https://github.com/data-mining-the-city/week-6) repository from the DMC Github page and switch to the `02-supervised-learning` branch. This branch has all of the code we have developed so far, including the analysis overlay grid that was developed in the last tutorial. To prepare for this tutorial, the color of the circles has been changed to gray to make the interpolation results easier to read. The name and id of the checkbox has also been changed from 'Heat Map' to 'Interpolation' to relate to the type of analysis we will be doing. The checkbox has also been set to be 'checked' by default, so that the analysis is performed the first time the page is loaded. The remainder of this tutorial will focus on the server side, where we will implement and train our model. To visualize the results, we will utilize the same framework we developed for the heat map, to make sure that our connection to the client end visualization remains intact.

Open the `app.py` file from the main repository directory in a text editor. This is the same server code we developed in the previous tutorials, except the portion of the code that is specific to the heat map has been commented out. Our new Machine Learning implementation will go in place of this code, and utilize the same data structure to make sure that the rest of our implementation continues to function in the same way.

Before we start writing the actual analysis code, we need to import the appropriate libraries into Python. At the top of the file, find the line that reads:

```python
from Queue import Queue
```

This is the last library we are currently importing. Under this line, add the lines:

```python
from sklearn import preprocessing
from sklearn import svm

import numpy as np
```

This will import two modules from the scikit-learn library: the 'preprocessing' module which will let us do some necessary preparation of the data, and the 'svm' module which actually implements the SVM algorithms for Machine Learning. We will also import the 'numpy' library, which is a core numerical analysis library that is necessary for converting data into a format that scikit-learn can work with. Adding 'as np' to the import statement allows us to use the 'np' shorthand for referencing the library as opposed to its full name.

Now go to line 165 in the document, directly below where the heat map code has been commented out. This is where we will write all the code for our Machine Learning implementation. Notice that the definition of the 'grid' list has not been commented out. To make sure that our analysis data is still passed correctly to the client, we will use this same grid list to make predictions and store the results.

First, let's create a couple of empty lists to store the feature and target data we will use to train our Machine Learning model. On a new line, type the following code:

```python
featureData = []
targetData = []
```

Remember that the feature data stores all the information that describes our data, except for the value that we want to model. In our case, the feature data will consist of the latitude and longitude of each data point. The target data then stores the value we want to model, which we know for a limited set of training data, but might not know for other data points. In our case, the value we want to model is the price of the data point. During training, the model will 'learn' how to relate the target value to the values in the feature data. This will allow us to 'predict' the target value of price for data points that we don't have a price for, such as the coordinates of the analysis overlay grid.

Next, let's iterate over all of the records returned from the database, and add the appropriate data to our feature and target data sets:

```python
for record in records:
	featureData.append([record.latitude, record.longitude])
	targetData.append(record.price)
```

The feature data set will be a list of lists. Each record in our data set will be represented by a list that contains all of the feature data we will use for training, in this case the latitude and longitude of the point. The target data set, on the other hand, will be a single list, with one target value associated with each record.

Next, we will convert both of these data sets from basic python lists to special numpy arrays. Scikit-learn, like many Python libraries, is built on top of numpy, which implements many very efficient multi-dimensional data structures for performing advanced computation as quickly as possible. Thus, to allow scikit-learn to work with our data, we will first have to convert it to special arrays that can be processed by numpy. Luckily, this is very easy to do:

```python
X = np.asarray(featureData, dtype='float')
y = np.asarray(targetData, dtype='float')
```

Here we create two new variables, and use the `np.asarray()` function from numpy to convert both lists to numpy arrays. The second parameter specifies that the data is of type 'float', which you have to declare explicitly in numpy. For the names of the arrays, we use X and y, which are conventions in Machine Learning. In descriptions of Machine Learning algorithms, 'X' typically represents the input or feature data set. It is capitalized because it is a two dimensional array (with the number of rows equal to the number of data samples, and the number of columns equal to the number of features), which is also a convention of numerical analysis. Likewise, 'y' typically represents the output or target data set, and it is kept lower case because it is a single dimensional array, with the length equal to the number of data samples. Calling the two data sets X and y is intuitive when discussing Machine Learning, since the trained model is understood to be a kind of function which gives values of 'y' based on 'x' inputs.

Now that we have our two data sets, we are almost ready to train the model. Before we do that, however, it is recommended that we normalize our feature data set so that each feature has a mean 0 and a variance of 1. We do this to balance out the features, and make sure that they all play an equal part in training the model. Otherwise, if one feature has a much larger range or average value than another, it would have a disproportionately large effect on the final model. To automate this scaling process, scikit-learn's preprocessing module has a useful object called [`StandardScaler`](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), which we implement by adding the following lines of code:

```python
scaler = preprocessing.StandardScaler().fit(X)
X_scaled = scaler.transform(X)
```

The first line creates a scaler object for our X data set by utilizing the `.fit()` method of the `StandardScaler` object. After we create the scaler object, we can then use its `transform` method to transform the X data set, and store it in a new variable called `X_scaled`. 

### Choosing the parameters

Now we are ready to train the model. In this case we will be using the [SVR](http://scikit-learn.org/stable/modules/svm.html#regression) model, which is an implementation of Support Vector Machines (SVM) for *regression*. SVR and other SVM algorithms can typically use a variety of functions or 'kernels' to model the data. The scikit-learn implementation allows you to use linear, polynomial, radial basis function (rbf), or sigmoid kernels (for more detail you can consult the [entry in the documentation](http://scikit-learn.org/stable/modules/svm.html#kernel-functions) covering SVM kernels). The first two kernel options are based on mathematical equations, and tend to give more rigid models that are more likely to suffer from high bias (for a good conceptual discussion of the bias-variance tradeoff, you can consult this [article](http://scott.fortmann-roe.com/docs/BiasVariance.html)). The last two kernels are distance-based functions that are determined by the distance of target points to each other. These functions are less restrictive then those based on mathematical equations, and thus tend to create looser models that are more likely to suffer from high variance. Although you are encouraged to experiment with all the kernel options, in this case we will use the 'rbf' kernel, which is the default choice for SVR. 

To control how tightly the SVR models the training data, the algorithm allows you to set two parameters, *C* and *ε* (the Greek letter epsilon), which are common across all SVM implementations. These parameters provide two ways to set the sensitivity of the model, to ensure that the model is flexible enough to represent the underlying system creating the data, but not so sensitive that it starts to model the noise that is particular to the training data. The *C* parameter represents the penalty parameter of the error function, which determines how seriously the algorithm tries to get every training data point right. With lower C values, the algorithm will forgive some misclassifications or poor predictions in exchange for a smoother decisions surface or simpler model. At higher C values, the algorithm will try to get every training point right, but the resulting model will be very complex and likely to model noise. In the bias-variance tradeoff, lower C values create high bias, while higher values create high variance:

`high bias <--- C ---> high variance`

The second parameter of the SVR model, *epsilon*, represents the width of the model's soft margin, which is the distance around a decision boundary within which training points that are misclassified are ignored. In the case of a continuous regression model like the SVR, the epsilon specifies how wrong the predicted value of a feature point has to be before it is considered an error. Lower values of epsilon will create a tighter margin, which means that the model will try to classify each point correctly, which leads to more complex models. Higher values of epsilon will allow the model to ignore more error, which leads to simpler and smoother models. In the bias-variance tradeoff, lower epsilon values create high variance, while higher values create high bias:

`high variance <--- epsilon ---> high bias`

A third parameter available for the SVR model which is specific to the 'rbf' kernel is *gamma*, which defines the strength of the distance function. Intuitively, this parameter effects how far the influence of a single training example reaches, with low values meaning 'far' and high values meaning 'close'. This is somewhat similar to the 'spread' parameter we used for the heat map calculation, although with the opposite meaning for high and low values. Lower values of gamma will give each point a farther influence, making the model smoother and simpler overall. Higher values will localize the effect of each sample, creating a more complex and jagged model, prone to local over-fitting. In the bias-variance tradeoff, lower gamma values create high bias, while higher values create high variance:

`high bias <--- gamma ---> high variance`

For a more in depth description of the parameters available for SVM models, you can read this [section](http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html#example-svm-plot-rbf-parameters-py) in the scikit-learn documentation. You can also consult the [SVR documentation](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR) for a full list of available parameters and their default settings.

By setting these parameters, we can get fairly good control of how the model performs, and how closely it will try to model our training data. In real world applications, the practice of Machine Learning is primarily concerned with the selection of an appropriate model and the proper setting of these parameters. Ofcourse the difficulty of this problem is that the parameters are fairly abstract, and rarely have any intuitive connection with the data or the system you are trying to model. Furthermore, the appropriateness of the parameters is fully dependent on the particular dataset you are working with, and thus there is rarely a correct answer for how to set them. Thus, Machine Learning practitioners usually rely on an experimental approach for setting the parameters, by generating many models with different parameter values, and choosing the one which performs best on a blind test set. This practice, known as cross-validation, is key to a proper implementation of Machine Learning, and we will cover it in the next tutorial. For now, we will just guess the values of these parameters to complete our basic model implementation.

### Training the model

On the following lines, write this code:

```python
C = 10000
e = 10
g = .01

model = svm.SVR(C=C, epsilon=e, gamma=g, kernel='rbf', cache_size=2000)
model.fit(X_scaled, y)
```

This is all the code we actually need to train our SVR model. On the first few lines, we specify the values of the three main parameters, whose values we guess for the time being. On the next line, we create the model we are going to use, and specify its parameters by passing them into the `.SVR()` method of scikit-learn's 'svm' module. The first four should be familiar to you, as they specify the three parameters described above, as well as the kernel we will be using. The final parameter sets the maximum RAM space that scikit-learn can use to perform the calculation. Setting this value higher will increase the speed of the calculation, but you should not set this higher than the memory you have available on your computer. We store the model with these parameters in a new variable called 'model' so we can use it in our code. On the last line we actually train the model on our data set by calling its `.fit()` method and passing both the feature and target data sets. The `.fit()` method will run an optimization process to model the data set in the most optimal way based on the parameter values. How long this takes depends on the model parameters and the size of the data, but it could take a bit of time so be patient!

Once the model is trained it can be used to predict the target value for new sets of features. In our case, we can use it to predict the price at any latitude or longitude in the world, although in practice it only really make sense to make predictions within the same range as the training data that the model is based on. Let's now use the model to predict the values within each cell of our analysis grid, which will give us our interpolation analysis. On the next lines, write the following code:

```python
for j in range(numH):
	for i in range(numW):
		lat = remap(j, numH, 0, lat1, lat2)
		lng = remap(i, 0, numW, lng1, lng2)

		testData = [[lat, lng]]
		X_test = np.asarray(testData, dtype='float')
		X_test_scaled = scaler.transform(X_test)
		grid[j][i] = model.predict(X_test_scaled)
```

Here we are using the same double loop we have seen before to iterate through all the rows and columns in our analysis grid. Within the loop, the first thing we have to do is to convert the x and y coordinates of each cell (represented by the iterators i and j) to their equivalent latitude and longitude coordinates on the map. We need to do this because the model was trained based on geographic latitude/longitude data. So if we want to make predictions based on the grid, we first need to get the geographic coordinates of each of its cells. To do this we use the `remap()` helper function we created earlier to map the grid coordinates from the starting range which goes from 0 to the number of rows and columns (stored in numH and numW), to the geographic extents of the map (which are stored in lat1/lat2 and lng1/lng2). As before, we have to flip the row grid range so that it matches the progression of latitudes increasing vertically on the page.

Once we have the latitude and longitude coordinates of the grid cell, we use them to create a new 'test' sample in the same format as the feature data set we created before. In this case we still have a list of lists, except now there is only one sample with a list of two features storing its coordinates. As before, we use the `.asarray()` method of the numpy library to convert this list to a numpy array. Then, we apply the 'scaler' object from before to this new sample to scale it to the same range as what was used to train the model. It is extremely important that you store the scaler operation in this way, so you can later apply it to any data you give to the model.

Finally, we pass the scaled data set to the `.predict()` method of the model, which returns a predicted value for the target. In this case, it will return its best guess for the price that an apartment in this grid cell would cost. We will store this value into the same 'grid' nested list that we used to store the values of the heat map. This way, the rest of our code should work in the same way.

The next line of code in your script should be the normalization of the grid list using the `normalizeArray()` helper function we created earlier. This normalization ensures that we do not need to worry about the range of values being returned from our predictions, since the visualization will be automatically scaled with red for the highest values and blue for the lowest. However, ultimately you would want to build in a graphic scale which informs the user about the values represented by the colors on the map.

Save the `app.py` file and start the server by running the `app.py` file in the Command Prompt or Terminal, or within a Canopy session. Make sure you also have your OrientDB server running, and have changed the database name and login information in the `app.py` file to match your database. Go to [`http://localhost:5000/`](http://localhost:5000/) in your browser. You should now see the message that the analysis is running, and once it is finished you should see the results of the interpolation visualized in the analysis grid. Don't worry if the results don't quite make sense yet. Since we specified the model parameters arbitrarily, they may not be the best settings for your data, which could generate poor prediction results.

This completes the first basic implementation of Machine Learning on the server. You can see that in terms of code, applying these models using scikit-learn is extremely easy. However, to apply them well and get meaningful results, it is important to understand the basics of how the algorithms work, and how to set the proper parameters for your data. The primary method for doing this is called cross-validation, and we will implement this for our example in the next tutorial.