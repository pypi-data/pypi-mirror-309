from promptflow.core import tool
from azure.storage.blob import BlobServiceClient
from pathlib import Path
from typing import Dict, List
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from promptflow.connections import CustomConnection, AzureOpenAIConnection
from concurrent.futures import ThreadPoolExecutor

import json

def download_blob(container_name: str, connection_string: str):
    """
    Download specific blobs from an Azure Blob Storage container to the local folder 'faissindex/'.
    
    Args:
        container_name (str): The container where the FAISS index can be found.
        connection_string (str): Connection string for access to the Azure Blob Storage.

    Returns:
        None
    """
    # Connect to the Azure Blob Storage and download the blobs
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()

    # Create a local folder 'faissindex/' if it does not exist
    Path("./faissindex/").mkdir(parents=True, exist_ok=True)

    def download_blob(blob_name: str):
        """
        Download the FAISS index blobs from the Azure Blob Storage.
        
        Args:
            blob_name (str): The name of the blob to download.
        """
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        if blob_name in ['faissindex/index.pkl', 'faissindex/index.faiss']:
            with open(file=f"{blob_name}", mode="wb") as download_file:
                download_file.write(container_client.download_blob(blob_name).readall())

    # Download the blobs in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(download_blob, [blob.name for blob in blob_list if blob.name in ['faissindex/index.pkl', 'faissindex/index.faiss']])

def create_structure(documents: Dict) -> List[Dict]:
    """
    Create a structured list of documents with the text, metadata and a score.

    Args:
        documents (Dict): A dictionary with documents and scores.

    Returns:
        List[Dict]: A list of dictionaries with structured data.
    """
    
    # Return a list of dictionaries with the text, metadata and score
    return [{'text': doc[0].page_content, 'metadata': doc[0].metadata, 'score': doc[1]} for doc in documents]

@tool
def custom_lookup_function(query: str, filters: str, top_k: int, container_name: str, storage: CustomConnection, openai: AzureOpenAIConnection) -> str:
    """
    Get filtered context based on a query and a filter using Azure OpenAI and FAISS.

    Args:
        query (str): The search query.
        filters (str): The metadata filters that have to be applied.
        top_k (int): The amount of results to return.
        container_name (str): The container where the FAISS index can be found.
        storage (CustomConnection): The connection with the storage in which the FAISS-index is located.
        openai (AzureOpenAIConnection): The connection with Azure OpenAI services.

    Returns:
        str: A JSON-formatted list with structured results.
    """
    # Check if the FAISS index exists locally; if not, download it
    if not Path('./faissindex/index.faiss').exists():
        try:
            # Keep in mind that the connection string is stored as key2 in the storage secrets
            storage_string = storage.secrets["key2"]
            download_blob(container_name, storage_string)
        except:
            download_blob(container_name, storage.connection_string)
    
    # Initialize AzureOpenAIEmbeddings with the correct parameters
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-ada-002",
        openai_api_version=openai.api_version,
        api_key=openai.api_key,
        azure_endpoint=openai.api_base
    )

    # Load the FAISS index from the local folder 'faissindex'
    db = FAISS.load_local("faissindex", embeddings, allow_dangerous_deserialization=True)
    
    # Do a similarity search with filtering
    # The filter should be in a dict format: {"metadata-field1": "filter1", "metadata-field2": "filter2", "...": "..."}
    filters_json = json.loads(filters)
    results = db.similarity_search_with_score(query, filter=filters_json, k=top_k)

    # Create a structured output of the results
    output = create_structure(results)

    # Return the structured output as a JSON-formatted string
    return str(output) 