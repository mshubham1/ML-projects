
# Car Price Prediction

This application will predict the Selling price of your car depend upon the varoius user inputs.
Car Price Prediction is a regression machine learning problem statement. 

## Table Content ✏️
* Demo
* Overview
* Dataset
* Installation
* Technology Used
* Bug/Feature Request
* Future scope of project
## Demo
![Car_Price_prediction](https://user-images.githubusercontent.com/47842305/141054996-13d86889-c352-450c-912b-580ad9654afe.gif)



## Overview  📜
The application is a web app which is developed in Flask Framework.

* Data Exploration - Using pandas,numpy,matplotlib and seaborn.
* Data Visulization- Insights obtained through graph about dependent and independent variable.
* Feature Engineering - Drop the column with higher correlation and perform StandardScaler to scale the data.
* Model Training - Trained the model with different regressor algo and obtained the Random Forest Regressor with best score.

```bash
      Model	                    MAE	       MSE	   RMSE
0	Decision Tree Regressor	 0.7440	 2.3642  1.5376
1	Random Forest Regressor	 0.5204	 0.5357  0.7319
2	XGB Regressor	       0.5067	 0.5859  0.7654
3	Linear Regression	       0.8737      1.3856  1.1771
```
## Dataset  
Dataset is available in Kaggle by CarDheko Company.
This dataset contains information about used cars.
This data can be used for a lot of purposes such as price prediction to exemplify the use of linear regression in Machine Learning.
Dataset link: https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho
## Installations  🗄️
The Code is written in Python 3.8 If you don't have Python installed you can find it here. If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip. To install the required packages and libraries, run this command in the project directory after cloning the repository:


First you need to create a virtual conda enviornment.

```bash
  conda create -n myenv python=3.6
  pip install -r requirements.txt
```
## Technologies Used

* Python
* FrontEnd: HTML & CSS
* Backend: Flask 

## Contributers
You can feel free to reach out me at shubhammourya2014@gmail.com

@Shubham Mourya
