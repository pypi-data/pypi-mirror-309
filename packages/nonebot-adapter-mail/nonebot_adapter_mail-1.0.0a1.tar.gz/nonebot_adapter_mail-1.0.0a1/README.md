<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" alt="nonebot-adapter-mail"></a>
</p>

<div align="center">

# NoneBot-Adapter-Mail

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ Mail Adapter ✨_
<!-- prettier-ignore-end -->

<p align="center">
  <a href="https://raw.githubusercontent.com/mobyw/nonebot-adapter-mail/master/LICENSE">
    <img src="https://img.shields.io/github/license/mobyw/nonebot-adapter-mail" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-adapter-mail">
    <img src="https://img.shields.io/pypi/v/nonebot-adapter-mail" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue" alt="python">
  <a href="https://results.pre-commit.ci/latest/github/mobyw/nonebot-adapter-mail/master">
    <img src="https://results.pre-commit.ci/badge/github/mobyw/nonebot-adapter-mail/master.svg" alt="pre-commit" />
  </a>
</p>

</div>

## Configuration

Config mail adapter by modifying the `.env` or `.env.*` file.

### MAIL_BOTS

- `id`: The email address of the bot.
- `name`: The name of the bot.
- `password`: The password of the bot.
- `subject`: The default subject of the email.
- `imap`: The IMAP configuration of the bot.
  - `host`: The IMAP host.
  - `port`: The IMAP port.
  - `tls`: Whether to use TLS.
- `smtp`: The SMTP configuration of the bot.
  - `host`: The SMTP host.
  - `port`: The SMTP port.
  - `tls`: Whether to use TLS.

Example:

```dotenv
MAIL_BOTS='
[
  {
    "id": "i@example.com",
    "name": "Name",
    "password": "p4ssw0rd",
    "subject": "Sent by NoneBot",
    "imap": {
      "host": "imap.example.com",
      "port": 993,
      "tls": true
    },
    "smtp": {
      "host": "smtp.example.com",
      "port": 465,
      "tls": true
    }
  }
]
'
```
