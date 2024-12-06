"""
This module defines Pydantic models for representing email-related data schemas.

Classes:
    EmailAddress (BaseModel): Schema for representing an email address.
    EmailMessage (BaseModel): Schema for representing an email message.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class EmailAddress(BaseModel):
    """
    EmailAddress schema for representing an email address.

    Attributes:
        address (str): The email address.
        name (Optional[str]): The name associated with the email address.
    """
    address: str
    name: Optional[str]


class EmailMessage(BaseModel):
    """
    EmailMessage schema for representing an email message.

    Attributes:
        id (str): The unique identifier for the email message.
        subject (Optional[str]): The subject of the email.
        from_email (List[EmailAddress]): The list of email addresses from which the email was sent.
        to (List[EmailAddress]): The list of email addresses to which the email was sent.
        received (Optional[str]): The date and time when the email was received.
        body (Optional[str]): The body content of the email.
        attachments (List): The list of attachments included in the email.
        bcc (List): The list of email addresses in the BCC field.
        cc (List): The list of email addresses in the CC field.
        domain (Optional[str]): The domain from which the email was sent.
        folder (Optional[str]): The folder in which the email is stored.
        inbox (Optional[str]): The inbox to which the email belongs.
        ip (Optional[str]): The IP address from which the email was sent.
        labels (List): The list of labels associated with the email.
        links (List): The list of links included in the email.
        originalInbox (Optional[str]): The original inbox to which the email was sent.
        read (Optional[bool]): Indicates whether the email has been read.
        rtls (Optional[bool]): Indicates whether the email is RTL (right-to-left).
        savedBy (Optional[str]): The user who saved the email.
        size (Optional[int]): The size of the email in bytes.
        spam (Optional[int]): Indicates whether the email is marked as spam.
        via (Optional[str]): The service or method via which the email was sent.
    """
    id: str = Field(alias="_id")
    subject: Optional[str]
    from_email: List[EmailAddress] = Field(default_factory=list)
    to: List[EmailAddress]
    received: Optional[str]
    body: Optional[str] = Field(default="")
    attachments: List
    bcc: List
    cc: List
    domain: Optional[str]
    folder: Optional[str]
    inbox: Optional[str]
    ip: Optional[str]
    labels: List
    links: List
    originalInbox: Optional[str]
    read: Optional[bool]
    rtls: Optional[bool]
    savedBy: Optional[str]
    size: Optional[int]
    spam: Optional[int]
    via: Optional[str]
