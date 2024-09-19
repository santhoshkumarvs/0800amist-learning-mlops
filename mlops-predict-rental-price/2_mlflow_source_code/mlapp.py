from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import mlflow
import mlflow.spark

spark = SparkSession.builder.getOrCreate()

# Read the CSV file into a Spark DataFrame
mldataset_path = 'data/rental.csv'
modelpath = 'model/'

# Set the experiment
mlflow.set_experiment("rental_prediction_experiment")

rentalDF = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(mldataset_path) \
    .withColumnRenamed("Area (sqft)", "area") \
    .withColumnRenamed("Number of Rooms", "roomcount") \
    .withColumnRenamed("Locality", "locality") \
    .withColumnRenamed("Rent Price (USD)", "rent")

splits = rentalDF.randomSplit([0.7, 0.3])
train_data = splits[0]
test_data = splits[1]
print("Training Rows:", train_data.count(), "Testing Rows:", test_data.count())

# Convert categorical 'Locality' column to numeric using StringIndexer
indexer = StringIndexer(inputCol='locality', outputCol='localityIdx')
indexedtrainData = indexer.fit(train_data).transform(train_data).drop('locality')
indexedtestData = indexer.fit(test_data).transform(test_data).drop('locality')

# Prepare features and label columns
feature_cols = ['area', 'roomcount', 'localityIdx']
assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')

# Define the Linear Regression model
lr = LinearRegression(featuresCol='features', labelCol='rent')

# Define the pipeline
pipeline = Pipeline(stages=[indexer, assembler, lr])

# Fit the model
model = pipeline.fit(train_data)

# Evaluate the model on test data
predictions = model.transform(test_data)
evaluator = RegressionEvaluator(labelCol='rent', predictionCol='prediction', metricName='rmse')
rmse = evaluator.evaluate(predictions)

# Log evaluation metric
mlflow.log_metric("rmse", rmse)

# Print RMSE
print("Root Mean Squared Error (RMSE):", rmse)

# Save MLflow run ID for reference
run_id = mlflow.active_run().info.run_id
print("MLflow run completed with ID:", run_id)

# Save the PySpark model using MLflow
mlflow.spark.save_model(model, modelpath)

print("Experiment run complete.")
