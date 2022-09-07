from ftplib import FTP
from consts import auth_info

ftp = FTP(host=auth_info["FTP_IP"])
ftp.set_debuglevel(2)
auth_check = False


def connect_ftp(fbrowse_btn, login_btn, file_menu):
    global auth_check
    if auth_check:
        file_menu.setEnabled(False)
        fbrowse_btn.setEnabled(False)
        ftp.quit()
        login_btn.setText("Connect")
    else:
        login_btn.setText("Disconnect")
        try:
            ftp.login(user=auth_info["FTP_USER"], passwd=auth_info["FTP_PSSWD"])
            file_menu.setEnabled(True)
            fbrowse_btn.setEnabled(True)
            auth_check = True
        except:
            print("error")
