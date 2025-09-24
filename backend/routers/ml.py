import os
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
import requests
from typing import Dict

# The router is created without a prefix.
# The prefix will be added in main.py when the router is included.
router = APIRouter(
    tags=["Machine Learning"]  # This groups the endpoint in the API docs.
)

# --- Configuration ---
# The URL for your model service, loaded from an environment variable.
# Ensure this is set in your Railway project settings.
MODEL_SERVICE_URL = os.environ.get("MODEL_SERVICE_URL")

# The endpoint path is now clean and simple.
# Final URL will be: /api/ml (from main.py) + /classify-waste (from here)
@router.post("/classify-waste", response_model=Dict)
async def classify_waste_image(image: UploadFile = File(...)):
    """
    Receives a waste image, forwards it to the ML model microservice for
    classification, and returns the model's prediction.
    """
    # Check if the model service URL is configured
    if not MODEL_SERVICE_URL:
        logging.error("MODEL_SERVICE_URL environment variable is not set.")
        raise HTTPException(status_code=500, detail="Model service is not configured correctly.")

    # Validate that the uploaded file is an image
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Prepare the image file in the format the model service expects
    files = {'image': (image.filename, await image.read(), image.content_type)}

    try:
        logging.info(f"Forwarding request to model service at {MODEL_SERVICE_URL}")
        # Send the POST request to the external model service
        response = requests.post(MODEL_SERVICE_URL, files=files, timeout=30)
        
        # Check if the model service responded with an error
        response.raise_for_status()
        
        # Return the successful JSON response from the model
        return response.json()

    except requests.exceptions.Timeout:
        logging.error("Request to the model service timed out.")
        raise HTTPException(status_code=504, detail="The model service took too long to respond.")
    except requests.exceptions.RequestException as e:
        # Handle network errors or if the model service is down
        logging.error(f"Could not connect to the model service: {e}")
        raise HTTPException(status_code=503, detail=f"The model service is currently unavailable: {e}")

