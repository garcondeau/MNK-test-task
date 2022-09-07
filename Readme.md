# MNK Test Task

MNK Test Task is a Python ftp client with pandas integration.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependecies.
```bash
pip install requirements.txt 
```

## Before start
Before starting work with MNK Test Task you must create database which is declared in consts.py 
```bash
CREATE DATABASE mnktask;
```

## Requisites edit
Use consts.py to edit FTP ip, user and password and DB host, user and password

```python
auth_info = {
    "FTP_IP": "138.201.56.185",
    "FTP_USER": "rekrut",
    "FTP_PSSWD": "zI4wG9yM5krQ3d"
}

db_info = {
    "DB_NAME": "mnktask",
    "DB_HOST": "localhost",
    "DB_PORT": "3306",
    "DB_USER": "root",
    "DB_PSSWD": "root"
}

```

## Software
MNK Test Task uses [7z](https://www.7-zip.org) preinstaled and [MySQL](https://www.mysql.com)

## About

Made by [garcondeau](https://github.com/garcondeau)