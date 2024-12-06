# Mailsac Client Library

![Build Status](https://github.com/gsejas/mailsac-pyclient/actions/workflows/test-and-package.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/pymailsac)
![License](https://img.shields.io/github/license/GSejas/mailsac-pyclient)
![Python Version](https://img.shields.io/pypi/pyversions/pymailsac)

This is a Python client library for interacting with the Mailsac REST API. It provides a simple interface to receive, and manage emails using Mailsac's services. See full documentation for the API, here https://mailsac.com/docs/api/#section/About-the-API

## Features

- Retrieve messages from your Mailsac inbox.
- Delete messages from your inbox.


| **Category**           | **Endpoint**                                               | **Method** | **Description**                                        | Implemented |
| ---------------------- | ---------------------------------------------------------- | ---------- | ------------------------------------------------------ | ----------- |
| **Email Messages API** | /addresses/{email}/message-count                           | GET        | Count messages for an email inbox                      | No          |
|                        | /addresses/{email}/messages                                | GET        | List messages for an email inbox                       | Yes         |
|                        | /addresses/{email}/messages                                | DELETE     | Delete all messages for an email inbox                 | No          |
|                        | /addresses/starred/messages                                | GET        | List starred (saved) messages on the account           | No          |
|                        | /addresses/{email}/messages/{messageId}                    | GET        | Get email message metadata                             | Yes         |
|                        | /addresses/{email}/messages/{messageId}                    | DELETE     | Delete an email message                                | Yes         |
|                        | /raw/{email}/{messageId}                                   | GET        | Get original SMTP message                              | No          |
|                        | /addresses/{email}/messages/{messageId}/headers            | GET        | Get parsed message headers                             | No          |
|                        | /dirty/{email}/{messageId}                                 | GET        | Get message HTML body (dirty)                          | No          |
|                        | /body/{email}/{messageId}                                  | GET        | Get message HTML body (sanitized)                      | No          |
|                        | /text/{email}/{messageId}                                  | GET        | Get message plaintext                                  | Yes         |
|                        | /addresses/{email}/messages/{messageId}/star               | PUT        | Star (save) a message                                  | No          |
|                        | /addresses/{email}/messages/{messageId}/labels/{label}     | PUT        | Add a label to a message                               | No          |
|                        | /addresses/{email}/messages/{messageId}/labels/{label}     | DELETE     | Remove a label from a message                          | No          |
|                        | /addresses/{email}/messages/{messageId}/folder/{folder}    | PUT        | Move a message into a folder                           | No          |
|                        | /addresses/{email}/messages/{messageId}/read/{readBoolean} | PUT        | Set message read/unread status                         | No          |
|                        | /inbox                                                     | GET        | Get all account messages paginated                     | No          |
|                        | /inbox-filter                                              | GET        | Filter messages in account by to, from, and/or subject | No          |
|                        | /inbox-search                                              | GET        | Search messages by to, from, and subject               | No          |
|                        | /domains/{domain}/messages                                 | GET        | List messages for a domain                             | No          |
|                        | /domains/{domain}/delete-all-domain-mail                   | POST       | Delete all messages in a domain                        | No          |

## Installation

To install the Mailsac client library, you can use pip:

```
pip install pymailsac
```

## Usage

Here is a basic example of how to use the MailsacClient:

```python
from pymailsac.client import MailsacClient

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
