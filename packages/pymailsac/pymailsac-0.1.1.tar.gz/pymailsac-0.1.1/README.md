# Mailsac Client Library

![Build Status](https://github.com/gsejas/mailsac-pyclient/actions/workflows/test-and-package.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/mailsac-pyclient)
![License](https://img.shields.io/github/license/GSejas/mailsac-pyclient)
![Python Version](https://img.shields.io/pypi/pyversions/mailsac-pyclient)

This is a Python client library for interacting with the Mailsac REST API. It provides a simple interface to receive, and manage emails using Mailsac's services. See full documentation for the API, here https://mailsac.com/docs/api/#section/About-the-API

## Features

- Retrieve messages from your Mailsac inbox.
- Delete messages from your inbox.

## Installation

To install the Mailsac client library, you can use pip:

```
pip install -r requirements.txt
```

## Usage

Here is a basic example of how to use the MailsacClient:

```python
from mailsac.client import MailsacClient

# Initialize the client
client = MailsacClient(api_key='your_api_key')

# Get messages
messages = client.get_messages('your_inbox_id')

# Delete a message
client.delete_message('your_inbox_id', 'message_id')
```

## Client Initialization

```mermaid
sequenceDiagram
    participant User
    participant MailsacClient
    User->>MailsacClient: Initialize with API key
    MailsacClient-->>User: Client instance created
```

## Fetching Messages

```mermaid
sequenceDiagram
    participant User
    participant MailsacClient
    participant MailsacAPI
    User->>MailsacClient: get_messages(email)
    MailsacClient->>MailsacAPI: GET /addresses/{email}/messages
    MailsacAPI-->>MailsacClient: JSON response with messages
    MailsacClient-->>User: List of EmailMessage instances
```

## Deleting a Message

```mermaid
sequenceDiagram
    participant User
    participant MailsacClient
    participant MailsacAPI
    User->>MailsacClient: delete_message(email, message_id)
    MailsacClient->>MailsacAPI: DELETE /addresses/{email}/messages/{message_id}
    MailsacAPI-->>MailsacClient: Success response
    MailsacClient-->>User: True
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bugs.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.