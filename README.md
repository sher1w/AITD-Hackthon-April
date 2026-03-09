Blue Harvest – Fish Prediction System

About the Project
Blue Harvest is a small project that tries to predict possible fishing zones near the Goa coast using environmental data.
The idea of the project is to use basic machine learning and ocean data such as temperature and salinity to estimate whether fish may be present in certain areas. The system also gives a possible fishing zone based on conditions.
This project is mainly built as a demonstration of how data and simple AI models can help in fisheries management.

Models Used
1. Fish Presence Model
A Decision Tree Classifier is used to predict whether fish are likely to be present.

Inputs:
Salinity
Temperature

Output:
Fish present
Fish not present

The trained model is saved as:
fish_predictor_model.pkl

2. Fishing Zone Prediction
Another Decision Tree model is used to estimate which fishing zone might be suitable.

Inputs used:
Temperature
Month of the year
Ocean current
Chlorophyll level

Possible zones:
Calangute
Baga
Colva

The model is trained on generated sample data in the backend.

Data Used
The system uses a few different sources of data:

Temperature
Fetched using a weather API.

Salinity
Loaded from a dataset file.

Ocean current and chlorophyll
Simulated values used to represent ocean conditions.

Tech Stack

Backend
Python
Flask
Pandas
Scikit-learn

Frontend
React
Vite

How to Run

Backend
Install dependencies
pip install flask pandas numpy scikit-learn joblib requests
Run the server
python FishFinder.py

Frontend
Install packages
npm install

Run the app
npm run dev
Notes

This project is a prototype and uses simplified environmental data.
The goal is to show how machine learning could help analyze fishing conditions
