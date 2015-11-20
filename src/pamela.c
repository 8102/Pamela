#include <stdio.h>

#include <security/pam_modules.h>
#include <security/pam_appl.h>
#include <security/pam_ext.h>

#ifndef PAM_EXTERN
# define PAM_EXTERN
#endif

#define UNUSED	__attribute__((unused))

void	test()
{
  printf("lol\n");
}

/* PAM entry point for session creation */
int	pam_sm_open_session(UNUSED pam_handle_t *pamh, UNUSED int flags,
			    UNUSED int argc, UNUSED const char **argv)
{
  test();
  return(PAM_IGNORE);
}

/* PAM entry point for session cleanup */
int	pam_sm_close_session(UNUSED pam_handle_t *pamh, UNUSED int flags,
			     UNUSED int argc, UNUSED const char **argv)
{
  return(PAM_IGNORE);
}

/* PAM entry point for accounting */
int	pam_sm_acct_mgmt(UNUSED pam_handle_t *pamh, UNUSED int flags,
			 UNUSED int argc, UNUSED const char **argv)
{
  return(PAM_IGNORE);
}

/* PAM entry point for authentication verification */
int	pam_sm_authenticate(UNUSED pam_handle_t *pamh, UNUSED int flags,
			    UNUSED int argc, UNUSED const char **argv)
{
  return(PAM_IGNORE);
}

/*
     PAM entry point for setting user credentials (that is, to actually
     establish the authenticated user's credentials to the service provider)
*/
int	pam_sm_setcred(UNUSED pam_handle_t *pamh, UNUSED int flags,
		       UNUSED int argc, UNUSED const char **argv)
{
  return(PAM_IGNORE);
}

/* PAM entry point for authentication token (password) changes */
int	pam_sm_chauthtok(UNUSED pam_handle_t *pamh, UNUSED int flags,
			 UNUSED int argc, UNUSED const char **argv)
{
  return(PAM_IGNORE);
}

#ifdef PAM_MODULE_ENTRY
PAM_MODULE_ENTRY("pamela");
#endif
