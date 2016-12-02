# Montreal Street Parking
This directory includes the script and notebook files for the following dataset:<br/>
https://www.kaggle.com/mnabaee/mtlstreetparking

This dataset includes the coordinates of the street segments as well as the parking signals in the City of Montreal.

##Using TensorFlow for Distributed Calculation of Closest Street Segments
Since the calculation of the closest street segments for all of the parking signs takes a long time, it was necessary to run it on multiple machines. Specifically, the signs were split into multiple smaller sets and each set was processed on a different machine. This task was done using the [distributed computing capabilities in TensorFlow](https://www.tensorflow.org/versions/r0.12/how_tos/distributed/index.html).

A few samples of the results are shown in the following map. Each marker in the map represents the location of a parking sign and the red line segment is the corresponding segment which is found to be closest to the sign.

<img src="closestSegments.bmp" width="600" align="middle">


##Parsing the sign texts
Each parking sign in the dataset has a text description which we need to parse and understand to be able to derive rules from.
The rules will then be used to say if we can park in a street side segment in a given time period.

##Putting everything together

The final demo notebook which uses the processed signs and draws a map of the street sides for a given time period is available [here](https://github.com/mnabaee/kernels/blob/master/mtl-street-parking/demo.ipynb)

In below, you can see the final results shown in a map. In the map, the street sides with green represent an appropriate place for parking during the specified hours in the specific day. 
<img src="finalres.png" width="600" align="middle">
