# Pamela

Installation:
-------------

Install required python lib.

    # apt-get install libpam-python python-pam cryptsetup

Copy the module with the others PAM.

    # cp pamela.py /lib/security/

Then modify the configuration files to add the module in the sessions.

    # emacs /etc/pam.d/common-session

Add the following line at the end of the file :

    session required  pam_python.so pamela.py
