from connection import ftp


def get_files():
    files_list = ftp.nlst()
    return (files_list)


def download_file(filename):
    try:
        with open(filename, "wb") as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
    except:
        return "error"