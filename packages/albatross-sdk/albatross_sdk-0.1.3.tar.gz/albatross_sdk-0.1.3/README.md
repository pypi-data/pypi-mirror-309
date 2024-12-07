# Albatross Python SDK

[![Pyright Type Checking](https://github.com/albatross-core/py-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/albatross-core/py-sdk/actions/workflows/ci.yml)

published: https://pypi.org/project/albatross-sdk/

A Python SDK for interacting with the Albatross API. This SDK provides a simple and intuitive way to manage categories and units in your Albatross instance.

## Features

- Easy authentication using ECDSA keypairs
- Category management (create, update, list)
- Unit operations
- CSV data import support

## Installation

```bash
pip install albatross-sdk
```

## Prerequisites

- Python 3.12 or higher
- An Albatross instance and credentials
- ECDSA keypair for authentication

## Authentication

### Generating a Keypair

Generate an [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) keypair using OpenSSL:

```bash
openssl ecparam -genkey -name prime256v1 -noout -out ecdsa_private_key.pem
openssl ec -in ecdsa_private_key.pem -pubout -out ecdsa_public_key.pem
```

## Quick Start

```python
from albatross_sdk.lib import AlbatrossSDK, CategoryData

# Initialize the client
private_key = AlbatrossSDK.load_private_key("path/to/your/private_key.pem")
instance_id = "your-instance-id"
client = AlbatrossSDK(
    instance=instance_id,
    private_key=private_key,
    base_url="https://your-albatross-instance.com"  # Optional
)

# Check API version
version = client.get_api_version()
print(f"Connected to Albatross API version: {version}")

# Create a category
category_data: CategoryData = {
    "unit": "user",
    "values": {
        "country_code": "US",
        "grade_level": 3,
        "user": "user-uuid"
    }
}

response = client.put_categories([category_data])
print(f"Category created: {response}")
```

## Working with Categories

### Single Category Operations

```python
# Define a category
user_category: CategoryData = {
    "unit": "user",
    "values": {
        "country_code": "AT",
        "grade_level": 2,
        "user": "39e23058-b7da-4a79-b464-5b67b579a433"
    }
}

# Create or update the category
result = client.put_categories([user_category])
```

### Bulk Import from CSV

```python
# Import categories from a CSV file
client.put_categories_csv("path/to/categories.csv", "user")
```

## Configuration Examples

```python
# Multiple instance configuration
instances = {
    "prod": "c094dea1-8b01-11ef-9882-068cf85ff8bb",
    "staging": "22a06113-8b04-11ef-ade1-42010aac0020",
    "dev": "96757573-827b-11ef-9882-068cf85ff8bb",
}

# Initialize client with specific instance
client = AlbatrossSDK(
    instance=instances["prod"],
    private_key=private_key,
    base_url="https://api.albatross.com"
)
```

## Development

### Running Tests

```bash
python -m pytest
```

### Type Checking

```bash
pyright .
```

## Related Resources

- [Go SDK Sample Code](https://gist.github.com/johnb8005/878da37315920b8538a25f651ba0db0f)
- [API Documentation](https://albatross-core.github.io/publicApiSpec/#/)
