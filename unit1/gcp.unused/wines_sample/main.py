from google.cloud import storage
from io import StringIO
import numpy as np
import pandas as pd
import sklearn.linear_model as lm
import sklearn.model_selection as ms


def predict_wine_quality(request):
    bucketname = 'labs'
    source_filename = 'winequality-red.csv'

    try:
        client = storage.Client()
        bucket = client.get_bucket(bucketname)
        blob = bucket.get_blob(source_filename)
        raw_contents = blob.download_as_string().decode("utf-8")

        contents_io = StringIO(raw_contents)
        wines_df = pd.read_csv(contents_io)

        predictors_df = wines_df.drop('quality', axis=1)
        response_df = wines_df['quality']

        predictors_training_df, predictors_testing_df, response_training_df, response_testing_df = ms.train_test_split(predictors_df, response_df, test_size=0.2)

        algorithm = lm.LinearRegression()
        model = algorithm.fit(predictors_training_df, response_training_df)
        prediction = model.predict(predictors_testing_df)

        # Calculate some characteristics of the residuals.
        residuals = np.abs(response_testing_df.values - prediction)

        # Calculate r-squared.
        r_squared = algorithm.score(predictors_df, response_df)

        print(f"The r-squared value of the data is {r_squared}. The mean of the residuals are {residuals.mean()} with a standard deviation of {residuals.std()}.")
        print("Overall, linear regression does a fair job predicting the quality of wine.")

        return 'Success.'
    except Exception as err:
        return f"This HTTP triggered function executed successfully, but errored with {str(err)}."
