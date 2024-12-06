import html
import base64
import email.message
import email.encoders
import email.mime.base
import email.mime.text

import mailparser
from nonebot.utils import escape_tag

from .model import Mail, User
from .message import Message, Attachment, MessageSegment


def escape_bytelines(s: list[bytearray]) -> str:
    """
    Escape a list of bytearrays to a string.

    - `s`: The list of bytearrays to escape.
    """
    return f'[{escape_tag(", ".join([i.decode() for i in s]))}]'


def extract_mail_parts(message: Message) -> list[email.message.EmailMessage]:
    """
    Extract email parts from a Message object.

    - `message`: The Message object to extract.
    """
    text: str = ""
    attachments = []
    contains_html = any(segment.type == "html" for segment in message)
    for segment in message:
        if segment.type == "text":
            text += (
                segment.data["text"]
                if not contains_html
                else html.escape(segment.data["text"])
            )
        elif segment.type == "html":
            text += segment.data["html"]
        elif segment.type == "attachment":
            attachments.append(segment)
    parts = []
    if contains_html:
        parts.append(email.mime.text.MIMEText(text, "html"))
    else:
        parts.append(email.mime.text.MIMEText(text))
    for attachment in attachments:
        if attachment.data["content_type"] and "/" in attachment.data["content_type"]:
            main_type, sub_type = attachment.data["content_type"].split("/")
        else:
            main_type, sub_type = "application", "octet-stream"
        part = email.mime.base.MIMEBase(main_type, sub_type)
        part.set_payload(attachment.data["data"])
        email.encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{attachment.data["name"]}"',
        )
        parts.append(part)
    return parts


def parse_attachment(attachment) -> Attachment:
    """
    Parse the attachment and return the Attachment object.

    - `attachment`: The attachment to parse.
    """

    data = (
        base64.b64decode(attachment["payload"])
        if attachment["binary"]
        else attachment["payload"]
    )

    if isinstance(data, str):
        data = data.encode()

    return MessageSegment.attachment(
        data,
        attachment["filename"],
        attachment["mail_content_type"],
    )


def parse_byte_mail(byte_mail: bytes) -> Mail:
    """
    Parse the mail and return the Mail object.

    - `byte_mail`: The byte mail to parse.
    """
    mail = mailparser.parse_from_bytes(byte_mail)

    return Mail(
        id=str(mail.message_id),
        sender=User(
            id=mail.from_[0][1],
            name=mail.from_[0][0],
        ),
        recipients_to=[
            User(
                id=recipient[1],
                name=recipient[0],
            )
            for recipient in mail.to
        ],
        recipients_cc=[
            User(
                id=recipient[1],
                name=recipient[0],
            )
            for recipient in mail.headers.get("Cc", [])
        ],
        recipients_bcc=[
            User(
                id=recipient[1],
                name=recipient[0],
            )
            for recipient in mail.headers.get("Bcc", [])
        ],
        date=mail.date,
        timezone=float(mail.timezone) if mail.timezone else None,
        message=(
            Message([MessageSegment.text(text) for text in mail.text_plain])
            + Message([parse_attachment(attachment) for attachment in mail.attachments])
        ),
        original_message=(
            Message([MessageSegment.html(html) for html in mail.text_html])
            + Message(
                [parse_attachment(attachment) for attachment in mail.attachments],
            )
        ),
        in_reply_to=str(mail.in_reply_to) if mail.in_reply_to else None,
    )
