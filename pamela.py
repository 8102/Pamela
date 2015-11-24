from os import environ
from os.path import isfile

import subprocess

config = {}

#
#   Function that load the configuration file
#
def    loadConfig(pamh):
    configPath = isfile('/home/' + pamh.user + '/.config/pamela/pamela.conf')
    config = {
                'container_name': "myContainer",
                'container_path': "/home/" + pamh.user,
                'backup': True,
                'backup_name': "backup",
                'backup_path': "/home/" + pamh.user + "/.local/",
                'volume_size': 100,
                'format': "ext4",
                'encryption_level': "medium"
            }
    if configPath:
        with open(configPath, 'r') as file:
            buf = file.readlines()
            for line in buf:
                line = str.strip(line, '\n')
                tokens = str.strip(line, '=')
                if tokens[0] == 'container_name':
                    config['container_name'] = tokens[1]
                elif tokens[0] == 'container_path':
                    config['container_path'] = tokens[1]
                elif tokens[0] == 'container_level':
                    config['container_level'] = tokens[1]
                elif tokens[0] == 'backup_name':
                    config['backup_name'] = tokens[1]
                elif tokens[0] == 'backup_path':
                    config['backup_path'] = tokens[1]
                elif tokens[0] == 'volume_size':
                    config['volume_size'] = tokens[1]
                elif tokens[0] == 'encryption_level':
                    config['encryption_level'] = tokens[1]
                elif tokens[0] == 'format':
                    config['format'] = tokens[1]
    return config

#
#   Function that erase the backup and print an error message that is called
#   when there is an error
#
def    eraseBackup(pamh, config, errorMsg):
    cmd = "rm -fr " + config['backup_path'] + config['backup_name']
    ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print "Error: pamela.py: " + errorMsg

def    createBackup(pamh, config):
    cmd = "ls " + config['backup_path'] + config['backup_name']
    ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if ret == 2:
        cmd = "dd if=/dev/zero of=" + config['backup_path'] + config['backup_name']
        cmd += " bs=" + str(config['volume_size']) + "M count=1"
        ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if ret != 0:
            eraseBackup(pamh, config, "Failed to create volume")
            return False
    cmd = "losetup /dev/loop0 /home/" + pamh.user + "/.local/" + config['backup_name']
    subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if ret != 0:
        eraseBackup(pamh, config, "Failed to create loopback device")
        return False
    return True

#
#   Function that create the Container thanks to cryptsetup
#
def    createContainer(pamh, config):
    volume = config['container_path'] + config['container_name']
    volumeName = config['container_name']
    passwd = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Encryption password: ")).resp
    if passwd == None:
        pamh.conversation(pamh.Message(pamh.PAM_ERROR_MSG, "Bad password!"))
        return pamh.PAM_AUTH_ERR
    if createBackup(pamh, config) == False:
        return False
    cmd = "echo \'" + passwd + "\' | cryptsetup --key-size 256 luksFormat /dev/loop0"
    if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) != 0:
        eraseBackup(pamh, config, "Failed to create luks device")
        return False
    cmd = "echo \'" + passwd + "\' | cryptsetup luksOpen /dev/loop0 " + volumeName + " -"
    if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) != 0:
        eraseBackup(pamh, config, "Failed to open luks device")
        return False
    cmd = "mkfs." + config['format'] + " /dev/mapper/" + volumeName
    if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) != 0:
        eraseBackup(pamh, config, "Failed to format luks device")
        return False
    cmd = "mkdir -p " + config['container_path'] + "/" + volumeName
    if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) != 0:
        eraseBackup(pamh, config, "Failed to create mount point")
        return False
    cmd = "mount /dev/mapper/" + volumeName + " " + config['container_path'] + "/" + volumeName
    if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) != 0:
        eraseBackup(pamh, config, "Failed to mount luks device")
        return False
    cmd = "chown " + pamh.user + ":" + pamh.user + " " + config['container_path'] + "/" + volumeName
    if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) != 0:
        eraseBackup(pamh, config, "Failed to chown luks device")
        return False
    return True

#
#   Function that check if the user is already log, if so it return True, else
#   it returns False
#
def    checkUser(curUser):
    ret = subprocess.check_output("who")
    for line in ret.splitlines():
        if line.split()[0] == curUser:
            return True
    return False

def    closeContainer(pamh, config):
    cmd = "umount " + config['container_path'] + "/" + config['container_name']
    ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    cmd = "cryptsetup luksClose " + config['container_name']
    ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if config['backup'] != True:
        cmd = "rm -fr " + config['backup_path'] + config['backup_name']
        ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    cmd = "rm -fr /home/" + pamh.user + config['backup_name']
    ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    cmd = "losetup -d /dev/loop0"
    ret = subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

def    pam_sm_authenticate(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_open_session(pamh, flags, argv):
    global config
    if pamh.user == "root":
        return pamh.PAM_SUCCESS
    if checkUser(pamh.user) == True:
        return pamh.PAM_SUCCESS
    config = loadConfig(pamh)
    ret = createContainer(pamh, config)
    if ret == False:
        return pamh.PAM_SUCCESS
    elif ret == pamh.PAM_AUTH_ERR:
        return pamh.PAM_AUTH_ERR
    print "Pamela module successfully loaded"
    return pamh.PAM_SUCCESS

def    pam_sm_close_session(pamh, flags, argv):
    global config
    if pamh.user == "root":
        return pamh.PAM_SUCCESS
    if checkUser(pamh.user) == True:
        return pamh.PAM_SUCCESS
    closeContainer(pamh, config)
    return pamh.PAM_SUCCESS

def    pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS
