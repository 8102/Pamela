# Pamela

Installation:
-------------

Compile:

    $ make

Copy the module with the others PAM.

    $ sudo cp pamela.so /lib/x86_64-linux-gnu/security/

Then modify the configuration files to add the module in the sessions.

     $ sudo emacs /etc/pam.d/common-session

Add the following line at the end of the file :

    session required pamela.so

