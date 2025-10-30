import requests
import json

# Replace "YOUR_URL" with the actual endpoint
url = "http://localhost:8000/predict" 

client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

# Send the POST request
response = requests.post(url, json=client)

# Get the JSON response
result = response.json()

# Print the result
print(f"Request Status Code: {response.status_code}")
print(f"Prediction Result: {result}")