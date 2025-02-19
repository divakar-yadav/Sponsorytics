from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import numpy as np
import os
import chardet
import time
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

# Predefined company descriptions
reference_companies = {
    "american_family_insurance": "American Family Insurance, commonly known as AmFam, is a leading mutual insurance company headquartered in Madison, Wisconsin...",
    "verizon": "Verizon Communications Inc. is a leading global provider of telecommunications, technology, and media services...",
    "rockwell": "Rockwell Automation is a leading global provider of industrial automation and digital transformation solutions..."
}

# Cache embeddings for reference companies (computed once)
reference_embeddings = {name: None for name in reference_companies}


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


# Precompute embeddings for reference companies
for name, desc in reference_companies.items():
    if reference_embeddings[name] is None:
        reference_embeddings[name] = get_embedding(desc)


@app.route("/upload", methods=["POST"])
def upload_files():
    """Uploads two specific files to Azure Blob Storage."""
    
    required_files = ["Companies_in_Milwaukee.xlsx", "Affiliated_Program_Industry_Features.xlsx"]
    
    # Check if files are present in request
    if "files" not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist("files")
    
    # Ensure both required files are uploaded
    uploaded_filenames = [secure_filename(file.filename) for file in files]
    missing_files = [f for f in required_files if f not in uploaded_filenames]

    if missing_files:
        return jsonify({"error": f"Missing files: {', '.join(missing_files)}"}), 400

    responses = {}

    for file in files:
        filename = secure_filename(file.filename)

        if filename not in required_files:
            return jsonify({"error": f"Unexpected file: {filename}. Expected only {required_files}"}), 400

        # Read file content
        raw_data = file.read()

        # Determine container based on filename
        container_name = CONTAINER_ONE if filename == "Companies_in_Milwaukee.xlsx" else CONTAINER_TWO
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        try:
            blob_client.upload_blob(raw_data, overwrite=True)
            file_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}"
            responses[filename] = file_url
        except Exception as e:
            return jsonify({"error": f"Upload failed for {filename}: {str(e)}"}), 500

    return jsonify({"message": "Files uploaded successfully", "uploads": responses}), 200



@app.route('/calculate_similarity', methods=['POST'])
def calculate_similarity():
    """Computes cosine similarity between uploaded file embeddings and reference company embeddings."""
    try:
        data = request.get_json()
        file_texts = data.get("file_texts", {})

        if not file_texts:
            return jsonify({"error": "No file texts provided"}), 400

        # Generate embeddings for input files
        input_embeddings = {
            file_name: get_embedding(content) for file_name, content in file_texts.items()
        }

        # Compute similarity
        results = []
        for file_name, file_embedding in input_embeddings.items():
            similarities = {
                ref_name: cosine_similarity(file_embedding, ref_embedding)
                for ref_name, ref_embedding in reference_embeddings.items()
            }
            avg_similarity = sum(similarities.values()) / len(similarities)
            results.append({
                "file": file_name,
                "similarities": similarities,
                "average_similarity": avg_similarity
            })

        sorted_results = sorted(results, key=lambda x: x["average_similarity"], reverse=True)

        return jsonify(sorted_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
