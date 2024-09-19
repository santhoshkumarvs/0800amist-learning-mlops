from flask import Flask, request, jsonify
import boto3
import pickle
import json
import numpy as np
from io import BytesIO

app = Flask(__name__)

def predict_from_s3(bucket_name, model_key, json_data):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Download the model file from S3
    model_file_obj = s3_client.get_object(Bucket=bucket_name, Key=model_key)
    model_file_content = model_file_obj['Body'].read()
    
    # Load the model from the downloaded content
    model = pickle.load(BytesIO(model_file_content))
    
    # Extract values from the input JSON data
    rooms = int(json_data['rooms_count'])
    area = int(json_data['area_in_sqft'])
    
    # Create a NumPy array with the user input
    user_input = np.array([[rooms, area]])
    
    # Predict the rental price using the loaded model
    predicted_rental_price = model.predict(user_input)
    
    return predicted_rental_price[0]

def upload_result_to_s3(predicted_price, bucket_name, output_key):
    # Prepare the result for uploading
    result = {
        'predicted_rental_price': predicted_price
    }
    
    # Convert result to JSON string
    json_result = json.dumps(result, indent=4)
    
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Upload the JSON string to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=json_result,
        ContentType='application/json'
    )

@app.route('/predict', methods=['POST'])
def predict():
    # Extract the JSON data from the request
    json_data = request.json
    
    # Define your S3 bucket and keys
    bucket_name = 'kfp-main-bt-alpha'
    model_key = 'mymodel/model.pkl'
    output_key = 'output/prediction_result.json'
    
    # Predict the price
    predicted_price = predict_from_s3(bucket_name, model_key, json_data)
    
    # Upload the result to S3
    upload_result_to_s3(predicted_price, bucket_name, output_key)
    
    # Return the prediction result as a response
    return jsonify({'predicted_rental_price': predicted_price})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
