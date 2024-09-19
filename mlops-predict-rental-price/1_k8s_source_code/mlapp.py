import json
import kfp
from kfp import dsl
from kfp.compiler import Compiler
from kfp.client import Client

# Define the model development component
@dsl.component(packages_to_install=['numpy', 'pandas', 'joblib', 'scikit-learn'])
def modeldevelopment(rooms: int, sqft: int)-> float:
    import pandas as pd
    import numpy as np
    import joblib
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error

    # Load and process the data( Replace with your rental_data.csv)
    rentalDF = pd.read_csv('https://raw.githubusercontent.com/azonecloud/0800amist-learning-mlops/main/mlops-predict-rental-price/data/rental_1000.csv')

    # Data Transformation (Feature Engineering - Use Features for Model Development)
    X = rentalDF[['rooms', 'sqft']].values   # Features 
    y = rentalDF['price'].values             # Label

    # Split Data into Training and Testing 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    # Model Training
    model = LinearRegression().fit(X_train, y_train)

    # Save the Model
    joblib.dump(model, '/tmp/rental_price_model.joblib')
    
    # Compute RMSE (optional)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse}")

    # Predict the rental price
    predict_rental_price = model.predict(np.array([[rooms, sqft]]))[0]
    print(f"The Predicted Rental Price for Rooms={rooms} and Area in Sqft={sqft} is={predict_rental_price}")

    return predict_rental_price


# Define the pipeline using the model development and prediction components
@dsl.pipeline(
    name='Rental Prediction Pipeline',
    description='A pipeline to predict rental prices using a trained model.'
)
def rental_prediction_pipeline(rooms_count: int, area_in_sqft: int) -> float:
    model_task = modeldevelopment(rooms=rooms_count, sqft=area_in_sqft)
    return model_task.output

if __name__ == "__main__":
    
    # Load pipeline arguments from a JSON file
    with open('pipeline_args.json', 'r') as f:
        arguments = json.load(f)
    
    # Compile the pipeline
    # Compiler().compile(rental_prediction_pipeline, 'rental_prediction_pipeline.yaml')

    # Connect to Kubeflow Pipelines server
    kfp_endpoint = None  # Replace with the actual URL of your Kubeflow Pipelines server
    client = kfp.Client(host=kfp_endpoint)

    # Create an experiment
    experiment_name = 'Experiment for Model to Predict Rental Price'
    experiment = client.create_experiment(name=experiment_name)
    print(f'Experiment created: {experiment}')
   
    # Run the pipeline using create_run_from_pipeline_func
    run_name = 'Run of Rental Price Prediction Pipeline'
    run_result = client.create_run_from_pipeline_func(
        pipeline_func=rental_prediction_pipeline,
        run_name=run_name,
        experiment_name=experiment_name,
        arguments={
            'rooms_count': arguments.get('rooms_count'),
            'area_in_sqft': arguments.get('area_in_sqft')
        }
    )

    print(f'Pipeline run submitted: {run_result}')
