from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import numpy as np
import os
import chardet
import time
import pandas as pd
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-domain requests

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure Storage Configuration
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_ONE = os.getenv("AZURE_CONTAINER_ONE")
CONTAINER_TWO = os.getenv("AZURE_CONTAINER_TWO")

# Verify required environment variables
if not all([openai.api_key, AZURE_CONNECTION_STRING, CONTAINER_ONE, CONTAINER_TWO]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# Predefined reference company descriptions
reference_companies = {
    "american_family_insurance": "American Family Insurance is a leading mutual insurance company headquartered in Madison, Wisconsin...",
    "verizon": "Verizon Communications Inc. is a leading global provider of telecommunications, technology, and media services...",
    "rockwell": "Rockwell Automation is a global provider of industrial automation and digital transformation solutions..."
}

# Function to compute cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Function to get embeddings from OpenAI API with retry mechanism
def get_embedding(text):
    retries = 3  # Max retries for OpenAI API
    for attempt in range(retries):
        try:
            response = openai.embeddings.create(model="text-embedding-ada-002", input=text)
            return response.data[0].embedding
        except openai.error.RateLimitError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

# Function to fetch file content from Azure Blob Storage
def fetch_blob_content(container_name, blob_name):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        stream = blob_client.download_blob()
        raw_data = stream.readall()  # Keep as raw bytes

        return raw_data  # Return binary data instead of decoding it

    except Exception as e:
        raise RuntimeError(f"Error fetching file {blob_name} from {container_name}: {str(e)}")


import io

# Function to extract company names from an Excel file
def extract_company_names_from_excel(excel_content, column_name="Company Name"):
    """Extracts company names from an Excel file content."""
    try:
        df = pd.read_excel(io.BytesIO(excel_content))  # Read binary data using io.BytesIO
        return df[column_name].dropna().tolist()
    except Exception as e:
        raise RuntimeError(f"Error reading Excel file: {str(e)}")


@app.route('/calculate_similarity', methods=['POST'])
def calculate_similarity():
    """Fetches uploaded files, extracts company names, computes cosine similarity."""
    try:
        # Define required files
        file1 = "Companies_in_Milwaukee.xlsx"
        file2 = "Affiliated_Program_Industry_Features.xlsx"

        # Determine the containers for each file
        container1 = CONTAINER_ONE
        container2 = CONTAINER_TWO

        # Fetch file contents from Azure Blob Storage (Binary format)
        content1 = fetch_blob_content(container1, file1)
        content2 = fetch_blob_content(container2, file2)

        # Extract company names from both Excel files
        companies1 = extract_company_names_from_excel(content1, "Company Name")
        companies2 = extract_company_names_from_excel(content2, "Company Name")

        if not companies1 or not companies2:
            return jsonify({"error": "No company names found in one or both files"}), 400

        # Convert company names into a single text string
        text1 = ", ".join(companies1)
        text2 = ", ".join(companies2)

        # Get embeddings for extracted company names
        embedding1 = get_embedding(text1)
        embedding2 = get_embedding(text2)

        # Compute cosine similarity
        similarity_score = cosine_similarity(embedding1, embedding2)

        return jsonify({
            "file1": file1,
            "file2": file2,
            "companies_in_file1": companies1,
            "companies_in_file2": companies2,
            "similarity_score": similarity_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
