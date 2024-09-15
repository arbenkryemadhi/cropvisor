import pandas as pd
import numpy as np
from netCDF4 import Dataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
nc_file_path = 'weather_data.nc'


train = pd.read_csv("crop_recommendation.csv")

# Preprocess data
X = train.drop("Crop", axis=1)
X = X.drop('Nitrogen', axis=1)
X = X.drop('Phosphorus', axis=1)
X = X.drop('Potassium', axis=1)
X = X.drop('Humidity', axis=1)
X = X.drop('pH_Value', axis=1)

y = train["Crop"]

scaler = StandardScaler()
X_preprocessed = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

# Train the model

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)



def fetch_weather_data(latitude, longitude, month):
    # Open the NetCDF file
    with Dataset(nc_file_path, 'r') as nc:
        # Extract dimensions and variables
        latitudes = nc.variables['latitude'][:]
        longitudes = nc.variables['longitude'][:]

        # Find the nearest indices for the given latitude and longitude
        lat_idx = (np.abs(latitudes - latitude)).argmin()
        lon_idx = (np.abs(longitudes - longitude)).argmin()
        month_idx = int(
            month) - 1  # Assuming month is provided as a 1-based index (1 for January, 2 for February, etc.)

        # Extract temperature and precipitation data for the given location and month
        # Adjust the variable names based on the dataset structure
        temperature = nc.variables['skt'][month_idx, lat_idx, lon_idx] - 273.15
        rainfall = nc.variables['tp'][month_idx, lat_idx, lon_idx] * 1000

    return temperature, rainfall


def recommend_crop(latitude, longitude, month):
    # Fetch weather data for the given location and month
    temperature, rainfall = fetch_weather_data(latitude, longitude, month)

    print(f"Temperature: {temperature}\nRainfall: {rainfall}")

    # Prepare the input data
    input_data = np.array([[temperature, rainfall]])

    # Normalize the input data
    input_data_scaled = scaler.transform(input_data)

    # Predict the crop
    crop_prediction = rf_classifier.predict(input_data_scaled)

    return crop_prediction[0]




# TEST
latitude = 30.3279
longitude = 19.8190
month = '01'

#crop = recommend_crop(latitude, longitude, month)
#print(f"The recommended crop for the given conditions is: {crop}")