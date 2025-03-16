import logging
import os
import json
import azure.functions as func
from cryptography.fernet import Fernet
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Initialize Key Vault client
KEY_VAULT_URL = "https://keysme.vault.azure.net/"
credential = DefaultAzureCredential()
key_vault_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Retrieve the encryption key from Key Vault
ENCRYPTION_KEY = key_vault_client.get_secret("EncryptionKey").value
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_data(data):
    """Encrypt data using Fernet symmetric encryption."""
    if data is None:
        return None
    return cipher_suite.encrypt(data.encode()).decode()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get data from ADF
        data = req.get_json()

        # Encrypt columns for Table 1: clients
        if 'clients' in data:
            for record in data['clients']:
                record['FirstName'] = encrypt_data(record['FirstName'])
                record['LastName'] = encrypt_data(record['LastName'])
                record['Email'] = encrypt_data(record['Email'])
                record['PhoneNumber'] = encrypt_data(record['PhoneNumber'])
                record['Address'] = encrypt_data(record['Address'])
                record['DateOfBirth'] = encrypt_data(record['DateOfBirth'])

        # Encrypt columns for Table 2: tax_details
        if 'tax_details' in data:
            for record in data['tax_details']:
                record['TaxID'] = encrypt_data(record['TaxID'])
                record['TaxResidency'] = encrypt_data(record['TaxResidency'])

        return func.HttpResponse(json.dumps(data), status_code=200)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)