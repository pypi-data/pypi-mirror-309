from typing import List, Dict, Any, Optional
from promptflow.core import tool
from promptflow_vectordb.core.contracts import SearchResultEntity
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import logging
import urllib.parse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

@tool
def generate_context_blob_url(
    search_result: List[Dict[str, Any]],
    account_name: str,
    container_name: str,
    generate_sas_urls: int = 1,
    append_page_number: int = 0,
    retrieve_metadata: int = 1
) -> str:
    """
    Generates a prompt context by retrieving blob URLs and formatting document information,
    including optional blob metadata retrieval. Allows users to toggle SAS URL generation,
    page number appending, and metadata retrieval.

    Args:
        search_result (List[Dict[str, Any]]): List of search result items.
        account_name (str): Azure Blob Storage account name.
        container_name (str): Azure Blob Storage container name.
        generate_sas_urls (int): Generate SAS URLs for blobs (1 for true, 0 for false).
        append_page_number (int): Append page numbers to the blob URLs (1 for true, 0 for false).
        retrieve_metadata (int): Retrieve blob metadata (1 for true, 0 for false).

    Returns:
        str: A formatted string containing document information and blob metadata.
    """

    def format_doc(doc: Dict[str, Any]) -> str:
        metadata_str = "\n".join([f"{key}: {value}" for key, value in doc.get('Metadata', {}).items()])
        metadata_section = f"\nBlob Metadata:\n{metadata_str}" if metadata_str else ""
        return (
            f"Content: {doc['Content']}\n"
            f"Source: {doc['Source']}\n"
            f"Blob URL: {doc.get('BlobURL', '')}{metadata_section}"
        )

    SOURCE_KEY = "source"
    URL_KEY = "url"

    # convert integer to booleans
    generate_sas_urls_bool = bool(generate_sas_urls)
    append_page_number_bool = bool(append_page_number)
    retrieve_metadata_bool = bool(retrieve_metadata)

    blob_service_client = None
    container_client = None
    delegation_key = None
    blob_names = []

    if generate_sas_urls_bool:
        try:
            # authenticate using AzureCliCredential
            credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=credential
            )
            container_client = blob_service_client.get_container_client(container_name)
            # get user delegation key for SAS token generation
            delegation_key = blob_service_client.get_user_delegation_key(
                key_start_time=datetime.utcnow(),
                key_expiry_time=datetime.utcnow() + timedelta(hours=1)
            )
        except Exception:
            logger.error("Failed to create BlobServiceClient or get delegation key.")
            generate_sas_urls_bool = False  # disable SAS URL generation error

    if generate_sas_urls_bool:
        try:
            # list all blob names in the container
            blob_names = [blob.name for blob in container_client.list_blobs()]
        except Exception:
            logger.error("Failed to list blobs in the container.")
            generate_sas_urls_bool = False  # disable SAS URL generation if error

    def generate_blob_url(blob_name: str, page_number: Optional[int] = None) -> str:
        try:
            # generate SAS token for the blob
            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=container_name,
                blob_name=blob_name,
                user_delegation_key=delegation_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1),
                protocol='https',
                content_disposition="inline",
            )
            encoded_blob_name = urllib.parse.quote(blob_name, safe='/')
            blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{encoded_blob_name}?{sas_token}"

            # append page number if enabled
            if append_page_number_bool and page_number is not None and isinstance(page_number, int):
                adjusted_page_number = page_number + 1
                blob_url += f"#page={adjusted_page_number}"

            return blob_url
        except Exception:
            logger.error(f"Failed to generate SAS URL for blob: {blob_name}")
            return ""

    retrieved_docs = []
    for item in search_result:
        try:
            entity = SearchResultEntity.from_dict(item)
            content = entity.text or ""
            source = ""

            if entity.metadata:
                source_info = entity.metadata.get(SOURCE_KEY, {})
                source = source_info.get(URL_KEY, "")

            blob_url = ""
            blob_metadata = {}

            if generate_sas_urls_bool:
                # get filepath from 'additional_fields' first
                filepath = item.get("additional_fields", {}).get("filepath")
                if not filepath:
                    # fallback to 'metadata['source']['filename']'
                    filepath = entity.metadata.get('source', {}).get('filename')

                if filepath and isinstance(filepath, str):
                    # find the blob name that matches the filepath
                    blob_name = next(
                        (name for name in blob_names if name.endswith(filepath)),
                        None
                    )
                    if blob_name:
                        page_number = entity.metadata.get("page_number")
                        blob_url = generate_blob_url(blob_name, page_number)

                        if retrieve_metadata_bool:
                            try:
                                blob_client = container_client.get_blob_client(blob_name)
                                properties = blob_client.get_blob_properties()
                                blob_metadata = properties.metadata or {}
                            except Exception:
                                logger.error(f"Failed to retrieve metadata for blob: {blob_name}")
                    else:
                        logger.warning(f"No matching blob found for filepath: {filepath}")
            else:
                blob_url = ""  # blob_url empty if SAS URL generation is disabled

            retrieved_docs.append({
                "Content": content,
                "Source": source,
                "BlobURL": blob_url,
                "Metadata": blob_metadata
            })
        except Exception:
            logger.error("Error processing search result item.")
            continue

    doc_string = "\n\n".join([format_doc(doc) for doc in retrieved_docs])
    return doc_string
