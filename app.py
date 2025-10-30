import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# --- 1. Load the Model Pipeline ---
# Make sure 'pipeline_v1.bin' is in the same directory
try:
    with open('pipeline_v1.bin', 'rb') as f_in:
        pipeline = pickle.load(f_in)
except FileNotFoundError:
    print("Error: pipeline_v1.bin not found. Make sure you downloaded it.")
    exit()

# --- 2. Define Input Data Structure (Pydantic) ---
# This ensures that the incoming JSON data matches what the model expects.
class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

# --- 3. Initialize FastAPI App ---
app = FastAPI()

# --- 4. Define the Prediction Endpoint ---
# @app.post("/predict")
# def predict(client: Client):
#    # Convert Pydantic model to a standard Python dictionary
#    # The pipeline expects a list of dictionaries for vectorization
#    client_dict = client.model_dump() 
#    
#    # The training code filled NAs: categorical='NA', numeric=0.
#    # While Pydantic helps, we apply the training logic explicitly for safety:
#    processed_client = {
#        'lead_source': client_dict.get('lead_source', 'NA'),
#        'number_of_courses_viewed': client_dict.get('number_of_courses_viewed', 0),
#        'annual_income': client_dict.get('annual_income', 0.0)
#    }
#
#   # Pipeline predicts: vectorization (DictVectorizer) + prediction (LogisticRegression)
#    # Note: It needs a list, even for a single record.
#    X = [processed_client]
#    y_pred = pipeline.predict(X)
#    
#    # The prediction is a numpy array. We take the first element (the prediction itself)
#    # and convert it to a standard Python boolean/integer for the JSON response.
#    result = bool(y_pred[0])
#    
#    return {"conversion_prediction": result}

# Optional: Add a health check endpoint
@app.get("/health")
def healthcheck():
    return {"status": "ok"}


# --- 4. Define the Prediction Endpoint ---
@app.post("/predict")
def predict(client: Client):
    # ... (Prepare client_dict and processed_client as before) ...
    client_dict = client.model_dump() 
    processed_client = {
        'lead_source': client_dict.get('lead_source', 'NA'),
        'number_of_courses_viewed': client_dict.get('number_of_courses_viewed', 0),
        'annual_income': client_dict.get('annual_income', 0.0)
    }
    
    X = [processed_client]
    
    # *** KEY CHANGE: Use predict_proba() instead of predict() ***
    y_proba = pipeline.predict_proba(X)
    
    # y_proba is a 2D array, e.g., [[0.4, 0.6]]
    # Column 0 is the probability of class 0 (No Conversion)
    # Column 1 is the probability of class 1 (Conversion/Subscription)
    
    # We want the probability of conversion (class 1)
    # Round to 3 decimal places for a cleaner output
    conversion_probability = round(y_proba[0, 1], 3)
    
    # We can also get the hard prediction (True/False) to include it
    y_pred = pipeline.predict(X)
    
    return {
        "conversion_prediction": bool(y_pred[0]),
        "conversion_probability": conversion_probability
    }