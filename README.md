# Space Race Project
This is the github repository for capstone project of IBM Data Science Professional certification course on IBM. 

## Problem statement 
In this capstone, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website, with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. 

## Objective 
A data scientist working for a private space launch company will be required to gather information SpaceX launches, create dahsboards for the team, and train a machine learning model using public information to predict if the first stage will land successfully and be reused.

## Data collection 
Historical launch data of SpaceX is collected using [SpaceX api](https://api.spacexdata.com/v4/launches/past). The additional detailed information about booster, payload mass, orbit, launch site data, core data, types and outcomes of the flight are extracted from corresponding additional APIs using collected data columns. 
| api                                                                                                 | data |
| --------------------------------------------------------------------------------------------------- |------------------------------------------------------------------------------------------- |
| [rocket](https://api.spacexdata.com/v4/rockets/)          | Booster name |
| [launchpad](https://api.spacexdata.com/v4/launchpads/) | (1) Longitude, (2) Latitude, (3) Launch site name |
| [payload](https://api.spacexdata.com/v4/payloads/)       | (1) Payload mass, (2) Orbit |
| [cores](https://api.spacexdata.com/v4/cores/)           | (1) Block of the core which is a number used to seperate version of cores, <br /> (2) Number of times this specific core has been reused, <br /> (3) Serial of the core |

[![ibm-ds-capstone-api-flowchart-v2.png](https://i.postimg.cc/sfSXM5Vd/ibm-ds-capstone-api-flowchart-v2.png)](https://postimg.cc/grzd5XXN)

## Data wrangling 
### Target variable
In the `Outcome` column of launch data, there are several labels for different mission outcomes. So, a `Class` variable is defined to represent a classification target variable that represents the outcome of the launch, with 0 as unsuccessful landing and 1 as successful landing. 
| Data label  | Mission outcome                                         | Class |
| ----------- | --------------------------------------------------------|-------|
| True Ocean  | Successfully landed to a specific region of the ocean   | 1 |
| False Ocean | Unsuccessfully landed to a specific region of the ocean | 0 |
| True RTLS   | Successfully landed to a ground pad                     | 1 |
| False RTLS  | Unsuccessfully landed to a ground pad                   | 0 |
| True ASDS   | Successfully landed on a drone ship                     | 1 |
| False ASDS  | Unsuccessfully landed on a drone ship                   | 0 |
| None ASDS   | Failure to land                                         | 0 |
| None None   | Failure to land                                         | 0 |

### Categorical variables 
One-hot encoding is applied to categorical columns: `Orbits`, `LaunchSite`, `LandingPad` and `Serial`. 

## Data visualizations
The success rate is in an increasing trend since 2013, with a peak of 90% in 2019.
<p align="center">
  <img src="https://i.postimg.cc/rpk7Mh1s/image.png" width="400" height="300"/>
</p>

Launch site KSC LC-39A has the highest attribution of 41.7% of all successful landings, whereas CCAFS SLC-40 has the lowest attribution of 12.5%. 
<p align="center">
  <img src="https://i.postimg.cc/VkDXkvMt/image.png" width="700" height="350"/>
</p>

Launch site KSC LC-39A has the highest success rate of 76.9%, whereas CCAFS LC-40 has the largest number of launches, 33, with the lowest success rate of 26.9.
<p align="center">
  <img src="https://i.postimg.cc/8kx7wWdw/image.png" width="700" height="350"/>
</p>

## Predictive analysis  
- The predictor variables are standardized using StandardScalar. 
- The data is then randomly split into 80% training data and 20% testing data.
- Train the logistic regression, SVM, decision tree, and KNN models and tune the corresponding hyperparameters of each model using GridSearchCV.
- Determine the accuracy performance of each model on test data
• Select the best performing classification model


<p align="center">
  <img src="https://i.postimg.cc/v8PZSnWC/ibm-ds-capstone-flowcharts-v2.png"/>
</p>



