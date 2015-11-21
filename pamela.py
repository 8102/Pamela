from os import environ
from os.path import isfile

pathTest = './pamela.conf'
pathProd = isfile('/home/' + environ['USER'] + '.config/pamela/pamela.conf')

def loadConfig():
	config = {
		'container_name': "myContainer",
		'container_path': "/home/" + environ['USER'],
		'encryption_level': "medium"
	}
	if pathTest:
		with open(pathTest, 'r') as f:
			buf = f.readlines()
			for line in buf:
				line = str.strip(line, '\n')
				tokens = str.split(line, '=')
				if tokens[0] == 'container_name':
					config['container_name'] = tokens[1]
				elif tokens[0] == 'container_path':
					config['container_path'] = tokens[1]
				elif tokens[0] == 'encryption_level':
					config['encryption_level'] = tokens[1]
	return config

def    pam_sm_authenticate(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_close_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def    pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS

config = loadConfig()
print(config)