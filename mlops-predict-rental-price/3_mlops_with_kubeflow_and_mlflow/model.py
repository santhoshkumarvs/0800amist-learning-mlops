import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Set the experiment name
mlflow.set_experiment("rental_price_prediction")

# Start an MLflow run
with mlflow.start_run(run_name="linear_regression_model"):

    # Load and process the data
    # rentalDF = pd.read_csv('data/rental_1000.csv')
    rentalDF = pd.read_csv('s3://kfp-main-bt-alpha/data/rental_1000.csv')

    # Data Transformation (Feature Engineering)
    X = rentalDF[['rooms', 'sqft']].values  # Features
    y = rentalDF['price'].values            # Label

    # Split Data into Training and Testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # Model Training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Compute RMSE
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Log the RMSE metric
    mlflow.log_metric("rmse", rmse)

    # Save the model
    mlflow.sklearn.save_model(model, "model")